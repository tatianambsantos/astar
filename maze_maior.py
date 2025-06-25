# Geração de maze "largura 3"
import numpy as np
from numpy.random import choice
import generate_maze

# Parâmetros
cell_size = 3  # largura mínima do caminho
maze_shape = (16, 16)  # labirinto em escala reduzida

""" # Geração do labirinto base
base_maze = np.ones(maze_shape, dtype=np.int8)
base_maze[1:-1, 1:-1] = choice([0, 1], size=(maze_shape[0] - 2, maze_shape[1] - 2), p=[0.7, 0.3])
base_maze[0][4] = 0  # entrada
base_maze[-1][-3] = 0  # saída """

base_maze = [
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
]
base_maze = np.array(base_maze, dtype=np.int8)

with open("base_maze.txt", "w") as f:
    for row in base_maze:
        f.write("".join(map(str, row)) + "\n")



print(base_maze)

# Expansão da base para ter caminhos com largura 3
expanded_maze = np.zeros((maze_shape[0]*cell_size, maze_shape[1]*cell_size), dtype=np.int8)

for i in range(maze_shape[0]):
    for j in range(maze_shape[1]):
        if base_maze[i, j] == 1:
            expanded_maze[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size] = 1

maze = expanded_maze



import matplotlib.pyplot as plt
plt.imshow(maze, cmap='gray_r')
plt.title("Maze com largura mínima 3")
plt.show()

# generate_maze.generate_sdf_from_maze_1(maze)
generate_maze.generate_sdf_from_maze_3(base_maze)
