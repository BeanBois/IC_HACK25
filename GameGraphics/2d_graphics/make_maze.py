# import random

# # Constants
# # maze_width = 150
# # maze_height = 100
# path_width = 3

# # Directions for maze generation (right, down, left, up)
# DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# # Initialize the maze as a grid of walls
# def initialize_maze(maze_width,maze_height):
#     return [['*' for _ in range(maze_width)] for _ in range(maze_height)]

# # Function to check if a position is within bounds
# def in_bounds(x, y, maze_width,maze_height):
#     return 0 <= x < maze_height and 0 <= y < maze_width

# # Prim's algorithm for maze generation
# def generate_maze(maze_width,maze_height):
#     maze = initialize_maze(maze_width,maze_height)

#     # Start with a random position in the maze and mark it as a path
#     start_x = random.randrange(1, maze_height, 2)
#     start_y = random.randrange(1, maze_width, 2)
#     maze[start_x][start_y] = '.'

#     # List of walls to check, starting with the walls surrounding the start position
#     walls = [(start_x, start_y)]

#     while walls:
#         x, y = walls.pop(random.randrange(len(walls)))

#         # Shuffle directions to make the maze generation random
#         random.shuffle(DIRECTIONS)

#         # Try each direction
#         for dx, dy in DIRECTIONS:
#             nx, ny = x + dx * 2, y + dy * 2

#             # If the new position is within bounds and is a wall
#             if in_bounds(nx, ny, maze_width,maze_height) and maze[nx][ny] == '*':
#                 # Carve a path to the new position
#                 maze[nx][ny] = '.'
#                 maze[x + dx][y + dy] = '.'

#                 # Add the neighboring walls to the list
#                 walls.append((nx, ny))

#     return maze

# # Enlarge the paths to make them 3 characters wide
# def widen_paths(maze,path_width):
#     # Loop through the maze, expanding each path
#     for x in range(1, maze_height - 1, 2):
#         for y in range(1, maze_width - 1, 2):
#             if maze[x][y] == '.':
#                 # Expand the path horizontally and vertically
#                 for i in range(-path_width//2, path_width//2 + 1):
#                     for j in range(-path_width//2, path_width//2 + 1):
#                         if in_bounds(x + i, y + j,maze_width,maze_height):
#                             maze[x + i][y + j] = '.'

# # Convert maze to string format for easier printing
# def maze_to_string(maze):
#     return '\n'.join(''.join(row) for row in maze)

# # Generate and print the maze

# def make_maze(maze_width=50, maze_height=50, path_width=3):
#     maze = generate_maze(maze_width,maze_height)
#     widen_paths(maze, path_width)
#     return maze_to_string(maze)

import random

# Constants
MAZE_WIDTH = 50
MAZE_HEIGHT = 30
PATH_WIDTH = 1

# Directions for maze generation (right, down, left, up)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initialize the maze as a grid of walls
def initialize_maze():
    return [['*' for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

# Function to check if a position is within bounds
def in_bounds(x, y):
    return 0 <= x < MAZE_HEIGHT and 0 <= y < MAZE_WIDTH

# Prim's algorithm for maze generation
def generate_maze():
    maze = initialize_maze()

    # Start with a random position in the maze and mark it as a path
    start_x = random.randrange(1, MAZE_HEIGHT, 2)
    start_y = random.randrange(1, MAZE_WIDTH, 2)
    maze[start_x][start_y] = '.'

    # List of walls to check, starting with the walls surrounding the start position
    walls = [(start_x, start_y)]

    while walls:
        x, y = walls.pop(random.randrange(len(walls)))

        # Shuffle directions to make the maze generation random
        random.shuffle(DIRECTIONS)

        # Try each direction
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2

            # If the new position is within bounds and is a wall
            if in_bounds(nx, ny) and maze[nx][ny] == '*':
                # Carve a path to the new position
                maze[nx][ny] = '.'
                maze[x + dx][y + dy] = '.'

                # Add the neighboring walls to the list
                walls.append((nx, ny))

    return maze

# Enlarge the paths to make them 3 characters wide
def widen_paths(maze):
    # Loop through the maze, expanding each path
    for x in range(1, MAZE_HEIGHT - 1, 2):
        for y in range(1, MAZE_WIDTH - 1, 2):
            if maze[x][y] == '.':
                # Expand the path horizontally and vertically
                for i in range(-PATH_WIDTH//2, PATH_WIDTH//2 + 1):
                    for j in range(-PATH_WIDTH//2, PATH_WIDTH//2 + 1):
                        if in_bounds(x + i, y + j):
                            maze[x + i][y + j] = '.'

# Convert maze to string format for easier printing
def maze_to_string(maze):
    return '\n'.join(''.join(row) for row in maze)

def make_maze():
    maze = generate_maze()
    widen_paths(maze)
    return maze_to_string(maze)

if __name__ == '__main__':
    print(make_maze())