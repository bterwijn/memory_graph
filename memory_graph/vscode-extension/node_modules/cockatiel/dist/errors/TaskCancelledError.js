"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskCancelledError = void 0;
class TaskCancelledError extends Error {
    /**
     * Error thrown when a task is cancelled.
     */
    constructor(message = 'Operation cancelled') {
        super(message);
        this.message = message;
        this.isTaskCancelledError = true;
    }
}
exports.TaskCancelledError = TaskCancelledError;
//# sourceMappingURL=TaskCancelledError.js.map