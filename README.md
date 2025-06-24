# astar

# 🧭 Projeto: Navegação com Robô Diferencial em Labirinto 3D com A⁎

Este projeto demonstra como controlar um **robô com rodas diferenciais** em um ambiente simulado no **Gazebo Ignition**. O robô deve seguir um caminho gerado com o algoritmo **A*** sobre um labirinto expandido, com paredes modeladas automaticamente a partir de uma matriz binária.

---

## 📚 Objetivo

Ensinar passo a passo:

✅ Como **gerar um labirinto** com caminhos navegáveis  
✅ Como **converter esse labirinto** em um mundo `.sdf` para o Gazebo  
✅ Como usar o **algoritmo A*** para planejar rotas  
✅ Como controlar um robô no **ROS 2** usando `/cmd_vel` e **odometria**

---

## 🧱 Etapas do Projeto

---

### 1️⃣ Geração do Labirinto Expandido  
**Arquivo:** `generate_maze_and_world.py`

- Define uma matriz binária `16x16`, onde:
  - `0` representa **caminho livre**
  - `1` representa **parede**

- A matriz é **expandida** para garantir largura realista dos caminhos (ex: 3 metros).  
  Isso é feito transformando cada célula em um **bloco 3x3**.

#### 📌 Exemplo de matriz base:
```python
base_maze = [
  [1, 1, 1, 1, 0, 1, 1, ...],
  [1, 0, 0, 1, 0, 0, 1, ...],
  ...
]
```


Gera uma visualização com matplotlib.

Salva a matriz em base_maze.txt.

Chama generate_sdf_from_maze() para gerar o mundo .sdf com paredes 3D.

### 🤖 2️⃣ Modelo do Robô (SDF)
**Arquivo:** meu_carrin.sdf

O modelo define um robô diferencial simples, com:

Corpo principal (chassi)

Duas rodas laterais com juntas revolute

Uma roda castor traseira com junta ball

# 📦 Plugins adicionados:

✅ DiffDrive – permite movimentar o robô com velocidades linear e angular

✅ OdomPublisher – publica automaticamente no tópico:

bash
Copy
Edit
/model/meu_carrin/odometry
🧭 Sensores opcionais:

IMU, LIDAR, Câmera

É publicado automaticamente o tópico /model/meu_carrin/odometry

### 3. Planejamento com A*

**Arquivo:** astar.py

Lê a matriz base_maze.txt.

Aplica o algoritmo A* entre o ponto de entrada (ex: (0, 4)) e saída (ex: (15, 13)).

Converte os índices da matriz para coordenadas do mundo, considerando:

cell_size

deslocamento de origem para centralizar

Função principal:

convert_path_to_world_coords_in_expanded_maze()

### 4. Controle do Robô no ROS 2

**Arquivo:** path_follower.py

Cria um nó ROS 2 que:

Subscrve Odometry para saber posição e orientação atual.

Publica em cmd_vel para movimentar.

Extrai yaw do quaternário com:

yaw = quat2euler([q.w, q.x, q.y, q.z])[2]

Divide o movimento em etapas:

Movimento retilíneo no eixo X.

Gira 90º para alinhar no eixo Y.

Move no eixo Y.

Gira novamente para alinhar com próximo X.

Usa flags para alternar entre os modos (moving_in_x, rotating, moving_in_y).
