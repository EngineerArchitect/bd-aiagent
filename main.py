import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate content using Google's Gemini API.")
    parser.add_argument("prompt", type=str, help="The input prompt for the AI model.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output (prints extra details).")
    args = parser.parse_args()
  
     # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)
                
    if args.verbose:
        print(f"User prompt: {args.prompt}")
       
    # Get the prompt from command line arguments
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args.prompt
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages, args.verbose)

def generate_content(client, messages, verbose=False):
    """
    Generate content using the provided prompt
    Note: The model 'gemini-2.0-flash-001' is used for demonstration purposes.
    Args:
        client (genai.Client): The GenAI client instance.
        messages (list): A list of Content objects containing the user prompt.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
