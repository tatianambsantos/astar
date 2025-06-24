import xml.etree.ElementTree as ET
import numpy as np

def extract_costmap_from_sdf(sdf_path, output_txt="costmap.txt", resolution=1.0, size=48):
    tree = ET.parse(sdf_path)
    root = tree.getroot()

    costmap = np.zeros((size, size), dtype=int)

    world = root.find("world")
    if world is None:
        raise ValueError("Tag <world> não encontrada.")

    for model in world.findall("model"):
        pose_tag = model.find("pose")
        if pose_tag is None:
            continue
        pose_values = list(map(float, pose_tag.text.strip().split()))
        x, y, z = pose_values[0], pose_values[1], pose_values[2]

        link = model.find("link")
        if link is None:
            continue
        collision = link.find("collision")
        if collision is None:
            continue
        geometry = collision.find("geometry")
        if geometry is None:
            continue
        box = geometry.find("box")
        if box is None:
            continue
        size_tag = box.find("size")
        if size_tag is None:
            continue

        sx, sy, sz = map(float, size_tag.text.strip().split())

        # Calcula quais células estão ocupadas (assume que a origem está no centro da matriz)
        min_x = int((x - sx/2) + size/2)
        max_x = int((x + sx/2) + size/2)
        min_y = int((y - sy/2) + size/2)
        max_y = int((y + sy/2) + size/2)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                if 0 <= i < size and 0 <= j < size:
                    costmap[j][i] = 1  # obs: y é linha, x é coluna
    
    costmap = np.fliplr(costmap)


    # Salvar em .txt
    with open(output_txt, "w") as f:
        for row in costmap:
            f.write("".join(map(str, row)) + "\n")

    print(f"Matriz de custos salva em {output_txt}")

# Exemplo de uso
extract_costmap_from_sdf("maze_from_matrix.sdf", output_txt="costmap.txt", resolution=1.0, size=48)
