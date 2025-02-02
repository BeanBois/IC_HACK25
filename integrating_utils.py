from GameGraphics.twod_graphics.utilities import *
from GameEngine.test import InteractiveChatGame
from GameGraphics.twod_graphics.config import *
import os 
import pygame as pg
import time

class Admin(GameObject):
    def __init__(self, name, game_map: GameMap, engine:InteractiveChatGame, interactive=True):
        super().__init__(name, game_map, interactive)
        self.text_engine = engine
        self.base_sprites_dir = os.getcwd() + '/GameGraphics/twod_graphics/Assets/'
        self.sprite_file = self.base_sprites_dir + 'npc/admin.png'
        self.sprite = pg.image.load(self.sprite_file)
        self.dialouge = None
        self._init_engine()
        self._init_chatbox()
    
    def _init_engine(self):
        dialouge = self.text_engine.init_ai()
        self.dialouge = dialouge
        print(type(self.dialouge))
        
    def _init_chatbox(self):
        chatbox_sprite_file = self.base_sprites_dir + 'chatbox/chatbox.png'
        self.chatbox = pg.image.load(chatbox_sprite_file)
        font_path = self.base_sprites_dir + 'fonts/chatbox_fontsv1.ttf'
        self.font = pg.font.Font(font_path, 36) 
    
    def interact(self, player,screen):
        chatbox_position = ( screen.screen_width//100, 7.5 * screen.screen_height//10)  # Adjust the position as needed
        chatbox_width = 10 * screen.screen_width // 10  # 90% of screen width
        chatbox_height = 2 * screen.screen_height // 10  # 20% of screen height
        font_size = self.font.size("A")[0] + 2
        max_letters_per_line = chatbox_width/(font_size) 
        
        options = ["Talk", "Respond"]
        selected_option = 0  # Index of the selected option
        resized_chatbox = pg.transform.scale(self.chatbox, (chatbox_width, chatbox_height))
        choice_active = True
        while choice_active:
            screen.screen.blit(resized_chatbox, chatbox_position)
            
            # Display choices
            for i, option in enumerate(options):
                color = (0, 0, 255) if i == selected_option else (0, 0, 0)  # Highlight selection
                option_surface = self.font.render(option, True, color)
                option_position = (chatbox_position[0] + 50, chatbox_position[1] + 30 + i * 40)
                screen.screen.blit(option_surface, option_position)

            screen.map_controller.display.flip()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pg.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pg.K_x:
                        choice_active = False  # Confirm selection
        # Resize the chatbox image
        if selected_option == 0:
            screen.screen.blit(resized_chatbox, chatbox_position)
            
            words = self.dialouge.split()

            # Initialize variables for pagination
            current_line = ""
            dialogue_lines = []
            for word in words:
                if len(current_line) + len(word) + 1 <= max_letters_per_line:
                    current_line += word + " "
                else:
                    dialogue_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                dialogue_lines.append(current_line.strip())

            # Paginate the dialogue into sets of 2 lines
            paginated_dialogue = [dialogue_lines[i:i + 2] for i in range(0, len(dialogue_lines), 2)]

            # Display each set of 2 lines and wait for the player to press X to continue
            for page in paginated_dialogue:
                # Clear the chatbox area
                screen.screen.blit(resized_chatbox, chatbox_position)

                # Render and display the current page (2 lines)
                text_position_y = chatbox_position[1] + 30  # Starting Y position for text
                for line in page:
                    text_surface = self.font.render(line, True, (0, 0, 0))  # Black text
                    text_position = (chatbox_position[0] + 30, text_position_y)
                    screen.screen.blit(text_surface, text_position)
                    text_position_y += self.font.get_height() + 5  # Move to the next line

                # Update the display
                screen.map_controller.display.flip()

                # Wait for the player to press the X key to continue
                waiting_for_input = True
                while waiting_for_input:
                    for event in pg.event.get():
                        if event.type == pg.KEYDOWN and event.key == pg.K_x:  # Wait for the X key to continue
                                waiting_for_input = False
        else:
            # After all dialogue is displayed,  show an input box for the player's response
            player_response = ""  # Variable to store the player's response
            input_active = True  # Flag to indicate if the input box is active
            while input_active:
                # Clear the chatbox area
                screen.screen.blit(resized_chatbox, chatbox_position)

                # Render the prompt text
                prompt_text = "Your response:"
                prompt_surface = self.font.render(prompt_text, True, (0, 0, 0))  # Black text
                prompt_position = (chatbox_position[0] + 30, chatbox_position[1] + 30)
                screen.screen.blit(prompt_surface, prompt_position)

                # Render the player's current response
                response_surface = self.font.render(player_response, True, (0, 0, 0))  # Black text
                response_position = (prompt_position[0], prompt_position[1] + self.font.get_height() + 5)
                screen.screen.blit(response_surface, response_position)

                # Update the display
                screen.map_controller.display.flip()

                # Handle events for text input
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:  # Enter key to submit the response
                            input_active = False
                        elif event.key == pg.K_BACKSPACE:  # Backspace to delete the last character
                            player_response = player_response[:-1]
                        else:
                            # Add the typed character to the response
                            player_response += event.unicode
            self.dialouge = self.text_engine.get_ai_response(player_response)
            screen.map_controller.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_x}))
            # Return the player's response (optional)
            return player_response
    

    def create_object(self,):
        pass
         
    def check_end(self):
        if "Congratulation" in self.dialouge or "Remember, in real emergency" in self.dialouge:
            return True
            
    

class Door(GameObject):
    
    def __init__(self, name, game_map: GameMap, interactive=True, walkable = True):
        super().__init__(name, game_map, interactive)
        self.walkable = walkable
        self.base_sprites_dir = os.getcwd() + '/GameGraphics/twod_graphics/Assets/'
        self.sprite_file = self.base_sprites_dir + 'map/door.png'
        sprite = pg.image.load(self.sprite_file)
        self.sprite = pg.transform.scale(sprite, (MAP_RATIO, MAP_RATIO))
    
    def interact(self, player, screen):
        pass
    
    def on_it(self,player):
        if player.x == self.x and player.y == self.y:
            return True
        return False
         
   
# class Pokemon(GameObject):
#  pass