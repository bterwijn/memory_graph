import { IBackoff, IBackoffFactory } from './Backoff';
import { GeneratorFn } from './ExponentialBackoffGenerators';
/**
 * Options passed into {@link ExponentialBackoff}.
 */
export interface IExponentialBackoffOptions<S> {
    /**
     * Delay generator function to use. This package provides several of these/
     * Defaults to "decorrelatedJitterGenerator", a good default for most
     * scenarios (see the linked Polly issue).
     *
     * @see https://github.com/App-vNext/Polly/issues/530
     * @see https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
     */
    generator: GeneratorFn<S>;
    /**
     * Maximum delay, in milliseconds. Defaults to 30s.
     */
    maxDelay: number;
    /**
     * Backoff exponent. Defaults to 2.
     */
    exponent: number;
    /**
     * The initial, first delay of the backoff, in milliseconds.
     * Defaults to 128ms.
     */
    initialDelay: number;
}
export declare class ExponentialBackoff<S> implements IBackoffFactory<unknown> {
    private readonly options;
    /**
     * An implementation of exponential backoff.
     */
    constructor(options?: Partial<IExponentialBackoffOptions<S>>);
    next(): IBackoff<unknown>;
}
