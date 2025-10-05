"use strict";var f=Object.create;var h=Object.defineProperty;var P=Object.getOwnPropertyDescriptor;var G=Object.getOwnPropertyNames;var M=Object.getPrototypeOf,x=Object.prototype.hasOwnProperty;var I=(o,n)=>{for(var s in n)h(o,s,{get:n[s],enumerable:!0})},y=(o,n,s,a)=>{if(n&&typeof n=="object"||typeof n=="function")for(let t of G(n))!x.call(o,t)&&t!==s&&h(o,t,{get:()=>n[t],enumerable:!(a=P(n,t))||a.enumerable});return o};var w=(o,n,s)=>(s=o!=null?f(M(o)):{},y(n||!o||!o.__esModule?h(s,"default",{value:o,enumerable:!0}):s,o)),E=o=>y(h({},"__esModule",{value:!0}),o);var _={};I(_,{activate:()=>$,deactivate:()=>D});module.exports=E(_);var r=w(require("vscode"));var i=w(require("vscode")),u=require("child_process"),v=require("util"),d=(0,v.promisify)(u.exec);async function k(){let n=i.workspace.getConfiguration("memoryGraph").get("pythonPath");if(n)return n;try{let s=i.extensions.getExtension("ms-python.python");if(s){s.isActive||await s.activate();let a=s.exports?.settings?.getExecutionDetails?.()?.execCommand?.[0];if(a)return a}}catch(s){console.log("Could not get Python from extension:",s)}return"python3"}async function z(o){try{let{stdout:n}=await d(`${o} -c "import memory_graph; print('OK')"`);return n.trim()==="OK"}catch{return!1}}async function b(){try{return await d("dot -V"),!0}catch{return!1}}async function C(o){try{let{stdout:n}=await d(`${o} --version`);return n.trim()}catch{return"Unknown"}}async function m(){let o=await k(),n=await C(o),s=await z(o),a=await b();return{pythonPath:o,version:n,hasMemoryGraph:s,hasGraphviz:a}}async function c(o){let n=[];if(o.hasMemoryGraph||n.push("memory_graph Python package"),o.hasGraphviz||n.push("Graphviz"),n.length===0)return;let s=`Missing dependencies: ${n.join(", ")}`;if(await i.window.showWarningMessage(s,"Install Instructions","Dismiss")==="Install Instructions"){let t=`
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

Python: ${o.pythonPath}
Version: ${o.version}
`,p=await i.workspace.openTextDocument({content:t,language:"markdown"});await i.window.showTextDocument(p)}}var e=null;async function $(o){console.log("Memory Graph extension is now active!");try{e=await m(),console.log("Python environment check:",e);let t=r.window.createStatusBarItem(r.StatusBarAlignment.Right,100);e.hasMemoryGraph&&e.hasGraphviz?(t.text="$(check) Memory Graph",t.tooltip=`Ready!
Python: ${e.version}
memory_graph: \u2713
Graphviz: \u2713`,t.backgroundColor=void 0):(t.text="$(warning) Memory Graph",t.tooltip="Missing dependencies - click for details",t.backgroundColor=new r.ThemeColor("statusBarItem.warningBackground"),t.command="memoryGraph.checkEnvironment"),t.show(),o.subscriptions.push(t),!e.hasMemoryGraph||!e.hasGraphviz?await c(e):r.window.showInformationMessage("Memory Graph extension loaded! \u{1F389}")}catch(t){console.error("Error checking Python environment:",t),r.window.showErrorMessage("Memory Graph: Failed to detect Python environment")}let n=r.commands.registerCommand("memoryGraph.checkEnvironment",async()=>{try{e=await m();let t=`
Python Environment Status:
- Python: ${e.pythonPath}
- Version: ${e.version}
- memory_graph: ${e.hasMemoryGraph?"\u2713":"\u2717"}
- Graphviz: ${e.hasGraphviz?"\u2713":"\u2717"}
`;e.hasMemoryGraph&&e.hasGraphviz?r.window.showInformationMessage("All dependencies are installed!",{modal:!1,detail:t}):await c(e)}catch(t){r.window.showErrorMessage("Failed to check environment: "+t)}}),s=r.commands.registerCommand("memoryGraph.visualize",async()=>{let t=r.window.activeTextEditor;if(!t){r.window.showErrorMessage("No active editor found");return}if(e||(e=await m()),!e.hasMemoryGraph){await r.window.showErrorMessage("memory_graph package not found","Install Instructions")==="Install Instructions"&&await c(e);return}if(!e.hasGraphviz){await r.window.showErrorMessage("Graphviz not found","Install Instructions")==="Install Instructions"&&await c(e);return}let p=t.selection,l=t.document.getText(p);if(!l){r.window.showWarningMessage("Please select some Python code to visualize");return}r.window.showInformationMessage(`Memory Graph: Ready to visualize ${l.length} characters`)}),a=r.commands.registerCommand("memoryGraph.openPanel",()=>{r.window.showInformationMessage("Memory Graph Panel - Coming soon in Phase 2!")});o.subscriptions.push(n),o.subscriptions.push(s),o.subscriptions.push(a)}function D(){console.log("Memory Graph extension is now deactivated")}0&&(module.exports={activate,deactivate});
//# sourceMappingURL=extension.js.map
