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

def analyse_data(aimessages, messages, act_context):
    model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    for i in range(len(aimessages)):
        context = [
            SystemMessage("you can answer only with a response  float between 5 and 0, where 5 is you fully agree and 0 is you fully disagree disagree"),
            HumanMessage("""Take this context, qustion, answer, and rate the answer with 5 or 0 for the following criteria, if you dont know or dont understand, asnwer must only contain numbers, return 0:'
                         1.player Is talkative
                         2.Tends to find fault with others
                         3.Does a thorough job
                         4. Is depressed, blue
                         5.Is original, comes up with new ideas"""+ "Question:"  + aimessages[i] + "Asnwer" + messages[i] + "Context" + act_context)
    ]
    print(model2.invoke(context).content)

# Get the AI's response
#map = model.invoke([HumanMessage(content="make me ive me a maze (nxn) with wall char '*' and path char '.'")])
#print(map)

print("Type 'exit' to end the game.\n\n")


i=0
#Main Loop
while i < 1:
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
    analyse_data(aimessages,messages,prompt_data['prompt'][act_key]['act_context'])
