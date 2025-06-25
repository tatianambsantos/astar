import numpy as np


############################ GERA BLOCOS DE 1X1 #######################################
def generate_sdf_from_maze_1(maze, filename="maze_from_matrix_3.sdf"):
    rows, cols = maze.shape

    header = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="generated_maze">
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Chão claro -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
          <material>
            <ambient>0.9 0.9 0.9 1</ambient>
            <diffuse>0.9 0.9 0.9 1</diffuse>
            <specular>0.3 0.3 0.3 1</specular>
          </material>
        </visual>
      </link>
    </model>
"""

    wall_template = """
    <model name="wall_{i}_{j}">
      <static>true</static>
      <pose>{x} {y} 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>1 1 1</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>1 1 1</size></box></geometry>
          <material>
            <ambient>0.0 0.8 0.0 1</ambient>
            <diffuse>0.0 0.8 0.0 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
      </link>
    </model>
"""

    models = ""
    for i in range(rows):
        for j in range(cols):
            if maze[i, j] == 1:
                # Convert (i, j) para coordenadas do mundo (com centro no meio da matriz)
                x = j - cols // 2
                y = rows // 2 - i
                models += wall_template.format(i=i, j=j, x=x, y=y)

    footer = """
        </world>
      </sdf>
      """


    with open(filename, "w") as f:
        f.write(header + models + footer)

    print(f"✅ Arquivo SDF gerado com sucesso: {filename}")

############################################ GERA BLOCOS DE 3X3 ####################################

import numpy as np

def generate_sdf_from_maze_3(maze, filename="maze_from_matrix_3.sdf", cell_size=3.0, wall_height=2.0):
    rows, cols = maze.shape

    header = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="generated_maze">
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Chão claro -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal><size>300 300</size></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>300 300</size></plane></geometry>
          <material>
            <ambient>0.9 0.9 0.9 1</ambient>
            <diffuse>0.9 0.9 0.9 1</diffuse>
            <specular>0.3 0.3 0.3 1</specular>
          </material>
        </visual>
      </link>
    </model>
"""

    wall_template = f"""
    <model name="wall_{{i}}_{{j}}">
      <static>true</static>
      <pose>{{x}} {{y}} {wall_height/2:.2f} 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>{cell_size} {cell_size} {wall_height}</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>{cell_size} {cell_size} {wall_height}</size></box></geometry>
          <material>
            <ambient>0.0 0.8 0.0 1</ambient>
            <diffuse>0.0 0.8 0.0 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
      </link>
    </model>
"""

    models = ""
    for i in range(rows):
        for j in range(cols):
            if maze[i, j] == 1:
                x = (j - cols // 2) * cell_size
                y = (rows // 2 - i) * cell_size
                models += wall_template.format(i=i, j=j, x=x, y=y)

    footer = """
  </world>
</sdf>
"""

    with open(filename, "w") as f:
        f.write(header + models + footer)

    print(f"✅ Arquivo SDF gerado com sucesso: {filename}")



# Exemplo de uso:
""" if __name__ == "__main__":
    # Aqui você pode carregar uma matriz já salva em .npy ou gerar uma nova:
    # Exemplo: carregando de arquivo
    # maze = np.load("maze_matrix.npy")

    # Ou usando uma geração rápida para testar:
    from numpy.random import choice
    maze = np.ones((48, 48), dtype=np.int8)
    maze[1:-1, 1:-1] = choice([0, 1], size=(46, 46), p=[0.7, 0.3])
    maze[0][10] = 0  # saída
    maze[-1][34] = 0  # entrada

    generate_sdf_from_maze(maze) """
