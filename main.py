import getpass
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import yaml


if not os.environ.get("ANTHROPIC_API_KEY"):
  os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")
  # Load the YAML file
with open("event.yml", "r") as file:
    prompt_data = yaml.safe_load(file)


model = ChatAnthropic(model="claude-3-5-sonnet-20240620")


# Define the initial system message
messages = []
user_inputs = []  # Store all user inputs
ai_responses = []  # Store all AI responses

# Start the interactive loop
print("Welcome to the game! You are talking to an android.")
print("Type 'exit' to end the game.\n")

# AI starts the conversation
initial_prompt = "Generate an (nxn) maze with walls ('*') and paths ('.')."
initial_response = model.invoke([HumanMessage(content=initial_prompt)])

print(f"Android: {initial_response.content}\n")
ai_responses.append(initial_response.content)  # Save AI's first response
messages.append(initial_response)  # Store in conversation history

# Main Loop
while True:
    # Get user input
    user_input = input("You: ")
    
    # Exit the game if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye! The game has ended.")
        break

    user_inputs.append(user_input)  # Save user input
    messages.append(HumanMessage(content=user_input))  # Store in conversation

    # Get AI's response
    response = model.invoke(messages)
    
    print(f"Android: {response.content}\n")
    
    ai_responses.append(response.content)  # Save AI's response
    messages.append(response)  # Store response in conversation history


# At the end, you have:
# - `user_inputs` storing all user messages
# - `ai_responses` storing all AI responses
