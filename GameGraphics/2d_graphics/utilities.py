#!/usr/bin/env python3.10

from config import *
import pygame # type: ignore

class Map:

    def __init__(self, map_string):
        self.map_controller = pygame
        self.map_matrix = self._str_to_mtx(map_string)
        self._make_screen()
    
    def _str_to_mtx(self, map_string):
        map_string = map_string.strip()
        map_lines = map_string.split('\n')
        map_matrix = []
        for line in map_lines:
            map_matrix.append(list(line))
        
        return map_matrix
    
    def step(self):
        pass
    
    def _make_screen(self):
        self._init_screen() # initialise the screen
        print("screen made")
    
    def fill_screen(self):
        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[y])):
                print('making')
                self._make_element(self.map_matrix[y][x], x, y)
        
        # Update the display after drawing all elements
                
    def _init_screen(self):
        self.map_controller.init()
        self.screen_width = len(self.map_matrix[0]) * MAP_RATIO 
        self.screen_height = len(self.map_matrix) * MAP_RATIO
        self.screen = self.map_controller.display.set_mode((self.screen_width, self.screen_height))
    
    def _make_element(self, element, x, y):
        if element is WALL_CHAR:
            self._make_wall(x, y)
        elif element is PATH_CHAR:
            self._make_path(x, y)
        print(f'el :{element}')
        
        print(f'made {element is PATH_CHAR or element is WALL_CHAR}')
    # function creates a map from a map in matrix form
    def _make_wall(self, x, y):
        wall = self.map_controller.Rect(x * MAP_RATIO, y * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        self.map_controller.draw.rect(self.screen, WALL_COLOUR, wall)
        print('made wall')
        
    def _make_path(self, x, y):
        path = self.map_controller.Rect(x * MAP_RATIO, y * MAP_RATIO, MAP_RATIO, MAP_RATIO)
        self.map_controller.draw.rect(self.screen, PATH_COLOUR, path)

if __name__ == "__main__":
    from test_data.test_map import TEST_MAP
    map = Map(TEST_MAP)
    running = True
    while running:
        # Check for events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map.fill_screen()
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()