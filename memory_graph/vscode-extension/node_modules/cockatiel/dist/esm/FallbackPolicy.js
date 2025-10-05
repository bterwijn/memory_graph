import { neverAbortedSignal } from './common/abort';
export class FallbackPolicy {
    constructor(executor, value) {
        this.executor = executor;
        this.value = value;
        /**
         * @inheritdoc
         */
        this.onSuccess = this.executor.onSuccess;
        /**
         * @inheritdoc
         */
        this.onFailure = this.executor.onFailure;
    }
    /**
     * Executes the given function.
     * @param fn Function to execute.
     * @returns The function result or fallback value.
     */
    async execute(fn, signal = neverAbortedSignal) {
        const result = await this.executor.invoke(fn, { signal });
        if ('success' in result) {
            return result.success;
        }
        return this.value();
    }
}
//# sourceMappingURL=FallbackPolicy.js.map