from GameGraphics.twod_graphics.utilities import *
from GameEngine.test import InteractiveChatGame
import os 
import pygame as pg
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
        
    def _init_chatbox(self):
        chatbox_sprite_file = self.base_sprites_dir + 'chatbox/chatbox.png'
        self.chatbox = pg.image.load(chatbox_sprite_file)
        font_path = self.base_sprites_dir + 'fonts/chatbox_fontsv1.ttf'
        self.font = pg.font.Font(font_path, 36)
        
    
    def interact(self, player,screen):
        chatbox_position = (100, 400)  # Adjust the position as needed
        screen.screen.blit(self.chatbox, chatbox_position)
        text_surface = self.font.render(self.dialouge, True, (255, 255, 255))  # White text
        text_position = (chatbox_position[0] + 20, chatbox_position[1] + 20)  # Offset from chatbox position
        screen.screen.blit(text_surface, text_position)
        screen.map_controller.display.flip()