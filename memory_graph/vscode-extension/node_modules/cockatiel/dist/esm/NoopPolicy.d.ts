import { IDefaultPolicyContext, IPolicy } from './Policy';
/**
 * A no-op policy, useful for unit tests and stubs.
 */
export declare class NoopPolicy implements IPolicy {
    readonly _altReturn: never;
    private readonly executor;
    readonly onSuccess: import(".").Event<import("./Policy").ISuccessEvent>;
    readonly onFailure: import(".").Event<import("./Policy").IFailureEvent>;
    execute<T>(fn: (context: IDefaultPolicyContext) => PromiseLike<T> | T, signal?: AbortSignal): Promise<T>;
}
