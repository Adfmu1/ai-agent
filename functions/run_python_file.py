import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    f_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not f_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(f_path):
        return f'Error: File "{file_path}" not found.'
    if not f_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        output = subprocess.run(["python", f_path], timeout=30, capture_output=True)
        ret_string = f"STDOUT: {output.stdout if output.stdout != b'' else "No output produced"} STDERR: {output.stderr}{f" Process exited with code {output.returncode}" if output.returncode != 0 else ""}"

        return ret_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    