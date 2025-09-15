from google.genai import types
import os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    f_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not f_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(f_path):
        return f'Error: File "{file_path}" not found.'
    if not f_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        output = subprocess.run(["python", f_path]+args, timeout=30, capture_output=True)
        ret_string = f"STDOUT: {output.stdout if output.stdout != b'' else "No output produced"} STDERR: {output.stderr}{f" Process exited with code {output.returncode}" if output.returncode != 0 else ""}"

        return ret_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute (run) a python file and return an output, constrained to the working directory. The args is not required.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Is a relative path to the file from working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments that can be passed to a python file. If arguments not specified, omit the property."

                ),
                description="Optional arguments that can be passed to a python file. If arguments not specified, omit the property."
            ),
        },
        required=["file_path"],
        
    ),
)