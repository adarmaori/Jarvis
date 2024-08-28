def create_file(path, content = None):
    try:
        with open(path, 'w+') as f:
            if content:
                f.write(content)
            else:
                f.write('')
    except Exception as e:
        return f"Error creating file: {e}"

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def append_file(path, content):
    try:
        with open(path, 'a') as f:
            f.write(content)
    except Exception as e:
        return f"Error appending to file: {e}"



tools = {
    "create_file": create_file,
    "read_file": read_file,
    "append_file": append_file
}