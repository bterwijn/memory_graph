"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.HydratingCircuitError = void 0;
class HydratingCircuitError extends Error {
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor(message = 'Execution prevented because the circuit breaker is open') {
        super(message);
        this.isHydratingCircuitError = true;
    }
}
exports.HydratingCircuitError = HydratingCircuitError;
//# sourceMappingURL=HydratingCircuitError.js.map