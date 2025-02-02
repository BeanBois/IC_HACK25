import getpass
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import yaml
import personalityres as personalities 
import numpy as np
import re



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
    if len(history) % 2 != 0:
      history.pop()
    matrix= []
    model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    for i in range(0, len(history), 2):
        print('here')
        context = [
            SystemMessage("You can answer only with a response float between 5 and 0, where 5 is you fully agree and 0 is you fully disagree. Please answer using the full range"),
            HumanMessage("""For the question, asnwer and context, jusge the for each paramethers with a float beetween  0 and 5, where 0 is disagree and 5 is agree, you can answe can only contain integers, if you font know or cannot asses, let it be 0 .
                        1. answer shows player is Is talkative',
                        2 answer shows player Tends to find fault with others',
                        3. answer shows player Does a thorough job', 
                        4. answer shows player Is depressed', 
                        5. answer shows player Is original, comes up with new ideas',
                        6. answer shows player Is reserved', 
                        7. answer shows player Is helpful and unselfish with others',
                        8 answer shows player Can be somewhat careless',
                        9. answer shows player Is relaxed, handles stress well',
                        10. answer shows player Is curious about many different things', 
                        11. answer shows player Is full of energy', 
                        12. answer shows player Starts quarrels with others',
                        13. answer shows player Is a reliable worker',
                        14. answer shows player Can be tense', 
                        15 answer shows player Is ingenious, a deep thinker',
                        16. answer shows player Generates a lot of enthusiasm',
                        17. answer shows player Has a forgiving nature',
                        18. answer shows player Tends to be disorganized', 
                        19. answer shows player Worries a lot',
                        20. answer shows player Has an active imagination', 
                        21. answer shows player Tends to be quiet', 
                        22. answer shows player Is generally trusting',
                        23. answer shows player Tends to be lazy',
                        24. answer shows player Is emotionally stable,
                        25. answer shows player not easily upset', 
                        26. answer shows player Is inventive',
                        27. answer shows player Has an assertive personality',
                        28. answer shows player Can be cold and aloof',
                        29. answer shows player Perseveres until the task is finished',
                        30. answer shows player Can be moody', 
                        31. answer shows player Values artistic,
                        32. answer shows player Is a good aesthetic experiences', 
                        33. answer shows player Is sometimes shy, inhibited', 
                        34. answer shows player Is considerate and kind to almost everyone',
                        35. answer shows player Does things efficiently',
                        36. answer shows player Remains calm in tense situations', 
                        37. answer shows player Prefers work that is routine', 
                        38. answer shows player Is outgoing, sociable', 
                        39. answer shows player Is sometimes rude to others', 
                        40. answer shows player Makes plans and follows through with them', '
                        41. answer shows player Gets nervous easily',
                        42. answer shows player Likes to reflect, play with ideas', 
                        43. answer shows player Has few artistic interests',
                        44. answer shows player Likes to cooperate with others', """
                        + " Question: " + str(history[i].content)
                        + " Answer: " + str(history[i + 1].content)
                        + " Context: " + str(act_context))]
        print('there')
        response = model2.invoke(context).content
        matrix.append(response)
    print(matrix)

    for text in matrix:
        print(text)
        pattern = r'\d+\.\s(\d+)'
    
        # Find all matches and convert them to integers
        scores = [int(match) for match in re.findall(pattern, text)]
        if len(scores) != 44:
            continue
        player.update_player_sheet(scores)
    player.calculate_traits()
    player.plot_personality_type()


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