/// <reference types="node" />

/**
 * Creates a VSIX from the extension in the current working directory.
 * @public
 */
export declare function createVSIX(options?: IPackageOptions): Promise<any>;

/**
 * @deprecated prefer IPackageOptions instead
 * @public
 */
export declare type IBaseVSIXOptions = Pick<IPackageOptions, 'baseContentUrl' | 'baseImagesUrl' | 'githubBranch' | 'gitlabBranch' | 'useYarn' | 'target' | 'preRelease'>;

/**
 * @deprecated prefer IPackageOptions instead
 * @public
 */
export declare type ICreateVSIXOptions = Pick<IPackageOptions, 'cwd' | 'packagePath'> & IBaseVSIXOptions;

/**
 * Options for the `listFiles` function.
 * @public
 */
export declare interface IListFilesOptions {
    /**
     * The working directory of the extension. Defaults to `process.cwd()`.
     */
    cwd?: string;
    /**
     * The package manager to use. Defaults to `PackageManager.Npm`.
     */
    packageManager?: PackageManager;
    /**
     * A subset of the top level dependencies which should be included. The
     * default is `undefined` which include all dependencies, an empty array means
     * no dependencies will be included.
     */
    packagedDependencies?: string[];
    /**
     * The location of an alternative .vscodeignore file to be used.
     * The `.vscodeignore` file located at the root of the project will be taken
     * instead, if none is specified.
     */
    ignoreFile?: string;
}

/**
 * Options for the `createVSIX` function.
 * @public
 */
export declare interface IPackageOptions {
    /**
     * The destination of the packaged the VSIX.
     *
     * Defaults to `NAME-VERSION.vsix`.
     */
    readonly packagePath?: string;
    readonly version?: string;
    /**
     * Optional target the extension should run on.
     *
     * https://code.visualstudio.com/api/working-with-extensions/publishing-extension#platformspecific-extensions
     */
    readonly target?: string;
    /**
     * Ignore all files inside folders named as other targets. Only relevant when
     * `target` is set. For example, if `target` is `linux-x64` and there are
     * folders named `win32-x64`, `darwin-arm64` or `web`, the files inside
     * those folders will be ignored.
     *
     * @default false
     */
    readonly ignoreOtherTargetFolders?: boolean;
    readonly commitMessage?: string;
    readonly gitTagVersion?: boolean;
    readonly updatePackageJson?: boolean;
    /**
     * The location of the extension in the file system.
     *
     * Defaults to `process.cwd()`.
     */
    readonly cwd?: string;
    readonly readmePath?: string;
    readonly changelogPath?: string;
    /**
     * GitHub branch used to publish the package. Used to automatically infer
     * the base content and images URI.
     */
    readonly githubBranch?: string;
    /**
     * GitLab branch used to publish the package. Used to automatically infer
     * the base content and images URI.
     */
    readonly gitlabBranch?: string;
    readonly rewriteRelativeLinks?: boolean;
    /**
     * The base URL for links detected in Markdown files.
     */
    readonly baseContentUrl?: string;
    /**
     * The base URL for images detected in Markdown files.
     */
    readonly baseImagesUrl?: string;
    /**
     * Should use Yarn instead of NPM.
     */
    readonly useYarn?: boolean;
    readonly dependencyEntryPoints?: string[];
    readonly ignoreFile?: string;
    readonly gitHubIssueLinking?: boolean;
    readonly gitLabIssueLinking?: boolean;
    readonly dependencies?: boolean;
    /**
     * Mark this package as a pre-release
     */
    readonly preRelease?: boolean;
    readonly allowStarActivation?: boolean;
    readonly allowMissingRepository?: boolean;
    readonly allowUnusedFilesPattern?: boolean;
    readonly skipLicense?: boolean;
    readonly signTool?: string;
}

/**
 * Options for the `publish` function.
 * @public
 */
export declare interface IPublishOptions {
    readonly packagePath?: string[];
    readonly version?: string;
    readonly targets?: string[];
    readonly ignoreOtherTargetFolders?: boolean;
    readonly commitMessage?: string;
    readonly gitTagVersion?: boolean;
    readonly updatePackageJson?: boolean;
    /**
     * The location of the extension in the file system.
     *
     * Defaults to `process.cwd()`.
     */
    readonly cwd?: string;
    readonly readmePath?: string;
    readonly changelogPath?: string;
    readonly githubBranch?: string;
    readonly gitlabBranch?: string;
    /**
     * The base URL for links detected in Markdown files.
     */
    readonly baseContentUrl?: string;
    /**
     * The base URL for images detected in Markdown files.
     */
    readonly baseImagesUrl?: string;
    /**
     * Should use Yarn instead of NPM.
     */
    readonly useYarn?: boolean;
    readonly dependencyEntryPoints?: string[];
    readonly ignoreFile?: string;
    /**
     * The Personal Access Token to use.
     *
     * Defaults to the stored one.
     */
    readonly pat?: string;
    readonly azureCredential?: boolean;
    readonly allowProposedApi?: boolean;
    readonly noVerify?: boolean;
    readonly allowProposedApis?: string[];
    readonly allowAllProposedApis?: boolean;
    readonly dependencies?: boolean;
    readonly preRelease?: boolean;
    readonly allowStarActivation?: boolean;
    readonly allowMissingRepository?: boolean;
    readonly allowUnusedFilesPattern?: boolean;
    readonly skipDuplicate?: boolean;
    readonly skipLicense?: boolean;
    readonly sigzipPath?: string[];
    readonly manifestPath?: string[];
    readonly signaturePath?: string[];
    readonly signTool?: string;
}

/**
 * Options for the `publishVSIX` function.
 * @public
 */
export declare type IPublishVSIXOptions = IPublishOptions & Pick<IPackageOptions, 'target'>;

/**
 * Lists the files included in the extension's package.
 * @public
 */
export declare function listFiles(options?: IListFilesOptions): Promise<string[]>;

/**
 * The supported list of package managers.
 * @public
 */
export declare enum PackageManager {
    Npm = 0,
    Yarn = 1,
    None = 2
}

/**
 * Publishes the extension in the current working directory.
 * @public
 */
export declare function publish(options?: IPublishOptions): Promise<any>;

/**
 * Publishes a pre-build VSIX.
 * @public
 */
export declare function publishVSIX(packagePath: string | string[], options?: IPublishVSIXOptions): Promise<any>;

export { }
