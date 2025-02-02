#!/usr/bin/env python3.10

import random
from make_maze import make_maze
from config import *
import pygame as pg # type: ignore
import math
import os

round_down = lambda x : math.floor(x)
class Game:
    pass

# this is where updates cascades from player interaction
class GameMap:
    
    def __init__(self,map_string):
        self.map_matrix = self._str_to_mtx(map_string)
        self.path_points = self._find_map(PATH_CHAR)
        self.objects = dict()
    
    # needs changing
    def player_facing_obj(self, player):
        player_pos = self.get_player()
        fn = None
        if player.orientation == PLAYER_ORIENTATION.NORTH:
            fn = lambda point : point[0] + 1 == player_pos[0] and point[1] == player_pos[1]
        elif player.orientation == PLAYER_ORIENTATION.SOUTH: 
            fn = lambda point : point[0] - 1 == player_pos[0] and point[1] == player_pos[1]
        elif player.orientation == PLAYER_ORIENTATION.EAST:
            fn = lambda point : point[1] + 1 == player_pos[1] and point[0] == player_pos[0]
        elif player.orientation == PLAYER_ORIENTATION.WEST:
            fn = lambda point : point[1] - 1 == player_pos[1] and point[0] == player_pos[0]
        for position in self.objects.keys():
            if fn(position):
                print(position)
                return True
        return False
    
    # needs changing
    def get_object_near_player(self,player):
        player_pos = self.get_player()
        fn = None
        if player.orientation == PLAYER_ORIENTATION.NORTH:
            fn = lambda point : point[0] + 1 == player_pos[0] and point[1] == player_pos[1]
        elif player.orientation == PLAYER_ORIENTATION.SOUTH: 
            fn = lambda point : point[0] - 1 == player_pos[0] and point[1] == player_pos[1]
        elif player.orientation == PLAYER_ORIENTATION.EAST:
            fn = lambda point : point[1] + 1 == player_pos[1] and point[0] == player_pos[0]
        elif player.orientation == PLAYER_ORIENTATION.WEST:
            fn = lambda point : point[1] - 1 == player_pos[1] and point[0] == player_pos[0]
        for position in self.objects.keys():
            if fn(position):
                return self.objects[position]
        return None
    
    def get_player(self):
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == PLAYER_CHAR:
                    return (i,j)
        
    def _str_to_mtx(self, map_string):
        map_string = map_string.strip()
        map_lines = map_string.split('\n')
        map_matrix = []
        for line in map_lines:
            map_matrix.append(list(line))
        
        return map_matrix
    
    def is_movable_position(self, x,y):
        return self.map_matrix[x][y] == PATH_CHAR

    # returns a set of tuples, which is the location of the elements
    def _find_map(self,element):
        path_points = set()
        # Loop through the 2D array
        for x in range(len(self.map_matrix)):
            for y in range(len(self.map_matrix[x])):
                if self.map_matrix[x][y] == element:
                    path_points.add((x, y)) 
        return path_points
    
    def add_object(self,obj,x,y):
        self.objects[(x,y)] = obj
        self.update_map(OBJECT_CHAR, x, y)
     
    def update_map(self,element,x,y):
        self.map_matrix[x][y] = element
        if element is PATH_CHAR:
            self.path_points.add((x,y))
        else:
            if (x,y) in self.path_points:
                self.path_points.remove((x,y))

    def draw_map(self,screen:pg.Surface):
        MINI_TILE_SIZE = 5
        offset_x = 0
        offset_y = 0
        for row_index, row in enumerate(self.map_matrix):
            for col_index, cell in enumerate(row):
                if cell == WALL_CHAR:
                    colour = WALL_COLOUR
                elif cell == PATH_CHAR:
                    colour = PATH_COLOUR
                elif cell == PLAYER_CHAR:
                    colour = PLAYER_COLOUR
                elif cell == OBJECT_CHAR:
                    obj = self.objects[(row_index, col_index)]
                    colour = INTERACTIVE_OBJECT_COLOUR if obj.interactive else PASSIVE_OBJECT_COLOUR 
                else:
                    colour = (255,0,0)
                rect = pg.Rect(
                    offset_x + (col_index * MINI_TILE_SIZE),
                    offset_y + (row_index * MINI_TILE_SIZE),
                    MINI_TILE_SIZE,
                    MINI_TILE_SIZE
                )
                pg.draw.rect(screen, colour, rect)
        # by default map is in the top right corner
        
