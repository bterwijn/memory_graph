"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DelegateBackoff = void 0;
class DelegateBackoff {
    /**
     * Backoff that delegates to a user-provided function. The function takes
     * the backoff context, and can optionally take (and return) a state value
     * that will be passed into subsequent backoff requests.
     */
    constructor(fn) {
        this.fn = fn;
    }
    /**
     * @inheritdoc
     */
    next(context) {
        return instance(this.fn).next(context);
    }
}
exports.DelegateBackoff = DelegateBackoff;
const instance = (fn, state, current = 0) => ({
    duration: current,
    next(context) {
        const result = fn(context, state);
        return typeof result === 'number'
            ? instance(fn, state, result)
            : instance(fn, result.state, result.delay);
    },
});
//# sourceMappingURL=DelegateBackoff.js.map