import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(file_path):
        f'Error: File not found or is not a regular file: "{file_path}"'
    if not file_path.startswith(os.path.abspath(working_directory)):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
    try:
        file_content = ""

        with open(file_path) as r_file:
            for line in r_file:
                file_content += line
                    
            if len(file_content) >= 10000:
                file_content = file_content[:10000]
                file_content += f"[...File {f"{file_path}"} truncated at 10000 characters]"
                
                    
        return file_content
                    
    except Exception as e:
        return f"Error getting file content: {e}"
                