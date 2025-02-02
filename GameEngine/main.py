import getpass
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import yaml
import personalityres as personalities 


def format_questions(questions):
    return "\n".join([f"{i+1}. {question}" for i, question in enumerate(questions)])

if not os.environ.get("ANTHROPIC_API_KEY"):
  os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")
  # Load the YAML file
with open("event.yml", "r") as file:
    prompt_data = yaml.safe_load(file)

model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

player = personalities.player_sheet("csv/BFI_44.csv")



def analyse_data(history, act_context):
    model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    for i in range(0,len(history),2):
        context = [
            SystemMessage("you can answer only with a response  float between 5 and 0, where 5 is you fully agree and 0 is you fully disagree disagree"),
            HumanMessage("Take this context, qustion, answer, and rate the answer with float between 5 and 0, where 5 is you fully agree and 0 is you fully disagree disagree for the following criteria, if you dont know or dont understand return 0, asnwer must only contain numbers, return 0: " + format_questions(player.questions) + "Question: " + str(history[i])  + " Answer: " + str(history[i+1])  + " Context: " + str(act_context))]
    print(model2.invoke(context).content)

# Get the AI's response
#map = model.invoke([HumanMessage(content="make me ive me a maze (nxn) with wall char '*' and path char '.'")])
#print(map)

print("Type 'exit' to end the game.\n\n")

# Initialize messages outside the loop to preserve conversation history
history = []  # Stores the full conversation history
i = 0

# Main Loop
while i < 1:
    i = i + 1
    act_key = f"act{i}"
    
    # Add system message for context
    context = SystemMessage(content=str({**prompt_data['prompt']['global'], **prompt_data['prompt'][act_key]}))
    history.append(context)  # Add system message to history
    
    # Add initial human message
    history.append(HumanMessage(content="hello"))  # Add user input to history
    
    # Get AI's response to the initial message
    response = model.invoke(history)  # Pass the full history to the model
    print(f"Android: {response.content}\n")
    history.append(AIMessage(content=response.content))  # Add AI response to history
    
    # Inner loop for conversation
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the game if the user types 'exit'
        if user_input.lower() == "exit":
            print("Goodbye! The game has ended.")
            break
        
        # Add user input to conversation history
        history.append(HumanMessage(content=user_input))
        
        # Get the AI's response
        response = model.invoke(history)  # Pass the full history to the model
        
        # Print the AI's response
        print(f"Android: {response.content}\n")
        
        # Add the AI's response to conversation history
        history.append(AIMessage(content=response.content))
    
    # Analyse data after the conversation ends
    analyse_data(history, prompt_data['prompt'][act_key]['act_context'])