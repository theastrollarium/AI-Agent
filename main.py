import os
from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key not found")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    max_iterations = 20
    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(response.choices[0].message.content)

        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception(f"Empty result from {tool_call.function.name}")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            return


    print(f"Error: Maximum number of iterations ({max_iterations}) reached without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
