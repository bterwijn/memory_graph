import { ExecuteWrapper } from './common/Executor';
import { IDefaultPolicyContext, IPolicy } from './Policy';
export declare class FallbackPolicy<AltReturn> implements IPolicy<IDefaultPolicyContext, AltReturn> {
    private readonly executor;
    private readonly value;
    readonly _altReturn: AltReturn;
    /**
     * @inheritdoc
     */
    readonly onSuccess: import(".").Event<import("./Policy").ISuccessEvent>;
    /**
     * @inheritdoc
     */
    readonly onFailure: import(".").Event<import("./Policy").IFailureEvent>;
    constructor(executor: ExecuteWrapper, value: () => AltReturn);
    /**
     * Executes the given function.
     * @param fn Function to execute.
     * @returns The function result or fallback value.
     */
    execute<T>(fn: (context: IDefaultPolicyContext) => PromiseLike<T> | T, signal?: AbortSignal): Promise<T | AltReturn>;
}
