import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
const writeFileAsync = promisify(fs.writeFile);
const unlinkAsync = promisify(fs.unlink);

export interface GraphGenerationOptions {
    code: string;
    pythonPath: string;
    outputFormat: 'svg' | 'png';
    visualizeType: 'locals' | 'stack';
}

export interface GraphResult {
    success: boolean;
    outputPath?: string;
    error?: string;
}

/**
 * Generate a memory graph from Python code
 */
export async function generateGraph(options: GraphGenerationOptions): Promise<GraphResult> {
    const tempDir = os.tmpdir();
    const timestamp = Date.now();
    const scriptPath = path.join(tempDir, `memory_graph_temp_${timestamp}.py`);
    const outputPath = path.join(tempDir, `memory_graph_output_${timestamp}.${options.outputFormat}`);

    try {
        // Create the Python script with memory_graph visualization
        const wrappedCode = wrapCodeWithMemoryGraph(options.code, outputPath, options.visualizeType);
        await writeFileAsync(scriptPath, wrappedCode, 'utf8');

        // Execute the Python script
        const { stdout, stderr } = await execAsync(
            `${options.pythonPath} "${scriptPath}"`,
            { timeout: 30000 } // 30 second timeout
        );

        // Check if output file was created
        if (!fs.existsSync(outputPath)) {
            return {
                success: false,
                error: `Output file not generated. stderr: ${stderr}`
            };
        }

        // Clean up the temporary script
        await unlinkAsync(scriptPath).catch(() => {});

        return {
            success: true,
            outputPath: outputPath
        };

    } catch (error: any) {
        // Clean up on error
        await unlinkAsync(scriptPath).catch(() => {});
        await unlinkAsync(outputPath).catch(() => {});

        return {
            success: false,
            error: error.message || String(error)
        };
    }
}

/**
 * Wrap user code with memory_graph visualization commands
 */
function wrapCodeWithMemoryGraph(
    userCode: string,
    outputPath: string,
    visualizeType: 'locals' | 'stack'
): string {
    // Remove any existing mg.show(), mg.render(), mg.block() calls from user code
    // This prevents conflicts with our wrapper code
    const cleanedCode = userCode
        .replace(/\bmg\.show\([^)]*\)/g, '# mg.show() removed by extension')
        .replace(/\bmg\.render\([^)]*\)/g, '# mg.render() removed by extension')
        .replace(/\bmg\.block\([^)]*\)/g, '# mg.block() removed by extension')
        .replace(/\bmemory_graph\.show\([^)]*\)/g, '# memory_graph.show() removed')
        .replace(/\bmemory_graph\.render\([^)]*\)/g, '# memory_graph.render() removed')
        .replace(/\bmemory_graph\.block\([^)]*\)/g, '# memory_graph.block() removed');

    // Escape the output path for Python
    const escapedPath = outputPath.replace(/\\/g, '\\\\');

    const template = `
import memory_graph as mg
import sys

# User code starts here
${cleanedCode}
# User code ends here

# Generate the graph
try:
    if '${visualizeType}' == 'stack':
        mg.render(mg.stack(), "${escapedPath}")
    else:
        mg.render(locals(), "${escapedPath}")
except Exception as e:
    print(f"Error generating graph: {e}", file=sys.stderr)
    sys.exit(1)
`;

    return template;
}

/**
 * Clean up old temporary files
 */
export async function cleanupOldTempFiles(): Promise<void> {
    const tempDir = os.tmpdir();
    const files = fs.readdirSync(tempDir);
    
    const now = Date.now();
    const oneHourAgo = now - (60 * 60 * 1000);

    for (const file of files) {
        if (file.startsWith('memory_graph_temp_') || file.startsWith('memory_graph_output_')) {
            try {
                const filePath = path.join(tempDir, file);
                const stats = fs.statSync(filePath);
                
                // Delete files older than 1 hour
                if (stats.mtimeMs < oneHourAgo) {
                    await unlinkAsync(filePath);
                }
            } catch (error) {
                // Ignore errors during cleanup
            }
        }
    }
}