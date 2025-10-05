"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NoopPolicy = void 0;
const abort_1 = require("./common/abort");
const Executor_1 = require("./common/Executor");
/**
 * A no-op policy, useful for unit tests and stubs.
 */
class NoopPolicy {
    constructor() {
        this.executor = new Executor_1.ExecuteWrapper();
        this.onSuccess = this.executor.onSuccess;
        this.onFailure = this.executor.onFailure;
    }
    async execute(fn, signal = abort_1.neverAbortedSignal) {
        return (0, Executor_1.returnOrThrow)(await this.executor.invoke(fn, { signal }));
    }
}
exports.NoopPolicy = NoopPolicy;
//# sourceMappingURL=NoopPolicy.js.map