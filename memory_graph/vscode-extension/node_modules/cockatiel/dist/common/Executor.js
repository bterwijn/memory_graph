"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExecuteWrapper = exports.returnOrThrow = void 0;
const Event_1 = require("./Event");
const returnOrThrow = (failure) => {
    if ('error' in failure) {
        throw failure.error;
    }
    if ('success' in failure) {
        return failure.success;
    }
    return failure.value;
};
exports.returnOrThrow = returnOrThrow;
const makeStopwatch = () => {
    if (typeof performance !== 'undefined') {
        const start = performance.now();
        return () => performance.now() - start;
    }
    else {
        const start = process.hrtime.bigint();
        return () => Number(process.hrtime.bigint() - start) / 1000000; // ns->ms
    }
};
class ExecuteWrapper {
    constructor(errorFilter = () => false, resultFilter = () => false) {
        this.errorFilter = errorFilter;
        this.resultFilter = resultFilter;
        this.successEmitter = new Event_1.EventEmitter();
        this.failureEmitter = new Event_1.EventEmitter();
        this.onSuccess = this.successEmitter.addListener;
        this.onFailure = this.failureEmitter.addListener;
    }
    clone() {
        return new ExecuteWrapper(this.errorFilter, this.resultFilter);
    }
    async invoke(fn, ...args) {
        const stopwatch = this.successEmitter.size || this.failureEmitter.size ? makeStopwatch() : null;
        try {
            const value = await fn(...args);
            if (!this.resultFilter(value)) {
                if (stopwatch) {
                    this.successEmitter.emit({ duration: stopwatch() });
                }
                return { success: value };
            }
            if (stopwatch) {
                this.failureEmitter.emit({ duration: stopwatch(), handled: true, reason: { value } });
            }
            return { value };
        }
        catch (rawError) {
            const error = rawError;
            const handled = this.errorFilter(error);
            if (stopwatch) {
                this.failureEmitter.emit({ duration: stopwatch(), handled, reason: { error } });
            }
            if (!handled) {
                throw error;
            }
            return { error };
        }
    }
}
exports.ExecuteWrapper = ExecuteWrapper;
//# sourceMappingURL=Executor.js.map