"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConsecutiveBreaker = void 0;
class ConsecutiveBreaker {
    /**
     * ConsecutiveBreaker breaks if more than `threshold` exceptions are received
     * over a time period.
     */
    constructor(threshold) {
        this.threshold = threshold;
        /**
         * @inheritdoc
         */
        this.state = 0;
    }
    /**
     * @inheritdoc
     */
    success() {
        this.state = 0;
    }
    /**
     * @inheritdoc
     */
    failure() {
        return ++this.state >= this.threshold;
    }
}
exports.ConsecutiveBreaker = ConsecutiveBreaker;
//# sourceMappingURL=ConsecutiveBreaker.js.map