import { IBackoff, IBackoffFactory } from './Backoff';
export type DelegateBackoffFn<T, S = void> = (context: T, state?: S) => {
    delay: number;
    state: S;
} | number;
export declare class DelegateBackoff<T, S = void> implements IBackoffFactory<T> {
    private readonly fn;
    /**
     * Backoff that delegates to a user-provided function. The function takes
     * the backoff context, and can optionally take (and return) a state value
     * that will be passed into subsequent backoff requests.
     */
    constructor(fn: DelegateBackoffFn<T, S>);
    /**
     * @inheritdoc
     */
    next(context: T): IBackoff<T>;
}
