import functions.config as config
import os

def get_file_content(working_directory, file_path):
    
    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not (abs_full_path.startswith(abs_working_dir + os.sep) or abs_full_path == abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_full_path): 
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:

        with open(abs_full_path, 'r', encoding="utf-8") as f:
            content = f.read(config.MAX_CHARS + 1)

        if len(content) > config.MAX_CHARS:
            content = content[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: Could not read file "{file_path}": {str(e)}'
