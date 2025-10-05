import { IBackoff, IBackoffFactory } from './Backoff';
export declare class IterableBackoff implements IBackoffFactory<unknown> {
    private readonly durations;
    /**
     * Backoff that returns a number from an iterable.
     */
    constructor(durations: ReadonlyArray<number>);
    /**
     * @inheritdoc
     */
    next(_context: unknown): IBackoff<unknown>;
}
