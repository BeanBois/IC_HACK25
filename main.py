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


# Get the AI's response
#map = model.invoke([HumanMessage(content="make me ive me a maze (nxn) with wall char '*' and path char '.'")])
#print(map)

print("Type 'exit' to end the game.\n\n")


i=0
#Main Loop
while i < 3:
    messages = []
    aimessages = []
    i = i + 1
    act_key = f"act{i}"
    context = [
    SystemMessage(str({**prompt_data['prompt']['global'], **prompt_data['prompt'][act_key]})),
    HumanMessage("hello"),
    ]
    print(model.invoke(context).content)
    while True:
        # Get user input
        user_input = input("You: ")
        # Exit the game if the user types 'exit'
        
        #this message is processed to the pther model
        messages.append(HumanMessage(content=user_input).content)

        # Get the AI's response
        response = model.invoke(messages)

        # Print the AI's response
        print(f"Android: {response.content}\n")

        # Add the AI's response to the conversation
        aimessages.append(response.content)

        #send_data(response, messages, prompt_data)e

        if user_input.lower() == "exit":
            print("Goodbye! The game has ended.")
            break
        print(aimessages)
        print(messages)
        print(prompt_data['prompt'][act_key]['act_context'])
