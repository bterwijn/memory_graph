"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BulkheadPolicy = void 0;
const abort_1 = require("./common/abort");
const defer_1 = require("./common/defer");
const Event_1 = require("./common/Event");
const Executor_1 = require("./common/Executor");
const BulkheadRejectedError_1 = require("./errors/BulkheadRejectedError");
const Errors_1 = require("./errors/Errors");
class BulkheadPolicy {
    /**
     * Returns the number of available execution slots at this point in time.
     */
    get executionSlots() {
        return this.capacity - this.active;
    }
    /**
     * Returns the number of queue slots at this point in time.
     */
    get queueSlots() {
        return this.queueCapacity - this.queue.length;
    }
    /**
     * Bulkhead limits concurrent requests made.
     */
    constructor(capacity, queueCapacity) {
        this.capacity = capacity;
        this.queueCapacity = queueCapacity;
        this.active = 0;
        this.queue = [];
        this.onRejectEmitter = new Event_1.EventEmitter();
        this.executor = new Executor_1.ExecuteWrapper();
        /**
         * @inheritdoc
         */
        this.onSuccess = this.executor.onSuccess;
        /**
         * @inheritdoc
         */
        this.onFailure = this.executor.onFailure;
        /**
         * Emitter that fires when an item is rejected from the bulkhead.
         */
        this.onReject = this.onRejectEmitter.addListener;
    }
    /**
     * Executes the given function.
     * @param fn Function to execute
     * @throws a {@link BulkheadRejectedException} if the bulkhead limits are exceeeded
     */
    async execute(fn, signal = abort_1.neverAbortedSignal) {
        if (signal.aborted) {
            throw new Errors_1.TaskCancelledError();
        }
        if (this.active < this.capacity) {
            this.active++;
            try {
                return await fn({ signal });
            }
            finally {
                this.active--;
                this.dequeue();
            }
        }
        if (this.queue.length < this.queueCapacity) {
            const { resolve, reject, promise } = (0, defer_1.defer)();
            this.queue.push({ signal, fn, resolve, reject });
            return promise;
        }
        this.onRejectEmitter.emit();
        throw new BulkheadRejectedError_1.BulkheadRejectedError(this.capacity, this.queueCapacity);
    }
    dequeue() {
        const item = this.queue.shift();
        if (!item) {
            return;
        }
        Promise.resolve()
            .then(() => this.execute(item.fn, item.signal))
            .then(item.resolve)
            .catch(item.reject);
    }
}
exports.BulkheadPolicy = BulkheadPolicy;
//# sourceMappingURL=BulkheadPolicy.js.map