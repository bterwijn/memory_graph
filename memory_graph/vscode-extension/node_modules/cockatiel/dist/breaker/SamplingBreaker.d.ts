import { CircuitState } from '../CircuitBreakerPolicy';
import { IBreaker } from './Breaker';
export interface ISamplingBreakerOptions {
    /**
     * Percentage (from 0 to 1) of requests that need to fail before we'll
     * open the circuit.
     */
    threshold: number;
    /**
     * Length of time over which to sample.
     */
    duration: number;
    /**
     * Minimum number of RPS needed to be able to (potentially) open the circuit.
     * Useful to avoid unnecessarily tripping under low load.
     */
    minimumRps?: number;
}
export declare class SamplingBreaker implements IBreaker {
    private readonly threshold;
    private readonly minimumRpms;
    private readonly duration;
    private readonly windowSize;
    private windows;
    private currentWindow;
    private currentFailures;
    private currentSuccesses;
    /**
     * @inheritdoc
     */
    get state(): unknown;
    /**
     * @inheritdoc
     */
    set state(value: unknown);
    /**
     * SamplingBreaker breaks if more than `threshold` percentage of calls over the
     * last `samplingDuration`, so long as there's at least `minimumRps` (to avoid
     * opening unnecessarily under low RPS).
     */
    constructor({ threshold, duration: samplingDuration, minimumRps }: ISamplingBreakerOptions);
    /**
     * @inheritdoc
     */
    success(state: CircuitState): void;
    /**
     * @inheritdoc
     */
    failure(state: CircuitState): boolean;
    private resetWindows;
    private rotateWindow;
    private push;
}
