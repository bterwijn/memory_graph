export declare const defer: <T>() => {
    resolve: (value: T) => void;
    reject: (error: Error) => void;
    promise: Promise<T>;
};
