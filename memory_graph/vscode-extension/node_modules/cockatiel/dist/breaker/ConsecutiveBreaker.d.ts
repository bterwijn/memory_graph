import { IBreaker } from './Breaker';
export declare class ConsecutiveBreaker implements IBreaker {
    private readonly threshold;
    /**
     * @inheritdoc
     */
    state: number;
    /**
     * ConsecutiveBreaker breaks if more than `threshold` exceptions are received
     * over a time period.
     */
    constructor(threshold: number);
    /**
     * @inheritdoc
     */
    success(): void;
    /**
     * @inheritdoc
     */
    failure(): boolean;
}
