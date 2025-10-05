import { IExponentialBackoffOptions } from '../backoff/ExponentialBackoff';
/**
 * Function used to get the next delay.
 */
export type GeneratorFn<S> = (state: S | undefined, options: IExponentialBackoffOptions<S>) => [number, S];
/**
 * Generator that creates a backoff with no jitter.
 */
export declare const noJitterGenerator: GeneratorFn<number>;
/**
 * Generator that randomizes an exponential backoff between [0, delay).
 */
export declare const fullJitterGenerator: GeneratorFn<number>;
/**
 * Generator that randomizes an exponential backoff between [0, delay).
 */
export declare const halfJitterGenerator: GeneratorFn<number>;
/**
 * Decorrelated jitter. This should be considered the optimal Jitter stategy
 * for most scenarios, as battle-tested in Polly.
 *
 * @see https://github.com/App-vNext/Polly/issues/530
 * @see https://github.com/Polly-Contrib/Polly.Contrib.WaitAndRetry/blob/24cb116a2a320e82b01f57e13bfeaeff2725ccbf/src/Polly.Contrib.WaitAndRetry/Backoff.DecorrelatedJitterV2.cs
 */
export declare const decorrelatedJitterGenerator: GeneratorFn<[number, number]>;
