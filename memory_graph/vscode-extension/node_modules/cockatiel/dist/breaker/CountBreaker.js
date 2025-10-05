"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CountBreaker = void 0;
const CircuitBreakerPolicy_1 = require("../CircuitBreakerPolicy");
class CountBreaker {
    /**
     * @inheritdoc
     */
    get state() {
        return {
            samples: this.samples,
            currentSample: this.currentSample,
            failures: this.failures,
            successes: this.successes,
        };
    }
    /**
     * @inheritdoc
     */
    set state(value) {
        Object.assign(this, value);
    }
    /**
     * CountBreaker breaks if more than `threshold` percentage of the last `size`
     * calls failed, so long as at least `minimumNumberOfCalls` calls have been
     * performed (to avoid opening unnecessarily if there are only few samples
     * in the sliding window yet).
     */
    constructor({ threshold, size, minimumNumberOfCalls = size }) {
        this.successes = 0;
        this.failures = 0;
        this.currentSample = 0;
        if (threshold <= 0 || threshold >= 1) {
            throw new RangeError(`CountBreaker threshold should be between (0, 1), got ${threshold}`);
        }
        if (!Number.isSafeInteger(size) || size < 1) {
            throw new RangeError(`CountBreaker size should be a positive integer, got ${size}`);
        }
        if (!Number.isSafeInteger(minimumNumberOfCalls) ||
            minimumNumberOfCalls < 1 ||
            minimumNumberOfCalls > size) {
            throw new RangeError(`CountBreaker size should be an integer between (1, size), got ${minimumNumberOfCalls}`);
        }
        this.threshold = threshold;
        this.minimumNumberOfCalls = minimumNumberOfCalls;
        this.samples = Array.from({ length: size }, () => null);
    }
    /**
     * @inheritdoc
     */
    success(state) {
        if (state === CircuitBreakerPolicy_1.CircuitState.HalfOpen) {
            this.reset();
        }
        this.sample(true);
    }
    /**
     * @inheritdoc
     */
    failure(state) {
        this.sample(false);
        if (state !== CircuitBreakerPolicy_1.CircuitState.Closed) {
            return true;
        }
        const total = this.successes + this.failures;
        if (total < this.minimumNumberOfCalls) {
            return false;
        }
        if (this.failures > this.threshold * total) {
            return true;
        }
        return false;
    }
    reset() {
        this.samples.fill(null);
        this.successes = 0;
        this.failures = 0;
    }
    sample(success) {
        const current = this.samples[this.currentSample];
        if (current === true) {
            this.successes--;
        }
        else if (current === false) {
            this.failures--;
        }
        this.samples[this.currentSample] = success;
        if (success) {
            this.successes++;
        }
        else {
            this.failures++;
        }
        this.currentSample = (this.currentSample + 1) % this.samples.length;
    }
}
exports.CountBreaker = CountBreaker;
//# sourceMappingURL=CountBreaker.js.map