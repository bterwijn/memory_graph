export class IterableBackoff {
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
const instance = (durations, index) => ({
    duration: durations[index],
    next() {
        return index === durations.length - 1 ? this : instance(durations, index + 1);
    },
});
//# sourceMappingURL=IterableBackoff.js.map