import * as vscode from 'vscode';

async function newFile(name: string) {
    let filename;
    if (!name) {
        await vscode.window.showInputBox({ prompt: 'Enter the name of the file'}).then((value) => {
            if (!value) {
                vscode.window.showErrorMessage('No name was provided');
                return;
            }
            filename = value;
        });
    }
    else {
        filename = name;
    }
    const editor = vscode.window.activeTextEditor;
    let directory;
    if (!editor) {
        directory = null;  // TODO: get the current working directory
    }
    else {
        directory = editor.document.uri.fsPath.split('/').slice(0, -1).join('/');
    }
    //create the file
    const fileUri = vscode.Uri.file(`${directory}/${filename}`);
    vscode.workspace.fs.writeFile(fileUri, new Uint8Array());
}

function renameFile(path: string, newName: string) {
    if (!path) {
        vscode.window.showInputBox({ prompt: 'Enter the path of the file to rename' }).then((value) => {
            if (!value) {
                vscode.window.showErrorMessage('No path was provided');
                return;
            }
            path = value;
        });
    }
}



export { newFile };