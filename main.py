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
messages = [
    SystemMessage(str(prompt_data))
]

# Start the interactive loop
print("Welcome to the game! You are talking to as android")
print("Type 'exit' to end the game.\n")

# Get the AI's response
map = model.invoke([HumanMessage(content="make me ive me a maze (nxn) with wall char '*' and path char '.'")])
print(map)

#Main Loop
while True:
    # Exit the game if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye! The game has ended.")
        break


    # Get user input
    user_input = input("You: ")

    # Add the user's message to the conversation
    #this message is processed to the pther model
    messages.append(HumanMessage(content=user_input))


    # Get the AI's response
    response = model.invoke(messages)

    # Print the AI's response
    print(f"Android: {response.content}\n")
    print(response)

    # Add the AI's response to the conversation
    messages.append(response)

    send_data(response, messages, prompt_data)

