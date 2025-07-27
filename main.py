import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    
    # Check if a command line argument was provided
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        print("Usage: python main.py \"Your prompt question here\"")
        sys.exit(1)
    
    # Get the prompt from command line arguments
    prompt = sys.argv[1]
    
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Configure GenAI client with the API key
    client = genai.Client(api_key=api_key)
    
    # Generate content using the provided prompt
    # Note: The model 'gemini-2.0-flash-001' is used for demonstration purposes.
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=prompt
    )
    
    response_text = response.text
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(f'Prompt tokens: {prompt_token_count}')
    print(f'Response tokens: {response_tokens}')
    print(f'Response: {response_text}')
    
if __name__ == "__main__":
    main()
