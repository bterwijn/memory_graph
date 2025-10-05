import * as vscode from 'vscode';
import { checkPythonEnvironment, showInstallationInstructions, PythonEnvironment } from './pythonUtils';

let pythonEnv: PythonEnvironment | null = null;

/**
 * This method is called when the extension is activated
 * Activation happens when a Python file is opened
 */
export async function activate(context: vscode.ExtensionContext) {
    console.log('Memory Graph extension is now active!');

    // Check Python environment on activation
    try {
        pythonEnv = await checkPythonEnvironment();
        console.log('Python environment check:', pythonEnv);

        // Show status in status bar
        const statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        
        if (pythonEnv.hasMemoryGraph && pythonEnv.hasGraphviz) {
            statusBarItem.text = "$(check) Memory Graph";
            statusBarItem.tooltip = `Ready!\nPython: ${pythonEnv.version}\nmemory_graph: ✓\nGraphviz: ✓`;
            statusBarItem.backgroundColor = undefined;
        } else {
            statusBarItem.text = "$(warning) Memory Graph";
            statusBarItem.tooltip = "Missing dependencies - click for details";
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            statusBarItem.command = 'memoryGraph.checkEnvironment';
        }
        
        statusBarItem.show();
        context.subscriptions.push(statusBarItem);

        // Show installation instructions if needed
        if (!pythonEnv.hasMemoryGraph || !pythonEnv.hasGraphviz) {
            await showInstallationInstructions(pythonEnv);
        } else {
            vscode.window.showInformationMessage('Memory Graph extension loaded! 🎉');
        }
    } catch (error) {
        console.error('Error checking Python environment:', error);
        vscode.window.showErrorMessage('Memory Graph: Failed to detect Python environment');
    }

    // Register command: Check Environment
    const checkEnvCommand = vscode.commands.registerCommand(
        'memoryGraph.checkEnvironment',
        async () => {
            try {
                pythonEnv = await checkPythonEnvironment();
                
                const status = `
Python Environment Status:
- Python: ${pythonEnv.pythonPath}
- Version: ${pythonEnv.version}
- memory_graph: ${pythonEnv.hasMemoryGraph ? '✓' : '✗'}
- Graphviz: ${pythonEnv.hasGraphviz ? '✓' : '✗'}
`;
                
                if (pythonEnv.hasMemoryGraph && pythonEnv.hasGraphviz) {
                    vscode.window.showInformationMessage(
                        'All dependencies are installed!',
                        { modal: false, detail: status }
                    );
                } else {
                    await showInstallationInstructions(pythonEnv);
                }
            } catch (error) {
                vscode.window.showErrorMessage('Failed to check environment: ' + error);
            }
        }
    );

    // Register command: Visualize Selection
    const visualizeCommand = vscode.commands.registerCommand(
        'memoryGraph.visualize',
        async () => {
            const editor = vscode.window.activeTextEditor;
            
            if (!editor) {
                vscode.window.showErrorMessage('No active editor found');
                return;
            }

            // Check environment first
            if (!pythonEnv) {
                pythonEnv = await checkPythonEnvironment();
            }

            if (!pythonEnv.hasMemoryGraph) {
                const action = await vscode.window.showErrorMessage(
                    'memory_graph package not found',
                    'Install Instructions'
                );
                if (action === 'Install Instructions') {
                    await showInstallationInstructions(pythonEnv);
                }
                return;
            }

            if (!pythonEnv.hasGraphviz) {
                const action = await vscode.window.showErrorMessage(
                    'Graphviz not found',
                    'Install Instructions'
                );
                if (action === 'Install Instructions') {
                    await showInstallationInstructions(pythonEnv);
                }
                return;
            }

            const selection = editor.selection;
            const selectedText = editor.document.getText(selection);

            if (!selectedText) {
                vscode.window.showWarningMessage('Please select some Python code to visualize');
                return;
            }

            vscode.window.showInformationMessage(
                `Memory Graph: Ready to visualize ${selectedText.length} characters`
            );
            
            // TODO: Phase 2 - We'll implement actual visualization here
        }
    );

    // Register command: Open Panel
    const openPanelCommand = vscode.commands.registerCommand(
        'memoryGraph.openPanel',
        () => {
            vscode.window.showInformationMessage('Memory Graph Panel - Coming soon in Phase 2!');
            // TODO: Phase 2.2 - We'll create the webview panel here
        }
    );

    // Add commands to subscriptions for cleanup
    context.subscriptions.push(checkEnvCommand);
    context.subscriptions.push(visualizeCommand);
    context.subscriptions.push(openPanelCommand);
}

/**
 * This method is called when the extension is deactivated
 */
export function deactivate() {
    console.log('Memory Graph extension is now deactivated');
}