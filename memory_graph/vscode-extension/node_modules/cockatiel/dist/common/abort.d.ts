import { IDisposable } from './Event';
export declare const neverAbortedSignal: AbortSignal;
export declare const abortedSignal: AbortSignal;
/**
 * Creates a new AbortController that is aborted when the parent signal aborts.
 * @private
 */
export declare const deriveAbortController: (signal?: AbortSignal) => {
    ctrl: AbortController;
} & IDisposable;
