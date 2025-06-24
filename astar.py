import heapq
from matplotlib import pyplot as plt
import numpy as np

def load_costmap(path):
    with open(path, "r") as f:
        return np.array([[int(ch) for ch in line.strip()] for line in f])

def heuristic(a, b):
    # Distância de Manhattan (pode ser substituída por euclidiana)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(costmap, start, goal):
    rows, cols = costmap.shape
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstrói o caminho
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            if costmap[neighbor[0]][neighbor[1]] == 1:
                continue  # obstáculo

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                came_from[neighbor] = current

    return None  # Caminho não encontrado

def matriz_to_world_coords(path, size, resolution=1.0):
    """
    Converte caminho da matriz (linha, coluna) para coordenadas reais em metros.
    Assume que a matriz tem a origem no centro.
    """
    world_path = []
    offset = size // 2
    for row, col in path:
        x = (col - offset) * resolution
        y = (row - offset) * resolution
        world_path.append((x, y))
    return world_path

# --------------------------
# EXECUÇÃO

def plot_base_maze(costmap, path, start, goal):
    # Plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(costmap, cmap='Greys', origin='upper')

    if path:
        path_y, path_x = zip(*path)
        ax.plot(path_x, path_y, color='red', linewidth=2, label="Caminho A*")
        ax.scatter(start[1], start[0], c='green', s=100, label='Início')
        ax.scatter(goal[1], goal[0], c='blue', s=100, label='Objetivo')

    ax.set_title("Caminho gerado pelo A* no labirinto")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend()
    plt.tight_layout()
    plt.show()

def convert_path_to_world_coords_in_expanded_maze(cell_size=3, resolution=1.0):
    """
    Converte um caminho baseado na matriz base_maze (16x16) para coordenadas (x, y) reais no mundo,
    assumindo que cada célula foi expandida para um bloco de cell_size x cell_size metros.
    
    Retorna uma lista de coordenadas em metros para o robô seguir no Gazebo.
    """
    costmap = load_costmap("base_maze.txt")
    start = (0, 4)      # linha, coluna
    goal  = (15, 13)

    path = astar(costmap, start, goal)
    if not path:
        print("❌ Caminho não encontrado.")
        return []
    
    print(f"path: {path}")
    
    plot_base_maze(costmap, path, start, goal)

    world_path = []
    for row, col in path:
        # Centro da célula expandida
        adjusted_col = col - 4
        x = adjusted_col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        world_path.append((x * resolution, y * resolution))

    return world_path



""" world_path_expanded = convert_path_to_world_coords_in_expanded_maze()

print("\n🌍 Caminho ajustado para o mundo expandido (coordenadas em metros):")
for x, y in world_path_expanded:
    print(f"({x:.2f}, {y:.2f})") """
