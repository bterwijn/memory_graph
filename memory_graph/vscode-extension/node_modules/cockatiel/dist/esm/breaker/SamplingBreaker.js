import { CircuitState } from '../CircuitBreakerPolicy';
export class SamplingBreaker {
    /**
     * @inheritdoc
     */
    get state() {
        return {
            windows: this.windows,
            currentWindow: this.currentWindow,
            currentFailures: this.currentFailures,
            currentSuccesses: this.currentSuccesses,
        };
    }
    /**
     * @inheritdoc
     */
    set state(value) {
        Object.assign(this, value);
    }
    /**
     * SamplingBreaker breaks if more than `threshold` percentage of calls over the
     * last `samplingDuration`, so long as there's at least `minimumRps` (to avoid
     * opening unnecessarily under low RPS).
     */
    constructor({ threshold, duration: samplingDuration, minimumRps }) {
        this.windows = [];
        this.currentWindow = 0;
        this.currentFailures = 0;
        this.currentSuccesses = 0;
        if (threshold <= 0 || threshold >= 1) {
            throw new RangeError(`SamplingBreaker threshold should be between (0, 1), got ${threshold}`);
        }
        this.threshold = threshold;
        // at least 5 windows, max 1 second each:
        const windowCount = Math.max(5, Math.ceil(samplingDuration / 1000));
        for (let i = 0; i < windowCount; i++) {
            this.windows.push({ startedAt: 0, failures: 0, successes: 0 });
        }
        this.windowSize = Math.round(samplingDuration / windowCount);
        this.duration = this.windowSize * windowCount;
        if (minimumRps) {
            this.minimumRpms = minimumRps / 1000;
        }
        else {
            // for our rps guess, set it so at least 5 failures per second
            // are needed to open the circuit
            this.minimumRpms = 5 / (threshold * 1000);
        }
    }
    /**
     * @inheritdoc
     */
    success(state) {
        if (state === CircuitState.HalfOpen) {
            this.resetWindows();
        }
        this.push(true);
    }
    /**
     * @inheritdoc
     */
    failure(state) {
        this.push(false);
        if (state !== CircuitState.Closed) {
            return true;
        }
        const total = this.currentSuccesses + this.currentFailures;
        // If we don't have enough rps, then the circuit is open.
        // 1. `total / samplingDuration` gets rps
        // 2. We want `rpms < minimumRpms`
        // 3. Simplifies to `total < samplingDuration * minimumRps`
        if (total < this.duration * this.minimumRpms) {
            return false;
        }
        // If we're above threshold, open the circuit
        // 1. `failures / total > threshold`
        // 2. `failures > threshold * total`
        if (this.currentFailures > this.threshold * total) {
            return true;
        }
        return false;
    }
    resetWindows() {
        this.currentFailures = 0;
        this.currentSuccesses = 0;
        for (const window of this.windows) {
            window.failures = 0;
            window.successes = 0;
            window.startedAt = 0;
        }
    }
    rotateWindow(now) {
        const next = (this.currentWindow + 1) % this.windows.length;
        this.currentFailures -= this.windows[next].failures;
        this.currentSuccesses -= this.windows[next].successes;
        const window = (this.windows[next] = { failures: 0, successes: 0, startedAt: now });
        this.currentWindow = next;
        return window;
    }
    push(success) {
        const now = Date.now();
        // Get the current time period window, advance if necessary
        let window = this.windows[this.currentWindow];
        if (now - window.startedAt >= this.windowSize) {
            window = this.rotateWindow(now);
        }
        // Increment current counts
        if (success) {
            window.successes++;
            this.currentSuccesses++;
        }
        else {
            window.failures++;
            this.currentFailures++;
        }
    }
}
//# sourceMappingURL=SamplingBreaker.js.map