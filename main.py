import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) 
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )
    
    response_text = response.text
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(f'Prompt tokens: {prompt_token_count}')
    print(f'Response tokens: {response_tokens}')
    print(f'Response: {response_text}')
    
if __name__ == "__main__":
    main()
