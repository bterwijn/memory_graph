export declare class TaskCancelledError extends Error {
    readonly message: string;
    readonly isTaskCancelledError = true;
    /**
     * Error thrown when a task is cancelled.
     */
    constructor(message?: string);
}
