export class TaskCancelledError extends Error {
    /**
     * Error thrown when a task is cancelled.
     */
    constructor(message = 'Operation cancelled') {
        super(message);
        this.message = message;
        this.isTaskCancelledError = true;
    }
}
//# sourceMappingURL=TaskCancelledError.js.map