from google.genai import types
import os

def get_files_info(working_directory, directory="."):
    dir = os.path.abspath(os.path.join(working_directory, directory))
    if not dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(dir):
        return f'Error: "{directory}" is not a directory'

    try:
        ret_string = []
        
        ret_string.append(f"Result for {"current" if directory == "." else directory} directory:")

        for file in os.listdir(dir):
            file_path = dir + "/" + file
            ret_string.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
            
        return "\n".join(ret_string)
    except Exception as e:
        return f"Error listing files: {e}"
    
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