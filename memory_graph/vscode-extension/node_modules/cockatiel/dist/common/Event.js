"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MemorizingEventEmitter = exports.EventEmitter = exports.onAbort = exports.Event = exports.noopDisposable = void 0;
const TaskCancelledError_1 = require("../errors/TaskCancelledError");
exports.noopDisposable = { dispose: () => undefined };
var Event;
(function (Event) {
    /**
     * Adds a handler that handles one event on the emitter.
     */
    Event.once = (event, listener) => {
        let syncDispose = false;
        let disposable;
        disposable = event(value => {
            listener(value);
            if (disposable) {
                disposable.dispose();
            }
            else {
                syncDispose = true; // callback can fire before disposable is returned
            }
        });
        if (syncDispose) {
            disposable.dispose();
            return exports.noopDisposable; // no reason to keep the ref around
        }
        return disposable;
    };
    /**
     * Returns a promise that resolves when the event fires, or when cancellation
     * is requested, whichever happens first.
     */
    Event.toPromise = (event, signal) => {
        if (!signal) {
            return new Promise(resolve => Event.once(event, resolve));
        }
        if (signal.aborted) {
            return Promise.reject(new TaskCancelledError_1.TaskCancelledError());
        }
        const toDispose = [];
        return new Promise((resolve, reject) => {
            const abortEvt = (0, exports.onAbort)(signal);
            toDispose.push(abortEvt);
            toDispose.push(abortEvt.event(() => {
                reject(new TaskCancelledError_1.TaskCancelledError());
            }));
            toDispose.push(Event.once(event, data => {
                resolve(data);
            }));
        }).finally(() => {
            for (const d of toDispose) {
                d.dispose();
            }
        });
    };
})(Event || (exports.Event = Event = {}));
/** Creates an Event that fires when the signal is aborted. */
const onAbort = (signal) => {
    const evt = new OneShotEvent();
    if (signal.aborted) {
        evt.emit();
        return { event: evt.addListener, dispose: () => { } };
    }
    const dispose = () => signal.removeEventListener('abort', l);
    // @types/node is currently missing the event types on AbortSignal
    const l = () => {
        evt.emit();
        dispose();
    };
    signal.addEventListener('abort', l);
    return { event: evt.addListener, dispose };
};
exports.onAbort = onAbort;
/**
 * Base event emitter. Calls listeners when data is emitted.
 */
class EventEmitter {
    constructor() {
        /**
         * Event<T> function.
         */
        this.addListener = listener => this.addListenerInner(listener);
    }
    /**
     * Gets the number of event listeners.
     */
    get size() {
        if (!this.listeners) {
            return 0;
        }
        else if (typeof this.listeners === 'function') {
            return 1;
        }
        else {
            return this.listeners.length;
        }
    }
    /**
     * Emits event data.
     */
    emit(value) {
        if (!this.listeners) {
            // no-op
        }
        else if (typeof this.listeners === 'function') {
            this.listeners(value);
        }
        else {
            for (const listener of this.listeners) {
                listener(value);
            }
        }
    }
    addListenerInner(listener) {
        if (!this.listeners) {
            this.listeners = listener;
        }
        else if (typeof this.listeners === 'function') {
            this.listeners = [this.listeners, listener];
        }
        else {
            this.listeners.push(listener);
        }
        return { dispose: () => this.removeListener(listener) };
    }
    removeListener(listener) {
        if (!this.listeners) {
            return;
        }
        if (typeof this.listeners === 'function') {
            if (this.listeners === listener) {
                this.listeners = undefined;
            }
            return;
        }
        const index = this.listeners.indexOf(listener);
        if (index === -1) {
            return;
        }
        if (this.listeners.length === 2) {
            this.listeners = index === 0 ? this.listeners[1] : this.listeners[0];
        }
        else {
            this.listeners = this.listeners.slice(0, index).concat(this.listeners.slice(index + 1));
        }
    }
}
exports.EventEmitter = EventEmitter;
/**
 * An event emitter that memorizes and instantly re-emits its last value
 * to attached listeners.
 */
class MemorizingEventEmitter extends EventEmitter {
    constructor() {
        super(...arguments);
        /**
         * @inheritdoc
         */
        this.addListener = listener => {
            const disposable = this.addListenerInner(listener);
            if (this.lastValue) {
                listener(this.lastValue.value);
            }
            return disposable;
        };
    }
    /**
     * Gets whether this emitter has yet emitted any event.
     */
    get hasEmitted() {
        return !!this.lastValue;
    }
    /**
     * @inheritdoc
     */
    emit(value) {
        this.lastValue = { value };
        super.emit(value);
    }
}
exports.MemorizingEventEmitter = MemorizingEventEmitter;
/**
 * An event emitter that fires a value once and removes all
 * listeners automatically after doing so.
 */
class OneShotEvent extends EventEmitter {
    constructor() {
        super(...arguments);
        /**
         * @inheritdoc
         */
        this.addListener = listener => {
            if (this.lastValue) {
                listener(this.lastValue.value);
                return exports.noopDisposable;
            }
            else {
                return this.addListenerInner(listener);
            }
        };
    }
    /**
     * @inheritdoc
     */
    emit(value) {
        this.lastValue = { value };
        super.emit(value);
        this.listeners = undefined;
    }
}
//# sourceMappingURL=Event.js.map