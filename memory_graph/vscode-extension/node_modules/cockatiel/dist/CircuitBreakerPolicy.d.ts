import { IBackoffFactory } from './backoff/Backoff';
import { IBreaker } from './breaker/Breaker';
import { ExecuteWrapper } from './common/Executor';
import { FailureReason, IDefaultPolicyContext, IPolicy } from './Policy';
export declare enum CircuitState {
    /**
     * Normal operation. Execution of actions allowed.
     */
    Closed = 0,
    /**
     * The automated controller has opened the circuit. Execution of actions blocked.
     */
    Open = 1,
    /**
     * Recovering from open state, after the automated break duration has
     * expired. Execution of actions permitted. Success of subsequent action/s
     * controls onward transition to Open or Closed state.
     */
    HalfOpen = 2,
    /**
     * Circuit held manually in an open state. Execution of actions blocked.
     */
    Isolated = 3
}
/**
 * Context passed into halfOpenAfter backoff delegate.
 */
export interface IHalfOpenAfterBackoffContext extends IDefaultPolicyContext {
    /**
     * The consecutive number of times the circuit has entered the
     * {@link CircuitState.Open} state.
     */
    attempt: number;
    /**
     * The result of the last method call that caused the circuit to enter the
     * {@link CircuitState.Open} state. Either a thrown error, or a value that we
     * determined should open the circuit.
     */
    result: FailureReason<unknown>;
}
export interface ICircuitBreakerOptions {
    breaker: IBreaker;
    /**
     * When to (potentially) enter the {@link CircuitState.HalfOpen} state from
     * the {@link CircuitState.Open} state. Either a duration in milliseconds or a
     * backoff factory.
     */
    halfOpenAfter: number | IBackoffFactory<IHalfOpenAfterBackoffContext>;
    /**
     * Initial state from a previous call to {@link CircuitBreakerPolicy.toJSON}.
     */
    initialState?: unknown;
}
export declare class CircuitBreakerPolicy implements IPolicy {
    private readonly options;
    private readonly executor;
    readonly _altReturn: never;
    private readonly breakEmitter;
    private readonly resetEmitter;
    private readonly halfOpenEmitter;
    private readonly stateChangeEmitter;
    private readonly halfOpenAfterBackoffFactory;
    private innerLastFailure?;
    private innerState;
    /**
     * Event emitted when the circuit breaker opens.
     */
    readonly onBreak: import("./common/Event").Event<FailureReason<unknown> | {
        isolated: true;
    }>;
    /**
     * Event emitted when the circuit breaker resets.
     */
    readonly onReset: import("./common/Event").Event<void>;
    /**
     * Event emitted when the circuit breaker is half open (running a test call).
     * Either `onBreak` on `onReset` will subsequently fire.
     */
    readonly onHalfOpen: import("./common/Event").Event<void>;
    /**
     * Fired whenever the circuit breaker state changes.
     */
    readonly onStateChange: import("./common/Event").Event<CircuitState>;
    /**
     * @inheritdoc
     */
    readonly onSuccess: import("./common/Event").Event<import("./Policy").ISuccessEvent>;
    /**
     * @inheritdoc
     */
    readonly onFailure: import("./common/Event").Event<import("./Policy").IFailureEvent>;
    /**
     * Gets the current circuit breaker state.
     */
    get state(): CircuitState;
    /**
     * Gets the last reason the circuit breaker failed.
     */
    get lastFailure(): FailureReason<unknown> | undefined;
    constructor(options: ICircuitBreakerOptions, executor: ExecuteWrapper);
    /**
     * Manually holds open the circuit breaker.
     * @returns A handle that keeps the breaker open until `.dispose()` is called.
     */
    isolate(): {
        dispose: () => void;
    };
    /**
     * Executes the given function.
     * @param fn Function to run
     * @throws a {@link BrokenCircuitError} if the circuit is open
     * @throws a {@link IsolatedCircuitError} if the circuit is held
     * open via {@link CircuitBreakerPolicy.isolate}
     * @returns a Promise that resolves or rejects with the function results.
     */
    execute<T>(fn: (context: IDefaultPolicyContext) => PromiseLike<T> | T, signal?: AbortSignal): Promise<T>;
    /**
     * Captures circuit breaker state that can later be used to recreate the
     * breaker by passing `state` to the `circuitBreaker` function. This is
     * useful in cases like serverless functions where you may want to keep
     * the breaker state across multiple executions.
     */
    toJSON(): unknown;
    private halfOpen;
    private open;
    private close;
}
