import getpass
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

if not os.environ.get("ANTHROPIC_API_KEY"):
  os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

# Define the initial system message
messages = [
    SystemMessage("As part of a game, you will answer as an android. The story begins with you standing at the grave of the Doctor who created you. The world is populated by robots in various forms, created for numerous purposes. Travel to places key to your memories of the Doctor, interact with the robots, and unravel the secrets behind the future the Doctor sought and what you were entrusted with.")
]

# Start the interactive loop
print("Welcome to the game! You are talking to as android")
print("Type 'exit' to end the game.\n")

#Main Loop
while True:
    # Get user input
    user_input = input("You: ")

    # Exit the game if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye! The game has ended.")
        break

    # Add the user's message to the conversation
    messages.append(HumanMessage(content=user_input))

    # Get the AI's response
    response = model.invoke(messages)

    # Print the AI's response
    print(f"Android: {response.content}\n")

    # Add the AI's response to the conversation
    messages.append(response)