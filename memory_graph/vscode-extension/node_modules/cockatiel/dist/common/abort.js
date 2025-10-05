"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deriveAbortController = exports.abortedSignal = exports.neverAbortedSignal = void 0;
const Event_1 = require("./Event");
exports.neverAbortedSignal = new AbortController().signal;
const cancelledSrc = new AbortController();
cancelledSrc.abort();
exports.abortedSignal = cancelledSrc.signal;
const noop = () => { };
/**
 * Creates a new AbortController that is aborted when the parent signal aborts.
 * @private
 */
const deriveAbortController = (signal) => {
    const ctrl = new AbortController();
    let dispose = noop;
    if (!signal) {
        return { ctrl, dispose };
    }
    if (signal.aborted) {
        ctrl.abort();
    }
    else {
        const abortEvt = (0, Event_1.onAbort)(signal);
        abortEvt.event(() => ctrl.abort());
        dispose = abortEvt.dispose;
    }
    return { ctrl, dispose };
};
exports.deriveAbortController = deriveAbortController;
//# sourceMappingURL=abort.js.map