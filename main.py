from GameGraphics.twod_graphics.utilities import *
from GameGraphics.twod_graphics.test_data.test_map import TEST_MAP
from integrating_utils import *
from GameEngine.test import InteractiveChatGame
from GameEngine.personalityres import *
import os 
# import serial
# from serial.tools import list_ports
from serialcomm import connect_and_send

if __name__ == "__main__":
    sound_file = os.getcwd()+"/GameGraphics/twod_graphics/Assets/sound/fetty_wap.mp3"
    screen = GameScreen(TEST_MAP,pg)
    player =  Player(screen.game_map)
    player_sheet_file = os.getcwd()+'/csv/BFI_44.csv'
    player_sheet = PlayerSheet(player_sheet_file)
    profile = None
    player_name = None
    # obj1 = GameObject("Test Object", screen.game_map)
    # obj2 = GameObject("Test Object", screen.game_map,interactive=True)
    chat_engine = InteractiveChatGame()
    admin = Admin("admin",screen.game_map, chat_engine)
    if 'fire' in admin.dialouge:
        fires = []
        for _ in range(10):
            x, y = random.choice(list(screen.game_map.path_points))
            position = (x,y)
            fire = Fire(position)
            screen.game_map.add_fire(x,y)
            fires.append(fire)
        fire_group = pg.sprite.Group(*fires)
            
        
    screen.set_player(player)
    running = True
    clock = pg.time.Clock()
    door = None
    while running:
        pg.event.pump()
        if door is not None and door.on_it(player):
            pg.mixer.music.load(sound_file)
            admin.text_engine.analyse_data(player_sheet)
            popup_font = pg.font.Font(None, 48)  # Use a larger font for the popup
            input_font = pg.font.Font(None, 36)  # Font for the player's input
            popup_text = "The game has ended! Please enter your name:"
            popup_surface = popup_font.render(popup_text, True, (255, 255, 255))  # White text
            popup_rect = popup_surface.get_rect(center=(screen.screen_width // 2, screen.screen_height // 2 - 50))

            # Create a semi-transparent background for the popup
            popup_background = pg.Surface((popup_rect.width + 40, popup_rect.height + 200), pg.SRCALPHA)
            pg.draw.rect(popup_background, (0, 0, 0, 200), popup_background.get_rect(), border_radius=10)  # Semi-transparent black
            pg.mixer.music.play()

            # Initialize player name input
            player_name = ""
            input_active = True

            while input_active:
                # Clear the screen
                screen.screen.fill((0, 0, 0))  # Fill with black

                # Blit the popup background and text onto the screen
                screen.screen.blit(popup_background, (popup_rect.x - 20, popup_rect.y - 20))
                screen.screen.blit(popup_surface, popup_rect)

                # Render the player's current input
                input_surface = input_font.render(player_name, True, (255, 255, 255))  # White text
                input_rect = input_surface.get_rect(center=(screen.screen_width // 2, screen.screen_height // 2 + 50))
                screen.screen.blit(input_surface, input_rect)

                # Update the display
                screen.map_controller.display.flip()

                # Handle events for text input
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:  # Enter key to submit the name
                            input_active = False
                        elif event.key == pg.K_BACKSPACE:  # Backspace to delete the last character
                            player_name = player_name[:-1]
                        else:
                            # Add the typed character to the player's name
                            player_name += event.unicode

            # Generate report after getting the player's name
            # admin.text_engine.analyse_data(player_sheet)
            # profile = PersonalityReport(player_sheet.personality_result_dict)

            # Display a final message
            final_text = f"Thank you, {player_name}! Tabulating results..."
            final_surface = popup_font.render(final_text, True, (255, 255, 255))  # White text
            final_rect = final_surface.get_rect(center=(screen.screen_width // 2, screen.screen_height // 2))

            # Clear the screen and display the final message
            screen.screen.fill((0, 0, 0))  # Fill with black
            screen.screen.blit(popup_background, (final_rect.x - 20, final_rect.y - 20))
            screen.screen.blit(final_surface, final_rect)

            # Update the display
            screen.map_controller.display.flip()
            player_sheet.calculate_traits()

            returnstr = "player_name"
            for key, value in player_sheet.personality_result_dict.items():
                returnstr += f"{key[0]:{round(value)}}"

            connect_and_send(returnstr)
            # ports = list_ports.comports()
            # for port in ports:
            #     if "USB Serial Device" in port.description:
            #         ser = serial.Serial(port.device, 115200)
            # returnstr = "player_name"  # implement name when I have it
            # for key, value in player_sheet.personality_result_dict.items():
            #     returnstr += f"{key[0]:{round(value)}}"
            # ser.write(returnstr.encode("ascii"))
            # ser.close()
            profile = PersonalityReport(player_sheet.personality_result_dict)
            # Wait for a few seconds to show the popup
            pg.time.wait(3000)  
            returnstr = f"{player_name}"
            for key, value in player_sheet.personality_result_dict.items():
                returnstr += f"{key[0]}:{round(value)}"
            connect_and_send(returnstr)
            break
        # Check for events (like closing the window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if player.moving and event.type == pg.KEYDOWN:
                print(screen.game_map.player_facing_obj(player))
                obj = screen.game_map.player_facing_obj(player)
                if event.key == pg.K_x and obj is not None:
                    player.set_interacting()
                    if obj.name == 'admin':
                        text = obj.interact(player,screen)
                        player.set_moving()
                        if obj.check_end() and door is None:
                            door = Door('door', screen.game_map, walkable=True)
                    else:
                        obj.interact(player,screen)
                else:
                    player.move(event.key)
            if player.interacting:
                pass 
        
            

        screen.fill_screen()
        fire_group.update() 
        fire_group.draw(screen.screen)
        screen.map_controller.display.flip()
        # Update the display
        clock.tick(60)  
    
    # gen and plot report 
    profile = PersonalityReport(player_sheet.personality_result_dict)
    profile.plot_personality_type()
    profile.generate_report()
    # Quit pg
    pg.quit()
    
