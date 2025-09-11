import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    if len(sys.argv) > 1:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        client = genai.Client(api_key=api_key)
    
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=sys.argv[1])
        
        print(response.text)

        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    else:
        print("no prompt provided")
        sys.exit(1)

if __name__ == "__main__":
    main()