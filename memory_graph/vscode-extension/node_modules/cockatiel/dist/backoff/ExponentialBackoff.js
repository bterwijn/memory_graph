"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExponentialBackoff = void 0;
const ExponentialBackoffGenerators_1 = require("./ExponentialBackoffGenerators");
const defaultOptions = {
    generator: ExponentialBackoffGenerators_1.decorrelatedJitterGenerator,
    maxDelay: 30000,
    exponent: 2,
    initialDelay: 128,
};
class ExponentialBackoff {
    /**
     * An implementation of exponential backoff.
     */
    constructor(options) {
        this.options = options ? { ...defaultOptions, ...options } : defaultOptions;
    }
    next() {
        return instance(this.options).next(undefined);
    }
}
exports.ExponentialBackoff = ExponentialBackoff;
/**
 * An implementation of exponential backoff.
 */
const instance = (options, state, delay = 0, attempt = -1) => ({
    duration: delay,
    next() {
        const [nextDelay, nextState] = options.generator(state, options);
        return instance(options, nextState, nextDelay, attempt + 1);
    },
});
//# sourceMappingURL=ExponentialBackoff.js.map