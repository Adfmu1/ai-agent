import os

def get_files_info(working_directory, directory="."):
    dir = os.path.join(directory, working_directory)
    if not os.path.exists(dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    ret_string = []

    for file in os.listdir(dir):
        file_path = dir + "/" + file
        ret_string.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        
    return "\n".join(ret_string)
