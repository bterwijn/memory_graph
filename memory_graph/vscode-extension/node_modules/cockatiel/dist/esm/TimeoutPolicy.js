import { deriveAbortController } from './common/abort';
import { Event, EventEmitter, onAbort } from './common/Event';
import { ExecuteWrapper, returnOrThrow } from './common/Executor';
import { TaskCancelledError } from './errors/TaskCancelledError';
export var TimeoutStrategy;
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
})(TimeoutStrategy || (TimeoutStrategy = {}));
export class TimeoutPolicy {
    constructor(duration, options, executor = new ExecuteWrapper(), unref = false) {
        this.duration = duration;
        this.options = options;
        this.executor = executor;
        this.unref = unref;
        this.timeoutEmitter = new EventEmitter();
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
        const { ctrl: aborter, dispose: disposeAbort } = deriveAbortController(signal);
        const timer = setTimeout(() => aborter.abort(), this.duration);
        if (this.unref) {
            timer.unref();
        }
        const context = { signal: aborter.signal };
        const onceAborted = onAbort(aborter.signal);
        const onCancelledListener = onceAborted.event(() => this.timeoutEmitter.emit());
        try {
            if (this.options.strategy === TimeoutStrategy.Cooperative) {
                return returnOrThrow(await this.executor.invoke(fn, context, aborter.signal));
            }
            return await this.executor
                .invoke(async () => Promise.race([
                Promise.resolve(fn(context, aborter.signal)),
                Event.toPromise(onceAborted.event).then(() => {
                    throw new TaskCancelledError(`Operation timed out after ${this.duration}ms`);
                }),
            ]))
                .then(returnOrThrow);
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
//# sourceMappingURL=TimeoutPolicy.js.map