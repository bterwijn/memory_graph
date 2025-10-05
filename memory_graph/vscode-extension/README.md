# Memory Graph - VS Code Extension

Visualize Python data structures, references, mutability, and memory relationships directly in Visual Studio Code.

Built on top of the [memory_graph](https://github.com/bterwijn/memory_graph) Python package.

## Features

- **Visual Data Structure Debugging** - See your data structures as intuitive graphs
- **Reference Tracking** - Understand which variables share data and avoid mutation bugs
- **Inline Visualization** - Graphs display in a VS Code panel alongside your code
- **Interactive Controls** - Zoom, refresh, and explore your memory graphs
- **Automatic Environment Detection** - Checks for Python, memory_graph, and Graphviz
- **Progress Notifications** - Clear feedback during graph generation

## Requirements

### Python Environment
- Python 3.6 or higher
- `memory_graph` Python package:
  ```bash
  pip install memory_graph
  ```

### Graphviz
- **macOS (Homebrew):**
  ```bash
  brew install graphviz
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get install graphviz
  ```
- **Windows:**
  Download from [graphviz.org/download](https://graphviz.org/download/)

## Installation

1. Clone the repository and navigate to the extension:
   ```bash
   git clone https://github.com/Akshen/memory_graph.git
   cd memory_graph/vscode-extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the extension:
   ```bash
   npm run compile
   ```

4. Press `F5` in VS Code to launch the Extension Development Host

## Usage

### Basic Workflow

1. **Write Python code** with data structures:
   ```python
   a = [1, 2, 3]
   b = a
   b.append(4)
   
   c = {'name': 'test', 'items': a}
   ```

2. **Select the code** you want to visualize

3. **Right-click** and choose **"Memory Graph: Visualize Selection"**
   - Or use Command Palette: `Ctrl+Shift+P` → "Memory Graph: Visualize Selection"

4. **View the graph** in the side panel showing:
   - All variables and their values
   - References between objects
   - Shared data (when multiple variables point to the same object)

### Commands

- **Memory Graph: Visualize Selection** - Generate graph from selected Python code
- **Memory Graph: Open Visualization Panel** - Open the graph panel
- **Memory Graph: Check Environment** - Verify dependencies are installed

### Panel Controls

Once a graph is displayed, you can:
- **Refresh** - Regenerate the graph with updated code
- **Zoom In/Out** - Explore complex graphs in detail
- **Reset Zoom** - Return to default view

## Configuration

Access settings via VS Code preferences:

- `memoryGraph.pythonPath` - Custom Python interpreter path (leave empty to use workspace Python)
- `memoryGraph.outputFormat` - Graph format: `svg` (default) or `png`

## Examples

### Example 1: Understanding References
```python
# Variables sharing the same list
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4] - Why?
```
**Visualize this** to see that `a` and `b` point to the same list object.

### Example 2: Shallow vs Deep Copy
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0].append(5)
```
**Visualize this** to see how shallow copy shares nested objects but deep copy doesn't.

### Example 3: Dictionary References
```python
data = {'x': 10, 'y': 20}
config = {'settings': data}
backup = data

data['x'] = 999
```
**Visualize this** to see how `config['settings']`, `backup`, and `data` all reference the same dictionary.

## Troubleshooting

### Extension doesn't activate
- Make sure you're editing a `.py` file
- Check the Debug Console for errors

### "memory_graph package not found"
- Install it: `pip3 install memory_graph`
- Or check the custom Python path in settings

### "Graphviz not found"
- Install Graphviz using your system's package manager
- Verify with: `dot -V`

### Graph generation fails
- Check that your Python code is valid
- Remove any existing `mg.show()` or `mg.render()` calls (extension adds these automatically)
- Check the error message for details

## Development

### Building from Source
```bash
npm install
npm run compile
```

### Running in Debug Mode
Press `F5` in VS Code to launch the Extension Development Host

### Watch Mode
```bash
npm run watch
```

### Packaging
```bash
npm run package
```

## Project Status

**Completed Features:**
- Phase 1: Foundation and Python environment detection
- Phase 2: Core visualization with webview integration

**Future Enhancements (not planned):**
- Smart variable selection
- Debug integration
- Advanced configuration options

## Contributing

This extension is part of the [memory_graph](https://github.com/bterwijn/memory_graph) project. For issues or contributions, please visit the main repository.

## Credits

- Based on [memory_graph](https://pypi.org/project/memory-graph/) by Bas Terwijn
- Extension development: Community contribution

## Learn More

- [memory_graph Documentation](https://github.com/bterwijn/memory_graph)
- [Memory Graph Web Debugger](https://memory-graph.com/)
- [VS Code Extension API](https://code.visualstudio.com/api)