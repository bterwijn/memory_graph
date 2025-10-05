"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TimeoutPolicy = exports.TimeoutStrategy = void 0;
const abort_1 = require("./common/abort");
const Event_1 = require("./common/Event");
const Executor_1 = require("./common/Executor");
const TaskCancelledError_1 = require("./errors/TaskCancelledError");
var TimeoutStrategy;
(function (TimeoutStrategy) {
    /**
     * Cooperative timeouts will simply revoke the inner cancellation token,
     * assuming the caller handles cancellation and throws or returns appropriately.
     */
    TimeoutStrategy["Cooperative"] = "optimistic";
    /**
     * Aggressive cancellation immediately throws
     */
    TimeoutStrategy["Aggressive"] = "aggressive";
})(TimeoutStrategy || (exports.TimeoutStrategy = TimeoutStrategy = {}));
class TimeoutPolicy {
    constructor(duration, options, executor = new Executor_1.ExecuteWrapper(), unref = false) {
        this.duration = duration;
        this.options = options;
        this.executor = executor;
        this.unref = unref;
        this.timeoutEmitter = new Event_1.EventEmitter();
        /**
         * @inheritdoc
         */
        this.onTimeout = this.timeoutEmitter.addListener;
        /**
         * @inheritdoc
         */
        this.onFailure = this.executor.onFailure;
        /**
         * @inheritdoc
         */
        this.onSuccess = this.executor.onSuccess;
    }
    /**
     * When timing out, a referenced timer is created. This means the Node.js
     * event loop is kept active while we're waiting for the timeout, as long as
     * the function hasn't returned. Calling this method on the timeout builder
     * will unreference the timer, allowing the process to exit even if a
     * timeout might still be happening.
     */
    dangerouslyUnref() {
        const t = new TimeoutPolicy(this.duration, this.options, this.executor, true);
        return t;
    }
    /**
     * Executes the given function.
     * @param fn Function to execute. Takes in a nested cancellation token.
     * @throws a {@link TaskCancelledError} if a timeout occurs
     */
    async execute(fn, signal) {
        const { ctrl: aborter, dispose: disposeAbort } = (0, abort_1.deriveAbortController)(signal);
        const timer = setTimeout(() => aborter.abort(), this.duration);
        if (this.unref) {
            timer.unref();
        }
        const context = { signal: aborter.signal };
        const onceAborted = (0, Event_1.onAbort)(aborter.signal);
        const onCancelledListener = onceAborted.event(() => this.timeoutEmitter.emit());
        try {
            if (this.options.strategy === TimeoutStrategy.Cooperative) {
                return (0, Executor_1.returnOrThrow)(await this.executor.invoke(fn, context, aborter.signal));
            }
            return await this.executor
                .invoke(async () => Promise.race([
                Promise.resolve(fn(context, aborter.signal)),
                Event_1.Event.toPromise(onceAborted.event).then(() => {
                    throw new TaskCancelledError_1.TaskCancelledError(`Operation timed out after ${this.duration}ms`);
                }),
            ]))
                .then(Executor_1.returnOrThrow);
        }
        finally {
            onCancelledListener.dispose();
            onceAborted.dispose();
            if (this.options.abortOnReturn !== false) {
                aborter.abort();
            }
            clearTimeout(timer);
            disposeAbort();
        }
    }
}
exports.TimeoutPolicy = TimeoutPolicy;
//# sourceMappingURL=TimeoutPolicy.js.map