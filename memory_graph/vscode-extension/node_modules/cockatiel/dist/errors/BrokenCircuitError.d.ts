export declare class BrokenCircuitError extends Error {
    readonly isBrokenCircuitError = true;
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor(message?: string);
}
