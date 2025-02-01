# Prompt : give me a maze (nxn) with wall char "*" and path char "."
test_map  = """
***************
*.....*.....*.*
*.*.*****.*.*.*
*.*.......*...*
*.*.*****.*.*.*
*...........*.*
***.*****.*****  
*...*.....*...*
*.*****...*.*.*
*.............*
*****.*****.*.*
*.....*.......*
***************
"""


def expand_path_width(test_map):
    # Convert the map to a list of lines for easier manipulation
    map_lines = test_map.splitlines()
    new_map = [list(line) for line in map_lines]

    # Get the dimensions of the map
    num_rows = len(map_lines)
    num_cols = len(map_lines[0])

    # Function to check if a point is inside the map
    def is_inside(x, y):
        return 0 <= x < num_rows and 0 <= y < num_cols

    # Loop through the map to expand paths
    for i in range(num_rows):
        for j in range(num_cols):
            if map_lines[i][j] == '.':
                # Expand the path by replacing adjacent cells
                for di in range(-1, 2):  # -1, 0, 1
                    for dj in range(-1, 2):  # -1, 0, 1
                        ni, nj = i + di, j + dj
                        if is_inside(ni, nj):
                            new_map[ni][nj] = '.'

    # Convert the modified map back to a string
    expanded_map = "\n".join("".join(line) for line in new_map)
    return expanded_map

# PATH_WIDTH = 3
# def in_bounds(x, y, maze_height, maze_width):
#     return 0 <= x < maze_height and 0 <= y < maze_width
# def widen_paths(maze):
#     maze_height = len(maze)
#     maze_width = len(maze[0])
#     # Loop through the maze, expanding each path
#     for x in range(1, maze_height - 1, 2):
#         for y in range(1, maze_width - 1, 2):
#             if maze[x][y] == '.':
#                 # Expand the path horizontally and vertically
#                 for i in range(-PATH_WIDTH//2, PATH_WIDTH//2 + 1):
#                     for j in range(-PATH_WIDTH//2, PATH_WIDTH//2 + 1):
#                         if in_bounds(x + i, y + j, maze_height, maze_width):
#                             maze[x + i][y + j] = '.'
#     return maze
TEST_MAP = expand_path_width(test_map)
print(TEST_MAP)