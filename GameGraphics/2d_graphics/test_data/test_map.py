# Prompt : give me a maze (nxn) with wall char "*" and path char "."
TEST_MAP  = """
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
# test_map  = """
# ***************
# *.....*.....*.*
# *.*.*****.*.*.*
# *.*.......*...*
# *.*.*****.*.*.*
# *...........*.*
# ***.*****.*****  
# *...*.....*...*
# *.*****...*.*.*
# *.............*
# *****.*****.*.*
# *.....*.......*
# *.....*.......*
# *.....*.......*
# ***************
# """

# def expand_path_width(test_map):
#     lines = test_map.split('\n')
#     new_maze = []
#     for i in range(1,len(lines)-1):
#         for j in range(1,len(lines[i])-1):
#             if lines[i][j] == '.':
#                 if lines[i-1][j] == '*':
                    

# TEST_MAP = expand_path_width(test_map)
# print(TEST_MAP)