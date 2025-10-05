export class ConstantBackoff {
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
const instance = (interval) => ({
    duration: interval,
    next() {
        return this;
    },
});
//# sourceMappingURL=ConstantBackoff.js.map