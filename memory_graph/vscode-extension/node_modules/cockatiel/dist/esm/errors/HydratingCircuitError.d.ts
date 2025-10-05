export declare class HydratingCircuitError extends Error {
    readonly isHydratingCircuitError = true;
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor(message?: string);
}
