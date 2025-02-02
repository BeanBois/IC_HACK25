import getpass
import os
import yaml
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class InteractiveChatGame:
    def __init__(self, event_file="event.yml", player_csv="csv/BFI_44.csv", act_num=1, model_version="claude-3-5-sonnet-20240620"):
        # Ensure API key is set
        if not os.environ.get("ANTHROPIC_API_KEY"):
            os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")
        
        # Initialize messages outside the loop to preserve conversation history
        self.model = ChatAnthropic(model=model_version)
        self.claude_model = ChatAnthropic(model=model_version)
        self.history = []  # Stores the full conversation history
        with open(event_file, "r") as file:
            self.prompt_data = yaml.safe_load(file)

        self.act_key = f"act{1}"

        print("Game initialized")

    def init_ai(self):
        # Add system message for context
        context = SystemMessage(content=str({**self.prompt_data['prompt']['global'], **self.prompt_data['prompt'][self.act_key]}))
        self.history.append(context)  # Add system message to history
        
        # Add initial human message
        self.history.append(HumanMessage(content="hello"))  # Add user input to history
        
        # Get AI's response to the initial message
        response = self.model.invoke(self.history)  # Pass the full history to the model
        print(f"Android: {response.content}\n")
        self.history.append(AIMessage(content=response.content))  # Add AI response to history

        return response.content
        
    def extract_objects_from_response(self, response_content):
        """
        This method processes the response content and passes it to the Claude model 
        to extract structured objects.
        """
        # Define a clear and structured prompt for Claude
        prompt = f"""From the following content:
        
        {response_content}

        Please extract a list of objects mentioned in the content and provide their relevant details in the form of a dictionary.
        ignore the player and make sure the objects are objects in a building
        Each object should include:
        - 'type': Whether the object is human or non-human.
        - 'sprite image': A URL or png the sprite image.
        - If the object is human, specify their gender (male or female) based on the name (if applicable).
        
        Example output (in JSON format):
        [
        """ \
        + \
        """
        {'name': 'ObjectName', 'type': 'human', 'sprite image': 'url_or_png_of_sprite', 'gender': 'male'},
        {'name': 'ObjectName', 'type': 'non-human', 'sprite image': 'url_or_png_of_sprite'}
        ]
        """    
        
        # context = SystemMessage(content=prompt)

        claude_response = self.claude_model.invoke(prompt)  # Assuming Claude is set up for extraction
        
        extracted_objects = claude_response.content

        return extracted_objects

    def get_ai_response(self, input_text):
        self.history.append(HumanMessage(content=input_text))
        response = self.model.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content
    
    def get_history(self):
        return self.history
    
    def analyse_data(self, history):
        if len(history) % 2 != 0:
            history.pop()
            matrix= []
        model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        for i in range(0, len(history), 2):
            print('here')
            context = [
                SystemMessage("You can answer only with a response float between 5 and 0, where 5 is you fully agree and 0 is you fully disagree."),
                HumanMessage("""For the given question, answer, and context, judge each of the following parameters with an integer between 0 and 5, where 0 means "disagree" and 5 means "agree." If you don't know or cannot assess a parameter, use 0. Your response must only contain integers separated by spaces, in the order of the parameters listed below
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
                            44. answer shows player Likes to cooperate with others', 
                            45. answer shows player Is easily distracted',
                            46. answer shows player Is sophisticated in art, music, or literature' """
                            + " Question: " + str(history[i].content)
                            + " Answer: " + str(history[i + 1].content)
                            + " Context: " + str(self.prompt_data.prompt_data['prompt'][self.act_key]['act_context']))]
            response = model2.invoke(context).content
            matrix.append(response)


