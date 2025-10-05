import { IBackoff, IBackoffFactory } from './Backoff';
export declare class ConstantBackoff implements IBackoffFactory<unknown> {
    private readonly interval;
    /**
     * Backoff that returns a constant interval.
     */
    constructor(interval: number);
    /**
     * @inheritdoc
     */
    next(): IBackoff<unknown>;
}
