import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface PythonEnvironment {
    pythonPath: string;
    hasMemoryGraph: boolean;
    hasGraphviz: boolean;
    version: string;
}

/**
 * Get the Python interpreter path
 * First tries user setting, then VS Code's Python extension, then system default
 */
export async function getPythonPath(): Promise<string> {
    // 1. Check user settings
    const config = vscode.workspace.getConfiguration('memoryGraph');
    const userPythonPath = config.get<string>('pythonPath');
    if (userPythonPath) {
        return userPythonPath;
    }

    // 2. Try to get from Python extension
    try {
        const pythonExtension = vscode.extensions.getExtension('ms-python.python');
        if (pythonExtension) {
            if (!pythonExtension.isActive) {
                await pythonExtension.activate();
            }
            const pythonPath = pythonExtension.exports?.settings?.getExecutionDetails?.()?.execCommand?.[0];
            if (pythonPath) {
                return pythonPath;
            }
        }
    } catch (error) {
        console.log('Could not get Python from extension:', error);
    }

    // 3. Fall back to system Python
    return 'python3';
}

/**
 * Check if memory_graph package is installed
 */
export async function checkMemoryGraph(pythonPath: string): Promise<boolean> {
    try {
        const { stdout } = await execAsync(`${pythonPath} -c "import memory_graph; print('OK')"`);
        return stdout.trim() === 'OK';
    } catch (error) {
        return false;
    }
}

/**
 * Check if Graphviz is installed
 */
export async function checkGraphviz(): Promise<boolean> {
    try {
        await execAsync('dot -V');
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Get Python version
 */
export async function getPythonVersion(pythonPath: string): Promise<string> {
    try {
        const { stdout } = await execAsync(`${pythonPath} --version`);
        return stdout.trim();
    } catch (error) {
        return 'Unknown';
    }
}

/**
 * Check the entire Python environment
 */
export async function checkPythonEnvironment(): Promise<PythonEnvironment> {
    const pythonPath = await getPythonPath();
    const version = await getPythonVersion(pythonPath);
    const hasMemoryGraph = await checkMemoryGraph(pythonPath);
    const hasGraphviz = await checkGraphviz();

    return {
        pythonPath,
        version,
        hasMemoryGraph,
        hasGraphviz
    };
}

/**
 * Show installation instructions if components are missing
 */
export async function showInstallationInstructions(env: PythonEnvironment): Promise<void> {
    const missing: string[] = [];

    if (!env.hasMemoryGraph) {
        missing.push('memory_graph Python package');
    }
    if (!env.hasGraphviz) {
        missing.push('Graphviz');
    }

    if (missing.length === 0) {
        return;
    }

    const message = `Missing dependencies: ${missing.join(', ')}`;
    const action = await vscode.window.showWarningMessage(
        message,
        'Install Instructions',
        'Dismiss'
    );

    if (action === 'Install Instructions') {
        const instructions = `
# Memory Graph Dependencies

## Install memory_graph
\`\`\`bash
pip3 install memory_graph
\`\`\`

## Install Graphviz
**macOS (Homebrew):**
\`\`\`bash
brew install graphviz
\`\`\`

**Linux (Ubuntu/Debian):**
\`\`\`bash
sudo apt-get install graphviz
\`\`\`

**Windows:**
Download from: https://graphviz.org/download/

---

Python: ${env.pythonPath}
Version: ${env.version}
`;

        const doc = await vscode.workspace.openTextDocument({
            content: instructions,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);
    }
}