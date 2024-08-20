import os
import requests
import json
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the base URL using environment variables
LLM_SERVER_IP = os.getenv('LLM_SERVER_IP')
LLM_SERVER_PORT = os.getenv('LLM_SERVER_PORT')
BASE_URL = f"http://{LLM_SERVER_IP}:{LLM_SERVER_PORT}/v1/chat/completions"

COMPLETION_PHRASE = "DONE"
MAX_ATTEMPTS = 5

def execute_bash_command(command):
    """Executes a bash command and automatically responds to prompts."""
    try:
        command = f"echo 'y' | {command.strip()}"
        print(f"Executing command: {command}")
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('ISO-8859-1')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('ISO-8859-1')}"

def stream_completion(model, messages, temperature=0.7, max_tokens=-1):
    """Streams a completion request to the AI model and returns the response."""
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data), stream=True)
        response.raise_for_status()

        full_response = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line.startswith("data:"):
                    json_data = decoded_line[len("data:"):].strip()

                    if json_data and json_data != "[DONE]":
                        try:
                            data_json = json.loads(json_data)
                            content = data_json.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            if content:
                                print(content, end='', flush=True)
                                full_response += content
                                if COMPLETION_PHRASE in content:
                                    print("\n[INFO] AI indicated task completion.")
                                    return full_response, True
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                    elif json_data == "[DONE]":
                        break

        return full_response, False
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None, False

def is_task_redundant(output, user_task):
    """Checks if the task was already completed."""
    keywords = ["already installed", "no action is needed", "newly installed, 0 to remove", "is already the newest version"]
    return any(keyword in output.lower() for keyword in keywords)

def main():
    """Main function to handle the user task loop."""
    if not LLM_SERVER_IP or not LLM_SERVER_PORT:
        print("[ERROR] LLM_SERVER_IP or LLM_SERVER_PORT environment variables are not set.")
        return

    model_name = "MaziyarPanahi/BASH-Coder-Mistral-7B-Mistral-7B-Instruct-v0.2-slerp-GGUF"

    while True:
        user_task = input("Enter the task you want to perform: ").strip()
        if not user_task:
            print("[INFO] Empty task input, exiting.")
            break

        attempt = 0
        task_complete = False

        while attempt < MAX_ATTEMPTS and not task_complete:
            attempt += 1

            # Send the task to the AI to get the Bash command
            prompt_messages = [
                { "role": "system", "content": "Please provide only the command needed to complete the following task in a Bash CLI. Only provide a single command. Do not add anything else outside of bash syntax. No additional context is needed. Do not format the command with backticks or Markdown." },
                { "role": "user", "content": user_task }
            ]

            ai_response, _ = stream_completion(model_name, prompt_messages)

            if ai_response:
                # Execute the AI-provided command in bash
                print(f"\n[Executing Command]: {ai_response.strip()}")
                bash_output = execute_bash_command(ai_response.strip())
                print(f"\n[Bash Output]:\n{bash_output}\n")

                if is_task_redundant(bash_output, user_task):
                    print("[INFO] The task has already been completed. Exiting loop.")
                    task_complete = True
                    break

                # Send the output back to the AI for evaluation
                prompt_messages = [
                    { "role": "system", "content": "Evaluate the following command output and determine if the task requested was successfully completed. If it matches the task requested, respond with 'DONE'. Otherwise, suggest another command to try. Do not reply with anything other than DONE or the next bash command" },
                    { "role": "user", "content": bash_output },
                    { "role": "user", "content": f"The task was: {user_task}" }
                ]

                _, task_complete = stream_completion(model_name, prompt_messages)

                if task_complete:
                    print("[INFO] Task has been completed successfully.")
                    break
            else:
                print("[ERROR] No response from AI. Exiting.")
                break

        if not task_complete:
            print("[INFO] Maximum attempts reached or unable to complete the task. Exiting.")

if __name__ == "__main__":
    main()
