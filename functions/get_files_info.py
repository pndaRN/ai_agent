import os
from google.genai import types

def get_files_info(working_directory, directory = "."):
    try:

        full_directory = os.path.join(working_directory, directory)

        abs_full = os.path.abspath(full_directory)
        abs_working = os.path.abspath(working_directory)

        if not abs_full.startswith(abs_working):
            return f'Error, Cannot list "{directory}" as it is an outside the permitted working directory'

        if not os.path.exists(full_directory):
            return f'Error: "{directory}" does not exist' 

        if not os.path.isdir(full_directory): 
            return f'Error: "{directory}" is not a directory'

        lines = []

        for item in sorted(os.listdir(full_directory)):
            item_path = os.path.join(full_directory, item)
            item_size = os.path.getsize(item_path)
            is_dir= os.path.isdir(item_path)

            line = f"- {item}: file_size={item_size}, is_dir={is_dir}"

            lines.append(line)

        return "\n".join(lines)
    
    except PermissionError as e:
        return f"Error: Permission denied - {str(e)}"
    except FileNotFoundError as e:
        return f"Error: File or directory not found - {str(e)}"
    except OSError as e:
        return f"Error: OS error - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