# controls the graphic of the game screen
# calls function that allows drawing of the map
class GameScreen:

    def __init__(self, map_string,pg):
        self.map_controller = pg
        self.game_map = GameMap(map_string)
        self._make_screen()
        self.player = None
    
    def set_player(self,player):
        self.player = player
        
    def add_element(self, element, x, y):
        self._make_element(element, x, y)
    
    def _make_screen(self):
        self._init_screen() # initialise the screen
    
    def fill_screen(self):
        for x in range(len(self.game_map.map_matrix)):
            for y in range(len(self.game_map.map_matrix[x])):
                self._make_element(self.game_map.map_matrix[x][y], y, x)
        self.game_map.draw_map(self.screen)
        self.map_controller.display.flip()
        # Update the display after drawing all elements
                
    def _init_screen(self):
        self.map_controller.init()
        self.screen_width = len(self.game_map.map_matrix[0]) * MAP_RATIO 
        self.screen_height = len(self.game_map.map_matrix) * MAP_RATIO
        self.screen = self.map_controller.display.set_mode((self.screen_width, self.screen_height))
    
    def _make_element(self, element, y, x):
        if element is WALL_CHAR:
            self._make_wall(y, x)
        if element is PATH_CHAR:
            self._make_path(y, x)
        if element is PLAYER_CHAR:
            self._make_player(y, x)
        if element is OBJECT_CHAR:
            self._make_object(y, x)
        
    def _make_object(self,x,y):
        obj = self.game_map.objects[(y,x)]
        color = INTERACTIVE_OBJECT_COLOUR if obj.interactive else PASSIVE_OBJECT_COLOUR
        self.map_controller.draw.rect(self.screen, color, obj.figure)
        
    # function creates a map from a map in matrix form
    def _make_wall(self, x, y):
        wall = self.map_controller.Rect(x * MAP_RATIO, y * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        self.map_controller.draw.rect(self.screen, WALL_COLOUR, wall)
        
    def _make_path(self, x, y):
        path = self.map_controller.Rect(x * MAP_RATIO, y * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        self.map_controller.draw.rect(self.screen, PATH_COLOUR, path)

    def _make_player(self,x,y):
        player = self.map_controller.Rect(x * MAP_RATIO, y * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        sprite = self.player.get_curr_sprite()
        scaled_sprite = self.map_controller.transform.scale(sprite, (player.width, player.height))
        # Draw the scaled sprite onto the screen at the player rectangle's position
        self.screen.blit(scaled_sprite, player.topleft)
    
        # Optional: Draw the rectangle outline for debugging (remove if not needed)
        self.map_controller.draw.rect(self.screen, PLAYER_COLOUR, player, 1)  
        # self.map_controller.draw.rect(self.screen, PLAYER_COLOUR, player)
        
# unimplemented
class CameraComponent:
    """ The camera object that will be used to render the scene and interact """
    def __init__(self,width,height,screen_size):
        self.camera = pg.Rect((0,0),(width,height))
        self.width = width
        self.height = height
        self.screen_size = screen_size
    def apply(self,entity):
        """ Apply the camera transformation to the entity """
        return entity.rect.move(self.camera.topleft)
    def apply_rect(self,rect):
        """ mueve la posición de la surface a la pos de la camara en topleft (arriba/izquierda)"""
        return rect.move(self.camera.topleft)
    def update(self,target):
        """Targe en negativo para que en caso de llegar al extremo left (positivo), 
        el movimiento sea 0"""
        x_pos = -target.rect.centerx + self.screen_size[0] // 2
        y_pos = -target.rect.centery + self.screen_size[1] // 2
        #limit scrolling to map size
        x_pos = min(0,x_pos) #left
        y_pos = min(0,y_pos) #top
        x_pos = max(-(self.width - self.screen_size[0]),x_pos)
        y_pos = max(-(self.height - self.screen_size[1]),y_pos)
        self.camera = pg.Rect(x_pos,y_pos,self.width,self.height)


# holder class that initiates the player
# responsible for keeping track of details of the player
class Player:
    def __init__(self, game_map:GameMap, gender='male'):
        self.game_map = game_map
        x, y = random.choice(list(self.game_map.path_points))
        self.game_map.update_map(PLAYER_CHAR, x, y)
        self.x = x  # Player's x-coordinate
        self.y = y  # Player's y-coordinate
        self.inventory = []  # List to store items
        self.resources = { # define the resources
            'health': 100,  # Example resource: health
            'energy': 50    # Example resource: energy
        }

        self.orientation = PLAYER_ORIENTATION.NORTH
        
        self.moving = True
        self.interacting = False
        
        # sprite stuff
        self.gender = gender
        self.sprite_movement_count = 0
        self._make_sprites()
                
    def _make_sprites(self):
        file_path = os.getcwd()+ '/GameGraphics/2d_graphics/Assets/player/'
        sprite_file = file_path + 'boy.png' if self.gender == 'male' else 'girl.png'
        full_sprite = pg.image.load(sprite_file)
        self.sprites = []
        full_sprite_width = full_sprite.get_width()
        sprite_width = full_sprite_width//12
        sprite_height = full_sprite.get_height()
        for i in range(12):  # Assuming there are 12 sprites
            # Create a subsurface for each sprite
            sprite = full_sprite.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            self.sprites.append(sprite)
       
    def get_curr_sprite(self):
        idx = self.sprite_movement_count + 3 * self.orientation.value
        return self.sprites[idx]
        
    def get_map_coords(self):
        return round_down(self.x), round_down(self.y)
    
    def set_moving(self):
        self.moving = True
        self.interacting = False
    
    def set_interacting(self):
        self.moving = False
        self.interacting = True

    def move(self, event_key):
        """Move the player by dx and dy."""
        dx = 0
        dy = 0
        if event_key == pg.K_UP:
            if self.orientation == PLAYER_ORIENTATION.NORTH:
                self.sprite_movement_count = (1 + self.sprite_movement_count) % 3
            else:
                self.sprite_movement_count = 0
            self.orientation = PLAYER_ORIENTATION.NORTH
            dx -=1
        elif event_key == pg.K_DOWN:
            if self.orientation == PLAYER_ORIENTATION.SOUTH:
                self.sprite_movement_count = (1 + self.sprite_movement_count) % 3
            else:
                self.sprite_movement_count = 0
            self.orientation = PLAYER_ORIENTATION.SOUTH
            dx +=1
        elif event_key == pg.K_LEFT:
            if self.orientation == PLAYER_ORIENTATION.WEST:
                self.sprite_movement_count = (1 + self.sprite_movement_count) % 3
            else:
                self.sprite_movement_count = 0
            self.orientation = PLAYER_ORIENTATION.WEST
            dy -=1
        elif event_key == pg.K_RIGHT:
            if self.orientation == PLAYER_ORIENTATION.EAST:
                self.sprite_movement_count = (1 + self.sprite_movement_count) % 3
            else:
                self.sprite_movement_count = 0
            self.orientation = PLAYER_ORIENTATION.EAST
            dy +=1
        # Check if the new position is valid
        if self.game_map.is_movable_position(self.x + dx, self.y + dy):
            prev_loc = (self.x, self.y)
            self.x += dx
            self.y += dy
            self.game_map.update_map(PLAYER_CHAR, self.x, self.y)
            self.game_map.update_map(PATH_CHAR, prev_loc[0], prev_loc[1])
                  
    def add_item(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    def use_resource(self, resource, amount):
        """Use a resource (e.g., health, energy)."""
        if resource in self.resources:
            self.resources[resource] -= amount
            if self.resources[resource] < 0:
                self.resources[resource] = 0  # Ensure resource doesn't go below 0

    def get_location(self):
        """Return the player's current location as a tuple (x, y)."""
        return (self.x, self.y)

    def __str__(self):
        """Return a string representation of the player."""
        return f"Player at ({self.x}, {self.y}) with inventory: {self.inventory} and resources: {self.resources}"

class GameObject:
    def __init__(self, name, game_map: GameMap, interactive=False):
        self.game_map = game_map
        x, y = random.choice(list(self.game_map.path_points))
        self.name = name  # Name of the object
        self.x = x        # X-coordinate of the object
        self.y = y        # Y-coordinate of the object
        self.interactive = interactive  # Whether the object is interactive
        self.figure = pg.Rect(y * MAP_RATIO, x * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        self.game_map.add_object(self, self.x, self.y)
        
    def interact(self, player):
        """Interact with the object. Override this method for interactive objects."""
        if self.interactive:
            print(f"You interact with the {self.name}.")
        else:
            print(f"The {self.name} is not interactive.")

    def get_location(self):
        """Return the object's location as a tuple (x, y)."""
        return (self.x, self.y)

    def __str__(self):
        """Return a string representation of the object."""
        return f"{self.name} at ({self.x}, {self.y})"


if __name__ == "__main__":
    from test_data.test_map import TEST_MAP
    # TEST_MAP = make_maze()
    screen = GameScreen(TEST_MAP,pg)
    player =  Player(screen.game_map)
    obj1 = GameObject("Test Object", screen.game_map)
    obj2 = GameObject("Test Object", screen.game_map,interactive=True)
    screen.set_player(player)
    running = True
    clock = pg.time.Clock()
    
    while running:
        pg.event.pump()
        # Check for events (like closing the window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if player.moving and event.type == pg.KEYDOWN:
                print(screen.game_map.player_facing_obj(player))
                if event.key == pg.K_x and screen.game_map.player_facing_obj(player):
                    player.set_interacting()
                    obj = screen.game_map.get_object_near_player(player)
                    obj.interact(player)
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