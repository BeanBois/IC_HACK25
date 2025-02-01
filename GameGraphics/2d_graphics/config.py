# ratios
MAP_RATIO = 60
PLAYER_RATIO = MAP_RATIO//2
OBJECT_RATIO = MAP_RATIO//2

# Colour for objects
WALL_COLOUR = (0, 0, 0) # black
PATH_COLOUR = (255, 255, 255) # white
PLAYER_COLOUR = (  0,   0, 255) # blue
INTERACTIVE_OBJECT_COLOUR = (  255,   0, 0) # red
PASSIVE_OBJECT_COLOUR = (  0,   255, 0) # green


# characters
WALL_CHAR = '*'
PATH_CHAR = '.'
OBJECT_CHAR = 'o'
PLAYER_CHAR = 'x'

from enum import Enum
class PLAYER_ORIENTATION(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3