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
                         5.Is original, comes up with new ideas""""Is original, comes up with new ideas " + "Question: " + str(aimessages[i])  + " Answer: " + str(messages[i])  + " Context: " + str(act_context))]
    print(model2.invoke(context).content)

# Get the AI's response
#map = model.invoke([HumanMessage(content="make me ive me a maze (nxn) with wall char '*' and path char '.'")])
#print(map)

print("Type 'exit' to end the game.\n\n")

# Initialize messages outside the loop to preserve conversation history
messages = []
aimessages = []
i = 0

# Main Loop
while i < 1:
    i = i + 1
    act_key = f"act{i}"
    
    # Add system message for context
    context = SystemMessage(content=str({**prompt_data['prompt']['global'], **prompt_data['prompt'][act_key]}))
    messages.append(context)
    
    # Add initial human message
    messages.append(HumanMessage(content="hello"))
    
    # Get AI's response to the initial message
    response = model.invoke(messages)
    print(f"Android: {response.content}\n")
    aimessages.append(response.content)
    
    # Inner loop for conversation
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the game if the user types 'exit'
        if user_input.lower() == "exit":
            print("Goodbye! The game has ended.")
            break
        
        # Add user input to conversation history
        messages.append(HumanMessage(content=user_input))
        
        # Get the AI's response
        response = model.invoke(messages)
        
        # Print the AI's response
        print(f"Android: {response.content}\n")
        
        # Add the AI's response to conversation history
        messages.append(response)
        aimessages.append(response.content)
    
    # Analyse data after the conversation ends
    analyse_data(aimessages, messages, prompt_data['prompt'][act_key]['act_context'])