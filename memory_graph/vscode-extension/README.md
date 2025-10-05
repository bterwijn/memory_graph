# Memory Graph - VS Code Extension

Visualize Python data structures, references, mutability, and call stacks directly in Visual Studio Code.

## Features

- 🎨 **Visual Debugging**: See your data structures as graphs
- 🔍 **Reference Tracking**: Understand which variables share data
- 📊 **Call Stack Visualization**: Debug function calls with visual context
- ⚡ **Debug Integration**: Auto-visualize during debugging sessions

## Requirements

- Python 3.6 or higher
- `memory_graph` Python package installed:
  ```bash
  pip install memory_graph
  ```
- Graphviz installed ([Download](https://graphviz.org/download/))

## Quick Start

1. Open a Python file
2. Select code you want to visualize
3. Right-click → **"Memory Graph: Visualize Selection"**
4. Or use Command Palette: `Ctrl+Shift+P` → "Memory Graph: Visualize"

## Extension Commands

- `Memory Graph: Visualize Selection` - Visualize selected Python code
- `Memory Graph: Open Visualization Panel` - Open the graph panel

## Extension Settings

- `memoryGraph.pythonPath` - Custom Python interpreter path
- `memoryGraph.outputFormat` - Graph output format (svg/png)
- `memoryGraph.autoVisualize` - Auto-visualize on debug breakpoints

## Development Status

🚧 **Phase 1.1 Complete** - Basic extension structure
- [x] Extension activation
- [x] Command registration
- [ ] Python integration (Phase 1.2)
- [ ] Graph rendering (Phase 2)
- [ ] Debug integration (Phase 4)

## Development

### Building
```bash
npm install
npm run compile
```

### Testing
Press `F5` in VS Code to launch Extension Development Host

### Packaging
```bash
npm run package
```

## License

MIT

## Credits

Based on the [memory_graph](https://github.com/bterwijn/memory_graph) Python package by Bas Terwijn.