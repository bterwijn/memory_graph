"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.isHydratingCircuitError = exports.isTaskCancelledError = exports.isIsolatedCircuitError = exports.isBulkheadRejectedError = exports.isBrokenCircuitError = void 0;
__exportStar(require("./BrokenCircuitError"), exports);
__exportStar(require("./BulkheadRejectedError"), exports);
__exportStar(require("./HydratingCircuitError"), exports);
__exportStar(require("./IsolatedCircuitError"), exports);
__exportStar(require("./TaskCancelledError"), exports);
const isBrokenCircuitError = (e) => !!e && e instanceof Error && 'isBrokenCircuitError' in e;
exports.isBrokenCircuitError = isBrokenCircuitError;
const isBulkheadRejectedError = (e) => !!e && e instanceof Error && 'isBulkheadRejectedError' in e;
exports.isBulkheadRejectedError = isBulkheadRejectedError;
const isIsolatedCircuitError = (e) => !!e && e instanceof Error && 'isBulkheadRejectedError' in e;
exports.isIsolatedCircuitError = isIsolatedCircuitError;
const isTaskCancelledError = (e) => !!e && e instanceof Error && 'isBulkheadRejectedError' in e;
exports.isTaskCancelledError = isTaskCancelledError;
const isHydratingCircuitError = (e) => !!e && e instanceof Error && 'isHydratingCircuitError' in e;
exports.isHydratingCircuitError = isHydratingCircuitError;
//# sourceMappingURL=Errors.js.map