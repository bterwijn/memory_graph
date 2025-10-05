export class BulkheadRejectedError extends Error {
    constructor(executionSlots, queueSlots) {
        super(`Bulkhead capacity exceeded (0/${executionSlots} execution slots, 0/${queueSlots} available)`);
        this.isBulkheadRejectedError = true;
    }
}
//# sourceMappingURL=BulkheadRejectedError.js.map