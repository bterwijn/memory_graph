"use strict";var A=Object.create;var u=Object.defineProperty;var O=Object.getOwnPropertyDescriptor;var S=Object.getOwnPropertyNames;var W=Object.getPrototypeOf,B=Object.prototype.hasOwnProperty;var R=(e,o)=>()=>(e&&(o=e(e=0)),o);var E=(e,o)=>{for(var r in o)u(e,r,{get:o[r],enumerable:!0})},_=(e,o,r,i)=>{if(o&&typeof o=="object"||typeof o=="function")for(let a of S(o))!B.call(e,a)&&a!==r&&u(e,a,{get:()=>o[a],enumerable:!(i=O(o,a))||i.enumerable});return e};var p=(e,o,r)=>(r=e!=null?A(W(e)):{},_(o||!e||!e.__esModule?u(r,"default",{value:e,enumerable:!0}):r,e)),U=e=>_(u({},"__esModule",{value:!0}),e);var M={};E(M,{cleanupOldTempFiles:()=>Q,generateGraph:()=>q});async function q(e){let o=x.tmpdir(),r=Date.now(),i=v.join(o,`memory_graph_temp_${r}.py`),a=v.join(o,`memory_graph_output_${r}.${e.outputFormat}`);try{let t=J(e.code,a,e.visualizeType);await N(i,t,"utf8");let{stdout:P,stderr:l}=await L(`${e.pythonPath} "${i}"`,{timeout:3e4});return c.existsSync(a)?(await w(i).catch(()=>{}),{success:!0,outputPath:a}):{success:!1,error:`Output file not generated. stderr: ${l}`}}catch(t){return await w(i).catch(()=>{}),await w(a).catch(()=>{}),{success:!1,error:t.message||String(t)}}}function J(e,o,r){let i=e.replace(/\bmg\.show\([^)]*\)/g,"# mg.show() removed by extension").replace(/\bmg\.render\([^)]*\)/g,"# mg.render() removed by extension").replace(/\bmg\.block\([^)]*\)/g,"# mg.block() removed by extension").replace(/\bmemory_graph\.show\([^)]*\)/g,"# memory_graph.show() removed").replace(/\bmemory_graph\.render\([^)]*\)/g,"# memory_graph.render() removed").replace(/\bmemory_graph\.block\([^)]*\)/g,"# memory_graph.block() removed"),a=o.replace(/\\/g,"\\\\");return`
import memory_graph as mg
import sys

# User code starts here
${i}
# User code ends here

# Generate the graph
try:
    if '${r}' == 'stack':
        mg.render(mg.stack(), "${a}")
    else:
        mg.render(locals(), "${a}")
except Exception as e:
    print(f"Error generating graph: {e}", file=sys.stderr)
    sys.exit(1)
`}async function Q(){let e=x.tmpdir(),o=c.readdirSync(e),i=Date.now()-60*60*1e3;for(let a of o)if(a.startsWith("memory_graph_temp_")||a.startsWith("memory_graph_output_"))try{let t=v.join(e,a);c.statSync(t).mtimeMs<i&&await w(t)}catch{}}var c,v,x,$,f,L,N,w,b=R(()=>{"use strict";c=p(require("fs")),v=p(require("path")),x=p(require("os")),$=require("child_process"),f=require("util"),L=(0,f.promisify)($.exec),N=(0,f.promisify)(c.writeFile),w=(0,f.promisify)(c.unlink)});var Z={};E(Z,{activate:()=>X,deactivate:()=>Y});module.exports=U(Z);var n=p(require("vscode"));var m=p(require("vscode")),I=require("child_process"),z=require("util"),G=(0,z.promisify)(I.exec);async function j(){let o=m.workspace.getConfiguration("memoryGraph").get("pythonPath");if(o)return o;try{let r=m.extensions.getExtension("ms-python.python");if(r){r.isActive||await r.activate();let i=r.exports?.settings?.getExecutionDetails?.()?.execCommand?.[0];if(i)return i}}catch(r){console.log("Could not get Python from extension:",r)}return"python3"}async function V(e){try{let{stdout:o}=await G(`${e} -c "import memory_graph; print('OK')"`);return o.trim()==="OK"}catch{return!1}}async function H(){try{return await G("dot -V"),!0}catch{return!1}}async function K(e){try{let{stdout:o}=await G(`${e} --version`);return o.trim()}catch{return"Unknown"}}async function y(){let e=await j(),o=await K(e),r=await V(e),i=await H();return{pythonPath:e,version:o,hasMemoryGraph:r,hasGraphviz:i}}async function d(e){let o=[];if(e.hasMemoryGraph||o.push("memory_graph Python package"),e.hasGraphviz||o.push("Graphviz"),o.length===0)return;let r=`Missing dependencies: ${o.join(", ")}`;if(await m.window.showWarningMessage(r,"Install Instructions","Dismiss")==="Install Instructions"){let a=`
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

Python: ${e.pythonPath}
Version: ${e.version}
`,t=await m.workspace.openTextDocument({content:a,language:"markdown"});await m.window.showTextDocument(t)}}var s=null;async function X(e){console.log("Memory Graph extension is now active!");let{cleanupOldTempFiles:o}=await Promise.resolve().then(()=>(b(),M));o().catch(t=>console.log("Cleanup error:",t));try{s=await y(),console.log("Python environment check:",s);let t=n.window.createStatusBarItem(n.StatusBarAlignment.Right,100);s.hasMemoryGraph&&s.hasGraphviz?(t.text="$(check) Memory Graph",t.tooltip=`Ready!
Python: ${s.version}
memory_graph: \u2713
Graphviz: \u2713`,t.backgroundColor=void 0):(t.text="$(warning) Memory Graph",t.tooltip="Missing dependencies - click for details",t.backgroundColor=new n.ThemeColor("statusBarItem.warningBackground"),t.command="memoryGraph.checkEnvironment"),t.show(),e.subscriptions.push(t),!s.hasMemoryGraph||!s.hasGraphviz?await d(s):n.window.showInformationMessage("Memory Graph extension loaded! \u{1F389}")}catch(t){console.error("Error checking Python environment:",t),n.window.showErrorMessage("Memory Graph: Failed to detect Python environment")}let r=n.commands.registerCommand("memoryGraph.checkEnvironment",async()=>{try{s=await y();let t=`
Python Environment Status:
- Python: ${s.pythonPath}
- Version: ${s.version}
- memory_graph: ${s.hasMemoryGraph?"\u2713":"\u2717"}
- Graphviz: ${s.hasGraphviz?"\u2713":"\u2717"}
`;s.hasMemoryGraph&&s.hasGraphviz?n.window.showInformationMessage("All dependencies are installed!",{modal:!1,detail:t}):await d(s)}catch(t){n.window.showErrorMessage("Failed to check environment: "+t)}}),i=n.commands.registerCommand("memoryGraph.visualize",async()=>{let t=n.window.activeTextEditor;if(!t){n.window.showErrorMessage("No active editor found");return}if(s||(s=await y()),!s){n.window.showErrorMessage("Failed to detect Python environment");return}if(!s.hasMemoryGraph){await n.window.showErrorMessage("memory_graph package not found","Install Instructions")==="Install Instructions"&&await d(s);return}if(!s.hasGraphviz){await n.window.showErrorMessage("Graphviz not found","Install Instructions")==="Install Instructions"&&await d(s);return}let P=t.selection,l=t.document.getText(P);if(!l){n.window.showWarningMessage("Please select some Python code to visualize");return}let C=s;await n.window.withProgress({location:n.ProgressLocation.Notification,title:"Generating memory graph...",cancellable:!1},async h=>{h.report({increment:0});let{generateGraph:F}=await Promise.resolve().then(()=>(b(),M)),D=n.workspace.getConfiguration("memoryGraph").get("outputFormat","svg");h.report({increment:30,message:"Running Python code..."});let g=await F({code:l,pythonPath:C.pythonPath,outputFormat:D,visualizeType:"locals"});if(h.report({increment:70}),g.success&&g.outputPath){let k=n.Uri.file(g.outputPath);await n.commands.executeCommand("vscode.open",k),n.window.showInformationMessage("Memory graph generated successfully!","Open Again").then(T=>{T==="Open Again"&&n.commands.executeCommand("vscode.open",k)})}else n.window.showErrorMessage(`Failed to generate graph: ${g.error}`)})}),a=n.commands.registerCommand("memoryGraph.openPanel",()=>{n.window.showInformationMessage("Memory Graph Panel - Coming soon in Phase 2!")});e.subscriptions.push(r),e.subscriptions.push(i),e.subscriptions.push(a)}function Y(){console.log("Memory Graph extension is now deactivated")}0&&(module.exports={activate,deactivate});
//# sourceMappingURL=extension.js.map
