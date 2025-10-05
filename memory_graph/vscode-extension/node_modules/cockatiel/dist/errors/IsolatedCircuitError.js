"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IsolatedCircuitError = void 0;
const BrokenCircuitError_1 = require("./BrokenCircuitError");
class IsolatedCircuitError extends BrokenCircuitError_1.BrokenCircuitError {
    /**
     * Exception thrown from {@link CircuitBreakerPolicy.execute} when the
     * circuit breaker is open.
     */
    constructor() {
        super(`Execution prevented because the circuit breaker is open`);
        this.isIsolatedCircuitError = true;
    }
}
exports.IsolatedCircuitError = IsolatedCircuitError;
//# sourceMappingURL=IsolatedCircuitError.js.map