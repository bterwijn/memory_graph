import { neverAbortedSignal } from './common/abort';
import { ExecuteWrapper, returnOrThrow } from './common/Executor';
/**
 * A no-op policy, useful for unit tests and stubs.
 */
export class NoopPolicy {
    constructor() {
        this.executor = new ExecuteWrapper();
        this.onSuccess = this.executor.onSuccess;
        this.onFailure = this.executor.onFailure;
    }
    async execute(fn, signal = neverAbortedSignal) {
        return returnOrThrow(await this.executor.invoke(fn, { signal }));
    }
}
//# sourceMappingURL=NoopPolicy.js.map