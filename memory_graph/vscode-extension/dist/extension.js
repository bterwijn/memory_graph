"use strict";var H=Object.create;var y=Object.defineProperty;var A=Object.getOwnPropertyDescriptor;var U=Object.getOwnPropertyNames;var B=Object.getPrototypeOf,R=Object.prototype.hasOwnProperty;var W=(t,e)=>()=>(t&&(e=t(t=0)),e);var z=(t,e)=>{for(var o in e)y(t,o,{get:e[o],enumerable:!0})},I=(t,e,o,s)=>{if(e&&typeof e=="object"||typeof e=="function")for(let i of U(e))!R.call(t,i)&&i!==o&&y(t,i,{get:()=>e[i],enumerable:!(s=A(e,i))||s.enumerable});return t};var h=(t,e,o)=>(o=t!=null?H(B(t)):{},I(e||!t||!t.__esModule?y(o,"default",{value:t,enumerable:!0}):o,t)),V=t=>I(y({},"__esModule",{value:!0}),t);var M={};z(M,{cleanupOldTempFiles:()=>X,generateGraph:()=>J});async function J(t){let e=_.tmpdir(),o=Date.now(),s=x.join(e,`memory_graph_temp_${o}.py`),i=x.join(e,`memory_graph_output_${o}.${t.outputFormat}`);try{let r=Q(t.code,i,t.visualizeType);await N(s,r,"utf8");let{stdout:G,stderr:g}=await K(`${t.pythonPath} "${s}"`,{timeout:3e4});return c.existsSync(i)?(await b(s).catch(()=>{}),{success:!0,outputPath:i}):{success:!1,error:`Output file not generated. stderr: ${g}`}}catch(r){return await b(s).catch(()=>{}),await b(i).catch(()=>{}),{success:!1,error:r.message||String(r)}}}function Q(t,e,o){let s=t.replace(/\bmg\.show\([^)]*\)/g,"# mg.show() removed by extension").replace(/\bmg\.render\([^)]*\)/g,"# mg.render() removed by extension").replace(/\bmg\.block\([^)]*\)/g,"# mg.block() removed by extension").replace(/\bmemory_graph\.show\([^)]*\)/g,"# memory_graph.show() removed").replace(/\bmemory_graph\.render\([^)]*\)/g,"# memory_graph.render() removed").replace(/\bmemory_graph\.block\([^)]*\)/g,"# memory_graph.block() removed"),i=e.replace(/\\/g,"\\\\");return`
import memory_graph as mg
import sys

# User code starts here
${s}
# User code ends here

# Generate the graph
try:
    if '${o}' == 'stack':
        mg.render(mg.stack(), "${i}")
    else:
        mg.render(locals(), "${i}")
except Exception as e:
    print(f"Error generating graph: {e}", file=sys.stderr)
    sys.exit(1)
`}async function X(){let t=_.tmpdir(),e=c.readdirSync(t),s=Date.now()-60*60*1e3;for(let i of e)if(i.startsWith("memory_graph_temp_")||i.startsWith("memory_graph_output_"))try{let r=x.join(t,i);c.statSync(r).mtimeMs<s&&await b(r)}catch{}}var c,x,_,F,P,K,N,b,E=W(()=>{"use strict";c=h(require("fs")),x=h(require("path")),_=h(require("os")),F=require("child_process"),P=require("util"),K=(0,P.promisify)(F.exec),N=(0,P.promisify)(c.writeFile),b=(0,P.promisify)(c.unlink)});var oe={};z(oe,{activate:()=>ee,deactivate:()=>te});module.exports=V(oe);var n=h(require("vscode"));var m=h(require("vscode")),$=require("child_process"),O=require("util"),k=(0,O.promisify)($.exec);async function j(){let e=m.workspace.getConfiguration("memoryGraph").get("pythonPath");if(e)return e;try{let o=m.extensions.getExtension("ms-python.python");if(o){o.isActive||await o.activate();let s=o.exports?.settings?.getExecutionDetails?.()?.execCommand?.[0];if(s)return s}}catch(o){console.log("Could not get Python from extension:",o)}return"python3"}async function L(t){try{let{stdout:e}=await k(`${t} -c "import memory_graph; print('OK')"`);return e.trim()==="OK"}catch{return!1}}async function Y(){try{return await k("dot -V"),!0}catch{return!1}}async function q(t){try{let{stdout:e}=await k(`${t} --version`);return e.trim()}catch{return"Unknown"}}async function w(){let t=await j(),e=await q(t),o=await L(t),s=await Y();return{pythonPath:t,version:e,hasMemoryGraph:o,hasGraphviz:s}}async function d(t){let e=[];if(t.hasMemoryGraph||e.push("memory_graph Python package"),t.hasGraphviz||e.push("Graphviz"),e.length===0)return;let o=`Missing dependencies: ${e.join(", ")}`;if(await m.window.showWarningMessage(o,"Install Instructions","Dismiss")==="Install Instructions"){let i=`
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

Python: ${t.pythonPath}
Version: ${t.version}
`,r=await m.workspace.openTextDocument({content:i,language:"markdown"});await m.window.showTextDocument(r)}}var p=h(require("vscode")),u=h(require("fs")),f=class t{static currentPanel;_panel;_disposables=[];constructor(e,o){this._panel=e,this._panel.webview.html=this._getLoadingHtml(),this._panel.webview.onDidReceiveMessage(s=>{switch(s.command){case"refresh":p.commands.executeCommand("memoryGraph.visualize");break}},null,this._disposables),this._panel.onDidDispose(()=>this.dispose(),null,this._disposables)}static createOrShow(e){let o=p.window.activeTextEditor?p.ViewColumn.Beside:p.ViewColumn.One;if(t.currentPanel)return t.currentPanel._panel.reveal(o),t.currentPanel;let s=p.window.createWebviewPanel("memoryGraphView","Memory Graph",o,{enableScripts:!0,retainContextWhenHidden:!0,localResourceRoots:[e]});return t.currentPanel=new t(s,e),t.currentPanel}updateGraph(e,o){if(!u.existsSync(e)){this._panel.webview.html=this._getErrorHtml("Graph file not found");return}if(o==="svg"){let s=u.readFileSync(e,"utf8");this._panel.webview.html=this._getGraphHtml(s,"svg")}else{let i=u.readFileSync(e).toString("base64");this._panel.webview.html=this._getGraphHtml(i,"png")}}showLoading(){this._panel.webview.html=this._getLoadingHtml()}showError(e){this._panel.webview.html=this._getErrorHtml(e)}_getLoadingHtml(){return`<!DOCTYPE html>
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
</html>`}_getErrorHtml(e){return`<!DOCTYPE html>
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
        <p>${this._escapeHtml(e)}</p>
    </div>
</body>
</html>`}_getGraphHtml(e,o){return`<!DOCTYPE html>
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
        ${o==="svg"?e:`<img src="data:image/png;base64,${e}" style="max-width: 100%; height: auto;" />`}
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
</html>`}_escapeHtml(e){return e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#039;")}dispose(){for(t.currentPanel=void 0,this._panel.dispose();this._disposables.length;){let e=this._disposables.pop();e&&e.dispose()}}};var a=null;async function ee(t){console.log("Memory Graph extension is now active!");let{cleanupOldTempFiles:e}=await Promise.resolve().then(()=>(E(),M));e().catch(r=>console.log("Cleanup error:",r));try{a=await w(),console.log("Python environment check:",a);let r=n.window.createStatusBarItem(n.StatusBarAlignment.Right,100);a.hasMemoryGraph&&a.hasGraphviz?(r.text="$(check) Memory Graph",r.tooltip=`Ready!
Python: ${a.version}
memory_graph: \u2713
Graphviz: \u2713`,r.backgroundColor=void 0):(r.text="$(warning) Memory Graph",r.tooltip="Missing dependencies - click for details",r.backgroundColor=new n.ThemeColor("statusBarItem.warningBackground"),r.command="memoryGraph.checkEnvironment"),r.show(),t.subscriptions.push(r),!a.hasMemoryGraph||!a.hasGraphviz?await d(a):n.window.showInformationMessage("Memory Graph extension loaded! \u{1F389}")}catch(r){console.error("Error checking Python environment:",r),n.window.showErrorMessage("Memory Graph: Failed to detect Python environment")}let o=n.commands.registerCommand("memoryGraph.checkEnvironment",async()=>{try{a=await w();let r=`
Python Environment Status:
- Python: ${a.pythonPath}
- Version: ${a.version}
- memory_graph: ${a.hasMemoryGraph?"\u2713":"\u2717"}
- Graphviz: ${a.hasGraphviz?"\u2713":"\u2717"}
`;a.hasMemoryGraph&&a.hasGraphviz?n.window.showInformationMessage("All dependencies are installed!",{modal:!1,detail:r}):await d(a)}catch(r){n.window.showErrorMessage("Failed to check environment: "+r)}}),s=n.commands.registerCommand("memoryGraph.visualize",async()=>{let r=n.window.activeTextEditor;if(!r){n.window.showErrorMessage("No active editor found");return}if(a||(a=await w()),!a){n.window.showErrorMessage("Failed to detect Python environment");return}if(!a.hasMemoryGraph){await n.window.showErrorMessage("memory_graph package not found","Install Instructions")==="Install Instructions"&&await d(a);return}if(!a.hasGraphviz){await n.window.showErrorMessage("Graphviz not found","Install Instructions")==="Install Instructions"&&await d(a);return}let G=r.selection,g=r.document.getText(G);if(!g){n.window.showWarningMessage("Please select some Python code to visualize");return}let D=a;await n.window.withProgress({location:n.ProgressLocation.Notification,title:"Generating memory graph...",cancellable:!1},async l=>{l.report({increment:0});let{generateGraph:T}=await Promise.resolve().then(()=>(E(),M)),S=n.workspace.getConfiguration("memoryGraph").get("outputFormat","svg");l.report({increment:30,message:"Running Python code..."});let v=await T({code:g,pythonPath:D.pythonPath,outputFormat:S,visualizeType:"locals"});if(l.report({increment:70}),v.success&&v.outputPath){let C=n.Uri.file(v.outputPath);await n.commands.executeCommand("vscode.open",C),n.window.showInformationMessage("Memory graph generated successfully!","Open Again").then(Z=>{Z==="Open Again"&&n.commands.executeCommand("vscode.open",C)})}else n.window.showErrorMessage(`Failed to generate graph: ${v.error}`)})}),i=n.commands.registerCommand("memoryGraph.openPanel",()=>{f.createOrShow(t.extensionUri)});t.subscriptions.push(o),t.subscriptions.push(s),t.subscriptions.push(i)}function te(){console.log("Memory Graph extension is now deactivated")}0&&(module.exports={activate,deactivate});
//# sourceMappingURL=extension.js.map
