import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        
    if len(sys.argv) == 1 and verbose:
        print("no prompt provided")
        sys.exit(1)
        
    for arg in sys.argv:
        if not arg == "--verbose":
            prompt = arg
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    if verbose:
        print(f"User prompt: {prompt}")
        
    messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    
    for i in range(20):
        try:
            final_response = generate_content(client, messages, verbose)
            
            if final_response:
                print("Final response:\n", final_response)
                break
            
        except Exception as e:
            print(f"Error: {e}")

        
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
    
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)        

    if not response.function_calls:
        return response.text
    
    func_responses = []

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("empty function call result")

        if "--verbose" in sys.argv:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        func_responses.append(function_call_result.parts[0])
            
    if not func_responses:
        raise Exception("no function responses generated, exiting")

    messages.append(types.Content(role="user", parts=func_responses))

            
    
    

if __name__ == "__main__":
    main()