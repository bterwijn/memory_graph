import * as vscode from 'vscode';
import * as fs from 'fs';

export class MemoryGraphPanel {
    public static currentPanel: MemoryGraphPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;

        // Set the webview's initial html content
        this._panel.webview.html = this._getLoadingHtml();

        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'refresh':
                        vscode.commands.executeCommand('memoryGraph.visualize');
                        break;
                }
            },
            null,
            this._disposables
        );

        // Clean up when panel is closed
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    public static createOrShow(extensionUri: vscode.Uri): MemoryGraphPanel {
        const column = vscode.window.activeTextEditor
            ? vscode.ViewColumn.Beside
            : vscode.ViewColumn.One;

        // If we already have a panel, show it
        if (MemoryGraphPanel.currentPanel) {
            MemoryGraphPanel.currentPanel._panel.reveal(column);
            return MemoryGraphPanel.currentPanel;
        }

        // Otherwise, create a new panel
        const panel = vscode.window.createWebviewPanel(
            'memoryGraphView',
            'Memory Graph',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        MemoryGraphPanel.currentPanel = new MemoryGraphPanel(panel, extensionUri);
        return MemoryGraphPanel.currentPanel;
    }

    public updateGraph(graphPath: string, format: 'svg' | 'png'): void {
        if (!fs.existsSync(graphPath)) {
            this._panel.webview.html = this._getErrorHtml('Graph file not found');
            return;
        }

        if (format === 'svg') {
            const svgContent = fs.readFileSync(graphPath, 'utf8');
            this._panel.webview.html = this._getGraphHtml(svgContent, 'svg');
        } else {
            // For PNG, convert to base64
            const pngBuffer = fs.readFileSync(graphPath);
            const base64 = pngBuffer.toString('base64');
            this._panel.webview.html = this._getGraphHtml(base64, 'png');
        }
    }

    public showLoading(): void {
        this._panel.webview.html = this._getLoadingHtml();
    }

    public showError(message: string): void {
        this._panel.webview.html = this._getErrorHtml(message);
    }

    private _getLoadingHtml(): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Graph</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        .message {
            text-align: center;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="message">
        <p>Select Python code and use "Memory Graph: Visualize Selection" to generate a graph.</p>
    </div>
</body>
</html>`;
    }

    private _getErrorHtml(error: string): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Graph - Error</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: var(--vscode-font-family);
            color: var(--vscode-errorForeground);
            background-color: var(--vscode-editor-background);
        }
        .error {
            text-align: center;
            padding: 20px;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <div class="error">
        <h2>Error</h2>
        <p>${this._escapeHtml(error)}</p>
    </div>
</body>
</html>`;
    }

    private _getGraphHtml(content: string, format: 'svg' | 'png'): string {
        const graphContent = format === 'svg' 
            ? content 
            : `<img src="data:image/png;base64,${content}" style="max-width: 100%; height: auto;" />`;

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Graph</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: var(--vscode-font-family);
            background-color: var(--vscode-editor-background);
            color: var(--vscode-foreground);
            overflow: auto;
        }
        .toolbar {
            position: sticky;
            top: 0;
            background-color: var(--vscode-editor-background);
            padding: 10px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--vscode-panel-border);
            z-index: 100;
        }
        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 8px 16px;
            margin-right: 8px;
            cursor: pointer;
            font-size: 13px;
            border-radius: 2px;
        }
        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        .graph-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: calc(100vh - 100px);
        }
        svg {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="toolbar">
        <button onclick="refresh()">Refresh</button>
        <button onclick="zoomIn()">Zoom In</button>
        <button onclick="zoomOut()">Zoom Out</button>
        <button onclick="resetZoom()">Reset Zoom</button>
    </div>
    <div class="graph-container" id="graphContainer">
        ${graphContent}
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        let currentZoom = 1;

        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }

        function zoomIn() {
            currentZoom = Math.min(currentZoom + 0.2, 3);
            applyZoom();
        }

        function zoomOut() {
            currentZoom = Math.max(currentZoom - 0.2, 0.5);
            applyZoom();
        }

        function resetZoom() {
            currentZoom = 1;
            applyZoom();
        }

        function applyZoom() {
            const container = document.getElementById('graphContainer');
            container.style.transform = 'scale(' + currentZoom + ')';
            container.style.transformOrigin = 'top center';
        }
    </script>
</body>
</html>`;
    }

    private _escapeHtml(text: string): string {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    public dispose(): void {
        MemoryGraphPanel.currentPanel = undefined;

        this._panel.dispose();

        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}