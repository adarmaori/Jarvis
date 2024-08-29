import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import openai
import warnings
from transcriber import Transcriber
import os
# from tools_temp import tools as tools_temp
from tools.todoist import commands as todoist_commands

tools_temp = { # TODO: make this external and more complete
    **todoist_commands.index,
}

warnings.filterwarnings("ignore")  # Like a boss

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up OpenAI key
with open(os.path.join("keys", "openai_api.key"), "r") as f:
    openai.api_key = f.read().strip()

# Function to get response from GPT-4
def get_gpt4_response(messages, tools) -> tuple[str | None, list[dict] | None]:
    response = openai.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        max_tokens=150,
        tools=tools
    )
    
    match response.choices[0].finish_reason:
        case "stop":
            return response.choices[0].message, None
        case "tool_calls":
            return response.choices[0].message, response.choices[0].message.tool_calls
    return None, None

# def add_numbers(num1, num2):
#     return num1 + num2

# Main function to run the voice-chat terminal application
def main():
    # Load tools from JSON file in the same directory as the script
    with open(os.path.join(script_dir, "../tools/todoist/commands.json"), "r") as f:
        tools = json.load(f)
    
    conversation = [
        {
            "role": "system",
            "content": """
            You are an AI assistant designed to help the user achieve what they want faster. 
            Right now you only have one user, who is a programmer who mostly uses Python and SystemVerilog. 
            The user will give you instructions by voice and you will carry them out to the best of your ability. 
            If you don't find it useful to call a tool or a function, just reply to the user. 
            If you do make some action, make sure to let the user know what you do before and after you do it.
            Do you understand these instructions?
            """
        },
        {
            "role": "assistant",
            "content": "Yes, I understand"
        }
    ]

    transcriber = Transcriber()

    def on_transcription(transcribed_text):
        print(transcribed_text)
        conversation.append({"role": "user", "content": transcribed_text})
        response, tool_calls = get_gpt4_response(conversation, tools)
        
        if tool_calls:
            print(response.content)
            conversation.append(response)
            for tool_call in tool_calls:
                if tool_call.function.name in tools_temp:
                    arguments = json.loads(tool_call.function.arguments)
                    result = tools_temp[tool_call.function.name](**arguments)
                    tool_response = {
                        "role": "tool",
                        "content": json.dumps({
                            **arguments,
                            "result": result
                        }),
                        "tool_call_id": tool_call.id
                    }
                    conversation.append(tool_response)
                    
                    follow_up_response, _ = get_gpt4_response(conversation, tools)
                    if follow_up_response:
                        print(follow_up_response.content)
                        conversation.append({"role": "assistant", "content": follow_up_response.content})
        elif response:
            print(response.content)
            conversation.append({"role": "assistant", "content": response.content})

    print("Press and hold the spacebar to start recording, release it to stop.")
    print("Press Ctrl+C to exit the program.")

    try:
        while True:
            transcriber.listen(on_transcription)
    except KeyboardInterrupt:
        print("\nExiting program.")

if __name__ == "__main__":
    main()
