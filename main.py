import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
                response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
                
                print(response.text)

                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
            print(response.text)
            
            
    else:
        print("no prompt provided")
        sys.exit(1)

if __name__ == "__main__":
    main()