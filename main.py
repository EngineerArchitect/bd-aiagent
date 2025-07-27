import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
     # Load environment variables from .env file
    load_dotenv()
    
    # Check if a command line argument was provided
    args = sys.argv[1:]
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    # Get the prompt from command line arguments
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages)   

def generate_content(client, messages):
    """
    Generate content using the provided prompt
    Note: The model 'gemini-2.0-flash-001' is used for demonstration purposes.
    
    Args:
        client (genai.Client): The GenAI client instance.
        messages (list): A list of Content objects containing the user prompt.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    
    response_text = response.text
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(f'Prompt tokens: {prompt_token_count}')
    print(f'Response tokens: {response_tokens}')
    print(f'Response: {response_text}')

    
if __name__ == "__main__":
    main()
