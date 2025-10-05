"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CircuitBreakerPolicy = exports.CircuitState = void 0;
const Backoff_1 = require("./backoff/Backoff");
const abort_1 = require("./common/abort");
const Event_1 = require("./common/Event");
const Executor_1 = require("./common/Executor");
const Errors_1 = require("./errors/Errors");
const IsolatedCircuitError_1 = require("./errors/IsolatedCircuitError");
var CircuitState;
(function (CircuitState) {
    /**
     * Normal operation. Execution of actions allowed.
     */
    CircuitState[CircuitState["Closed"] = 0] = "Closed";
    /**
     * The automated controller has opened the circuit. Execution of actions blocked.
     */
    CircuitState[CircuitState["Open"] = 1] = "Open";
    /**
     * Recovering from open state, after the automated break duration has
     * expired. Execution of actions permitted. Success of subsequent action/s
     * controls onward transition to Open or Closed state.
     */
    CircuitState[CircuitState["HalfOpen"] = 2] = "HalfOpen";
    /**
     * Circuit held manually in an open state. Execution of actions blocked.
     */
    CircuitState[CircuitState["Isolated"] = 3] = "Isolated";
})(CircuitState || (exports.CircuitState = CircuitState = {}));
class CircuitBreakerPolicy {
    /**
     * Gets the current circuit breaker state.
     */
    get state() {
        return this.innerState.value;
    }
    /**
     * Gets the last reason the circuit breaker failed.
     */
    get lastFailure() {
        return this.innerLastFailure;
    }
    constructor(options, executor) {
        this.options = options;
        this.executor = executor;
        this.breakEmitter = new Event_1.EventEmitter();
        this.resetEmitter = new Event_1.EventEmitter();
        this.halfOpenEmitter = new Event_1.EventEmitter();
        this.stateChangeEmitter = new Event_1.EventEmitter();
        this.innerState = { value: CircuitState.Closed };
        /**
         * Event emitted when the circuit breaker opens.
         */
        this.onBreak = this.breakEmitter.addListener;
        /**
         * Event emitted when the circuit breaker resets.
         */
        this.onReset = this.resetEmitter.addListener;
        /**
         * Event emitted when the circuit breaker is half open (running a test call).
         * Either `onBreak` on `onReset` will subsequently fire.
         */
        this.onHalfOpen = this.halfOpenEmitter.addListener;
        /**
         * Fired whenever the circuit breaker state changes.
         */
        this.onStateChange = this.stateChangeEmitter.addListener;
        /**
         * @inheritdoc
         */
        this.onSuccess = this.executor.onSuccess;
        /**
         * @inheritdoc
         */
        this.onFailure = this.executor.onFailure;
        this.halfOpenAfterBackoffFactory =
            typeof options.halfOpenAfter === 'number'
                ? new Backoff_1.ConstantBackoff(options.halfOpenAfter)
                : options.halfOpenAfter;
        if (options.initialState) {
            const initialState = options.initialState;
            this.innerState = initialState.ownState;
            this.options.breaker.state = initialState.breakerState;
            if (this.innerState.value === CircuitState.Open ||
                this.innerState.value === CircuitState.HalfOpen) {
                this.innerLastFailure = { error: new Errors_1.HydratingCircuitError() };
                let backoff = this.halfOpenAfterBackoffFactory.next({
                    attempt: 1,
                    result: this.innerLastFailure,
                    signal: abort_1.neverAbortedSignal,
                });
                for (let i = 2; i <= this.innerState.attemptNo; i++) {
                    backoff = backoff.next({
                        attempt: i,
                        result: this.innerLastFailure,
                        signal: abort_1.neverAbortedSignal,
                    });
                }
                this.innerState.backoff = backoff;
            }
        }
    }
    /**
     * Manually holds open the circuit breaker.
     * @returns A handle that keeps the breaker open until `.dispose()` is called.
     */
    isolate() {
        if (this.innerState.value !== CircuitState.Isolated) {
            this.innerState = { value: CircuitState.Isolated, counters: 0 };
            this.breakEmitter.emit({ isolated: true });
            this.stateChangeEmitter.emit(CircuitState.Isolated);
        }
        this.innerState.counters++;
        let disposed = false;
        return {
            dispose: () => {
                if (disposed) {
                    return;
                }
                disposed = true;
                if (this.innerState.value === CircuitState.Isolated && !--this.innerState.counters) {
                    this.innerState = { value: CircuitState.Closed };
                    this.resetEmitter.emit();
                    this.stateChangeEmitter.emit(CircuitState.Closed);
                }
            },
        };
    }
    /**
     * Executes the given function.
     * @param fn Function to run
     * @throws a {@link BrokenCircuitError} if the circuit is open
     * @throws a {@link IsolatedCircuitError} if the circuit is held
     * open via {@link CircuitBreakerPolicy.isolate}
     * @returns a Promise that resolves or rejects with the function results.
     */
    async execute(fn, signal = abort_1.neverAbortedSignal) {
        const state = this.innerState;
        switch (state.value) {
            case CircuitState.Closed:
                const result = await this.executor.invoke(fn, { signal });
                if ('success' in result) {
                    this.options.breaker.success(state.value);
                }
                else {
                    this.innerLastFailure = result;
                    if (this.options.breaker.failure(state.value)) {
                        this.open(result, signal);
                    }
                }
                return (0, Executor_1.returnOrThrow)(result);
            case CircuitState.HalfOpen:
                await state.test.catch(() => undefined);
                if (this.state === CircuitState.Closed && signal.aborted) {
                    throw new Errors_1.TaskCancelledError();
                }
                return this.execute(fn);
            case CircuitState.Open:
                if (Date.now() - state.openedAt < state.backoff.duration) {
                    throw new Errors_1.BrokenCircuitError();
                }
                const test = this.halfOpen(fn, signal);
                this.innerState = {
                    value: CircuitState.HalfOpen,
                    test,
                    backoff: state.backoff,
                    attemptNo: state.attemptNo + 1,
                };
                this.stateChangeEmitter.emit(CircuitState.HalfOpen);
                return test;
            case CircuitState.Isolated:
                throw new IsolatedCircuitError_1.IsolatedCircuitError();
            default:
                throw new Error(`Unexpected circuit state ${state}`);
        }
    }
    /**
     * Captures circuit breaker state that can later be used to recreate the
     * breaker by passing `state` to the `circuitBreaker` function. This is
     * useful in cases like serverless functions where you may want to keep
     * the breaker state across multiple executions.
     */
    toJSON() {
        const state = this.innerState;
        let ownState;
        if (state.value === CircuitState.HalfOpen) {
            ownState = {
                value: CircuitState.Open,
                openedAt: 0,
                attemptNo: state.attemptNo,
            };
        }
        else if (state.value === CircuitState.Open) {
            ownState = {
                value: CircuitState.Open,
                openedAt: state.openedAt,
                attemptNo: state.attemptNo,
            };
        }
        else {
            ownState = state;
        }
        return { ownState, breakerState: this.options.breaker.state };
    }
    async halfOpen(fn, signal) {
        this.halfOpenEmitter.emit();
        try {
            const result = await this.executor.invoke(fn, { signal });
            if ('success' in result) {
                this.options.breaker.success(CircuitState.HalfOpen);
                this.close();
            }
            else {
                this.innerLastFailure = result;
                this.options.breaker.failure(CircuitState.HalfOpen);
                this.open(result, signal);
            }
            return (0, Executor_1.returnOrThrow)(result);
        }
        catch (err) {
            // It's an error, but not one the circuit is meant to retry, so
            // for our purposes it's a success. Task failed successfully!
            this.close();
            throw err;
        }
    }
    open(reason, signal) {
        if (this.state === CircuitState.Isolated || this.state === CircuitState.Open) {
            return;
        }
        const attemptNo = this.innerState.value === CircuitState.HalfOpen ? this.innerState.attemptNo : 1;
        const context = { attempt: attemptNo, result: reason, signal };
        const backoff = this.innerState.value === CircuitState.HalfOpen
            ? this.innerState.backoff.next(context)
            : this.halfOpenAfterBackoffFactory.next(context);
        this.innerState = { value: CircuitState.Open, openedAt: Date.now(), backoff, attemptNo };
        this.breakEmitter.emit(reason);
        this.stateChangeEmitter.emit(CircuitState.Open);
    }
    close() {
        if (this.state === CircuitState.HalfOpen) {
            this.innerState = { value: CircuitState.Closed };
            this.resetEmitter.emit();
            this.stateChangeEmitter.emit(CircuitState.Closed);
        }
    }
}
exports.CircuitBreakerPolicy = CircuitBreakerPolicy;
//# sourceMappingURL=CircuitBreakerPolicy.js.map