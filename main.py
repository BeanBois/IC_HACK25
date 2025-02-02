from GameGraphics.twod_graphics.utilities import *
from GameGraphics.twod_graphics.test_data.test_map import TEST_MAP
from integrating_utils import *
from GameEngine.test import InteractiveChatGame

if __name__ == "__main__":
    screen = GameScreen(TEST_MAP,pg)
    player =  Player(screen.game_map)
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