from config import MAX_CHARS
import os
from google.genai import types


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
            content = f.read(MAX_CHARS + 1)

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: Could not read file "{file_path}": {str(e)}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
