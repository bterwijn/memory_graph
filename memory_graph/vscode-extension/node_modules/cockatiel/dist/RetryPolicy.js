"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RetryPolicy = void 0;
const ConstantBackoff_1 = require("./backoff/ConstantBackoff");
const abort_1 = require("./common/abort");
const Event_1 = require("./common/Event");
const delay = (duration, unref) => new Promise(resolve => {
    const timer = setTimeout(resolve, duration);
    if (unref) {
        timer.unref();
    }
});
class RetryPolicy {
    constructor(options, executor) {
        this.options = options;
        this.executor = executor;
        this.onGiveUpEmitter = new Event_1.EventEmitter();
        this.onRetryEmitter = new Event_1.EventEmitter();
        /**
         * @inheritdoc
         */
        this.onSuccess = this.executor.onSuccess;
        /**
         * @inheritdoc
         */
        this.onFailure = this.executor.onFailure;
        /**
         * Emitter that fires when we retry a call, before any backoff.
         *
         */
        this.onRetry = this.onRetryEmitter.addListener;
        /**
         * Emitter that fires when we're no longer retrying a call and are giving up.
         */
        this.onGiveUp = this.onGiveUpEmitter.addListener;
    }
    /**
     * When retrying, a referenced timer is created. This means the Node.js event
     * loop is kept active while we're delaying a retried call. Calling this
     * method on the retry builder will unreference the timer, allowing the
     * process to exit even if a retry might still be pending.
     */
    dangerouslyUnref() {
        return new RetryPolicy({ ...this.options, unref: true }, this.executor.clone());
    }
    /**
     * Executes the given function with retries.
     * @param fn Function to run
     * @returns a Promise that resolves or rejects with the function results.
     */
    async execute(fn, signal = abort_1.neverAbortedSignal) {
        const factory = this.options.backoff || new ConstantBackoff_1.ConstantBackoff(0);
        let backoff;
        for (let retries = 0;; retries++) {
            const result = await this.executor.invoke(fn, { attempt: retries, signal });
            if ('success' in result) {
                return result.success;
            }
            if (!signal.aborted && retries < this.options.maxAttempts) {
                const context = { attempt: retries + 1, signal, result };
                backoff = backoff ? backoff.next(context) : factory.next(context);
                const delayDuration = backoff.duration;
                const delayPromise = delay(delayDuration, !!this.options.unref);
                // A little sneaky reordering here lets us use Sinon's fake timers
                // when we get an emission in our tests.
                this.onRetryEmitter.emit({ ...result, delay: delayDuration, attempt: retries + 1 });
                await delayPromise;
                continue;
            }
            this.onGiveUpEmitter.emit(result);
            if ('error' in result) {
                throw result.error;
            }
            return result.value;
        }
    }
}
exports.RetryPolicy = RetryPolicy;
//# sourceMappingURL=RetryPolicy.js.map