"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BrokenCircuitError = void 0;
class BrokenCircuitError extends Error {
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor(message = 'Execution prevented because the circuit breaker is open') {
        super(message);
        this.isBrokenCircuitError = true;
    }
}
exports.BrokenCircuitError = BrokenCircuitError;
//# sourceMappingURL=BrokenCircuitError.js.map