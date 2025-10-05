"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConstantBackoff = void 0;
class ConstantBackoff {
    /**
     * Backoff that returns a constant interval.
     */
    constructor(interval) {
        this.interval = interval;
    }
    /**
     * @inheritdoc
     */
    next() {
        return instance(this.interval);
    }
}
exports.ConstantBackoff = ConstantBackoff;
const instance = (interval) => ({
    duration: interval,
    next() {
        return this;
    },
});
//# sourceMappingURL=ConstantBackoff.js.map