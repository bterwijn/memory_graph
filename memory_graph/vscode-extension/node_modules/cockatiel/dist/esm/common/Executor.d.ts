import { FailureReason, IFailureEvent, ISuccessEvent } from '../Policy';
export type FailureOrSuccess<R> = FailureReason<R> | {
    success: R;
};
export declare const returnOrThrow: <R>(failure: FailureOrSuccess<R>) => R;
export declare class ExecuteWrapper {
    private readonly errorFilter;
    private readonly resultFilter;
    private readonly successEmitter;
    private readonly failureEmitter;
    readonly onSuccess: import("./Event").Event<ISuccessEvent>;
    readonly onFailure: import("./Event").Event<IFailureEvent>;
    constructor(errorFilter?: (error: Error) => boolean, resultFilter?: (result: unknown) => boolean);
    clone(): ExecuteWrapper;
    invoke<T extends unknown[], R>(fn: (...args: T) => PromiseLike<R> | R, ...args: T): Promise<FailureOrSuccess<R>>;
}
