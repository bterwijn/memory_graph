export declare class BulkheadRejectedError extends Error {
    readonly isBulkheadRejectedError = true;
    constructor(executionSlots: number, queueSlots: number);
}
