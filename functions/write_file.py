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

