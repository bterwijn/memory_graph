import { IBackoffFactory } from './backoff/Backoff';
import { ExecuteWrapper } from './common/Executor';
import { FailureReason, IDefaultPolicyContext, IPolicy } from './Policy';
/**
 * Context passed into the execute method of the builder.
 */
export interface IRetryContext extends IDefaultPolicyContext {
    /**
     * The retry attempt, starting at 1 for calls into backoffs.
     */
    attempt: number;
}
/**
 * Context passed into backoff delegate.
 */
export interface IRetryBackoffContext<R> extends IRetryContext {
    /**
     * The result of the last method call. Either a thrown error, or a value
     * that we determined should be retried upon.
     */
    result: FailureReason<R>;
}
export interface IRetryPolicyConfig {
    backoff: IBackoffFactory<IRetryBackoffContext<unknown>>;
    maxAttempts: number;
    /**
     * Whether to unreference the internal timer. This means the policy will not
     * keep the Node.js even loop active. Defaults to `false`.
     */
    unref?: boolean;
}
export declare class RetryPolicy implements IPolicy<IRetryContext> {
    private options;
    private readonly executor;
    readonly _altReturn: never;
    private readonly onGiveUpEmitter;
    private readonly onRetryEmitter;
    /**
     * @inheritdoc
     */
    readonly onSuccess: import("./common/Event").Event<import("./Policy").ISuccessEvent>;
    /**
     * @inheritdoc
     */
    readonly onFailure: import("./common/Event").Event<import("./Policy").IFailureEvent>;
    /**
     * Emitter that fires when we retry a call, before any backoff.
     *
     */
    readonly onRetry: import("./common/Event").Event<FailureReason<unknown> & {
        delay: number;
        attempt: number;
    }>;
    /**
     * Emitter that fires when we're no longer retrying a call and are giving up.
     */
    readonly onGiveUp: import("./common/Event").Event<FailureReason<unknown>>;
    constructor(options: Readonly<IRetryPolicyConfig>, executor: ExecuteWrapper);
    /**
     * When retrying, a referenced timer is created. This means the Node.js event
     * loop is kept active while we're delaying a retried call. Calling this
     * method on the retry builder will unreference the timer, allowing the
     * process to exit even if a retry might still be pending.
     */
    dangerouslyUnref(): RetryPolicy;
    /**
     * Executes the given function with retries.
     * @param fn Function to run
     * @returns a Promise that resolves or rejects with the function results.
     */
    execute<T>(fn: (context: IRetryContext) => PromiseLike<T> | T, signal?: AbortSignal): Promise<T>;
}
