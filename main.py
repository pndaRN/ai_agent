import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Get API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Setting up client
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    # Setting up content
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do i build a calculator app?"')
    content = " ".join(args)

    if verbose:
        print(f"User prompt: {content}\n")

    # Setting up list of messages
    messages = [
        types.Content(role="user", parts = [types.Part(text=content)])
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):

    # Getting response from gemini
    response = client.models.generate_content(
         model = "gemini-2.0-flash-001", 
         contents = messages
    )

    # Print response
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
