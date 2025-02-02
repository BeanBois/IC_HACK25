from GameGraphics.twod_graphics.utilities import *
from GameGraphics.twod_graphics.test_data.test_map import TEST_MAP
from integrating_utils import *
from GameEngine.test import InteractiveChatGame
from GameEngine.personalityres import *
import os 
if __name__ == "__main__":
    
    screen = GameScreen(TEST_MAP,pg)
    player =  Player(screen.game_map)
    player_sheet_file = os.getcwd()+'/csv/BFI_44.csv'
    player_sheet = PlayerSheet(player_sheet_file)
    # obj1 = GameObject("Test Object", screen.game_map)
    # obj2 = GameObject("Test Object", screen.game_map,interactive=True)
    chat_engine = InteractiveChatGame()
    admin = Admin("admin",screen.game_map, chat_engine)
    screen.set_player(player)
    running = True
    clock = pg.time.Clock()
    door = None
    while running:
        pg.event.pump()
        if door is not None and door.on_it(player):
            admin.text_engine.analyse_data()
            popup_font = pg.font.Font(None, 48)  # Use a larger font for the popup
            popup_text = "The game has ended! Tabulating Result..."
            popup_surface = popup_font.render(popup_text, True, (255, 255, 255))  # White text
            popup_rect = popup_surface.get_rect(center=(screen.screen_width // 2, screen.screen_height // 2))

            # Create a semi-transparent background for the popup
            popup_background = pg.Surface((popup_rect.width + 40, popup_rect.height + 40), pg.SRCALPHA)
            pg.draw.rect(popup_background, (0, 0, 0, 200), popup_background.get_rect(), border_radius=10)  # Semi-transparent black

            # Blit the popup background and text onto the screen
            screen.screen.blit(popup_background, (popup_rect.x - 20, popup_rect.y - 20))
            screen.screen.blit(popup_surface, popup_rect)

            # Update the display
            screen.map_controller.display.flip()
            player.calculate_traits()
            profile = PersonalityReport(player_sheet.personality_result_dict)
            # Wait for a few seconds to show the popup
            pg.time.wait(3000)  
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
        screen.map_controller.display.flip()
        # Update the display
        clock.tick(60)  

    # Quit pg
    pg.quit()