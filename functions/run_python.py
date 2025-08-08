import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not (abs_full_path.startswith(abs_working_dir + os.sep) or abs_full_path == abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    cmd = ["python3", abs_full_path] + args

    try:
        result = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            capture_output = True,
            text = True,
            timeout = 30
        )

        stdout, stderr = result.stdout.strip(), result.stderr.strip()
        if not stdout and not stderr:
            return "No output produced."

        return_code = result.returncode
        if return_code != 0:
            return "Process exited with code {return_code}"

        return{
            f"STDOUT": result.stdout,
            f"STDERR": result.stderr,
            f"returncode": result.returncode
        }

    except Exception as e:
                return f'Error: executing Python file: {e}'

    except subprocess.TimeoutExpired as e:
        return{
            "STDOUT" : e.stdout or "",
            "STDERR" : e.stderr or "Process timed out after {} seconds".format(timeout),
            "returncode": -1
        }

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
