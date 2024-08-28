import * as vscode from 'vscode';
import * as http from 'http';
import * as url from 'url';

let server: http.Server;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel("Jarvis");
	outputChannel.show(true);
	outputChannel.appendLine('Hello World this is the append');
	// outputChannel.appendLine('Activating extension...');

    server = http.createServer((req, res) => {
        outputChannel.appendLine('Received request: ' + req.url + ' ' + req.method);
        const parsedUrl = url.parse(req.url!, true);
        if (parsedUrl.pathname === '/') {
            // Handle the request here
			let body = '';

			req.on('data', (chunk) => {
				body += chunk.toString();
			});

			req.on('end', () => {
				try {
					const parsedBody = JSON.parse(body);
					outputChannel.appendLine('Parsed body: ' + JSON.stringify(parsedBody));
					const command = parsedBody.command;
					outputChannel.appendLine('Parsed Command: ' + command);

					if (command === 'newfile') {
						const folderUri = vscode.workspace.workspaceFolders![0].uri;
						const filename = parsedBody.filename;
						outputChannel.appendLine('Creating new file: ' + filename);
						const newFileUri = vscode.Uri.joinPath(folderUri, filename);
						vscode.workspace.fs.writeFile(newFileUri, new Uint8Array());
					}

				} catch (error: any) {
					outputChannel.appendLine('Error parsing body: ' + error.message);
				}
			});

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: 'Request received' }));
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Not Found');
        }
    });
	
	outputChannel.appendLine('Creating Server...');
    server.listen(3000, () => {
        outputChannel.appendLine('Server is listening on port 3000');
    });

    context.subscriptions.push({
        dispose: () => {
            if (server) {
                server.close(() => {
                    outputChannel.appendLine('Server closed');
                });
            }
        }
    });
}

export function deactivate() {
    if (server) {
        server.close(() => {
            outputChannel.appendLine('Server closed');
        });
    }
}