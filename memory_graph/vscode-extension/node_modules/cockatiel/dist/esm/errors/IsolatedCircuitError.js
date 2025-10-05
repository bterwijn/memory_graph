import { BrokenCircuitError } from './BrokenCircuitError';
export class IsolatedCircuitError extends BrokenCircuitError {
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor() {
        super(`Execution prevented because the circuit breaker is open`);
        this.isIsolatedCircuitError = true;
    }
}
//# sourceMappingURL=IsolatedCircuitError.js.map