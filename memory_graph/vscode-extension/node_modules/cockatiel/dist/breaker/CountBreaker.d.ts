import { CircuitState } from '../CircuitBreakerPolicy';
import { IBreaker } from './Breaker';
export interface ICountBreakerOptions {
    /**
     * Percentage (from 0 to 1) of requests that need to fail before we'll
     * open the circuit.
     */
    threshold: number;
    /**
     * Size of the count based sliding window.
     */
    size: number;
    /**
     * Minimum number of calls needed to (potentially) open the circuit.
     * Useful to avoid unnecessarily tripping when there are only few samples yet.
     * Defaults to {@link ICountBreakerOptions.size}.
     */
    minimumNumberOfCalls?: number;
}
export declare class CountBreaker implements IBreaker {
    private readonly threshold;
    private readonly minimumNumberOfCalls;
    /**
     * The samples in the sliding window. `true` means "success", `false` means
     * "failure" and `null` means that there is no sample yet.
     */
    private samples;
    private successes;
    private failures;
    private currentSample;
    /**
     * @inheritdoc
     */
    get state(): unknown;
    /**
     * @inheritdoc
     */
    set state(value: unknown);
    /**
     * CountBreaker breaks if more than `threshold` percentage of the last `size`
     * calls failed, so long as at least `minimumNumberOfCalls` calls have been
     * performed (to avoid opening unnecessarily if there are only few samples
     * in the sliding window yet).
     */
    constructor({ threshold, size, minimumNumberOfCalls }: ICountBreakerOptions);
    /**
     * @inheritdoc
     */
    success(state: CircuitState): void;
    /**
     * @inheritdoc
     */
    failure(state: CircuitState): boolean;
    private reset;
    private sample;
}
