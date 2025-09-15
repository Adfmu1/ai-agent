import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_run_python_file
from functions.write_file import schema_write_file


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_run_python_file,
        schema_write_file
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def main():
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        client = genai.Client(api_key=api_key)
        
        messages = [
                types.Content(role="user", parts=[types.Part(text=prompt)])
        ]
    
        if "--verbose" in sys.argv:
            for prompt in messages:
                print("User prompt:", prompt)
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001", 
                    contents=prompt,
                    config=config
                    )

                print(response.text)
                if response.function_calls != None:
                    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
                    

                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:

            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=config
                )
            
            print(response.text)
            if response.function_calls != None:
                print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
            
            
    else:
        print("no prompt provided")
        sys.exit(1)

if __name__ == "__main__":
    main()