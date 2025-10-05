"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Event_1 = require("./Event");
const emitter0 = new Event_1.EventEmitter();
const emitter1 = new Event_1.EventEmitter();
emitter1.addListener(() => undefined);
const emitter3 = new Event_1.EventEmitter();
emitter3.addListener(() => undefined);
emitter3.addListener(() => undefined);
emitter3.addListener(() => undefined);
bench('0 listener', () => emitter0.emit(true));
bench('1 listener', () => emitter1.emit(true));
bench('3 listener', () => emitter3.emit(true));
//# sourceMappingURL=Executor.bench.js.map