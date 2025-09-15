from google.genai import types
import os

def write_file(working_directory, file_path, content):
    f_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not f_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{f_path}" as it is outside the permitted working directory'
        
    try:
        file_dir = "/".join(f_path.split("/")[:-1])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        
        with open(f_path, "w") as w_file:
            w_file.write(content)
            
        return f'Successfully wrote to "{f_path}" ({len(content)} characters written)'
        
        
    except Exception as e:
        return f"Error writing to file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a content given as an argument to a file in given filepath, which is constrained to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Is a relative path to the file from working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to a file in a given file_path in working directory."
            ),
        },
    ),
)