"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IterableBackoff = void 0;
class IterableBackoff {
    /**
     * Backoff that returns a number from an iterable.
     */
    constructor(durations) {
        this.durations = durations;
    }
    /**
     * @inheritdoc
     */
    next(_context) {
        return instance(this.durations, 0);
    }
}
exports.IterableBackoff = IterableBackoff;
const instance = (durations, index) => ({
    duration: durations[index],
    next() {
        return index === durations.length - 1 ? this : instance(durations, index + 1);
    },
});
//# sourceMappingURL=IterableBackoff.js.map