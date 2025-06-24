import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from transforms3d.euler import quat2euler
from astar import convert_path_to_world_coords_in_expanded_maze

class PathFollower(Node):
    def __init__(self, path):
        super().__init__('path_follower')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/model/meu_carrin/odometry', self.odom_callback, 10)

        self.path = path
        self.current_pose = None
        self.current_index = 0

        self.timer = self.create_timer(0.05, self.follow_path)

        self.moving_in_x = True
        self.rotating = False
        self.moving_in_y = False

    def odom_callback(self, msg):
        self.current_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            self.get_yaw_from_quaternion(msg.pose.pose.orientation)
        )

    def get_yaw_from_quaternion(self, orientation):
        q = orientation
        yaw = quat2euler([q.w, q.x, q.y, q.z])[2]
        return yaw

    def normalize_angle(self, angle):
        """Garante que o ângulo esteja entre -π e π."""
        return math.atan2(math.sin(angle), math.cos(angle))

    def follow_path(self):
        if self.current_pose is None or self.current_index >= len(self.path):
            return

        goal_x, goal_y = self.path[self.current_index]
        x, y, yaw = self.current_pose

        tolerance = 0.1
        twist = Twist()

        # 1️⃣ Movendo no eixo X
        if self.moving_in_x:
            if abs(goal_x - x) > tolerance:
                distance_to_goal = abs(goal_x - x)
                direction = 1.0 if goal_x > x else -1.0
                twist.linear.x = min(5.0, 2.0 * direction * distance_to_goal)
            else:
                self.moving_in_x = False
                self.rotating_to_y = True

        # 2️⃣ Girando para alinhar no eixo Y
        elif self.rotating_to_y:
            target_yaw = math.pi / 2 if goal_y > y else -math.pi / 2
            yaw_diff = self.normalize_angle(target_yaw - yaw)

            print(f"[Y] Yaw atual: {math.degrees(yaw):.2f}°, alvo: {math.degrees(target_yaw):.2f}°, diff: {math.degrees(yaw_diff):.2f}°")

            if abs(yaw_diff) > 0.03:
                twist.angular.z = 0.8 * yaw_diff
            else:
                twist.angular.z = 0.0
                self.rotating_to_y = False
                self.moving_in_y = True

        # 3️⃣ Movendo no eixo Y
        elif self.moving_in_y:
            if abs(goal_y - y) > tolerance:
                distance_to_goal = abs(goal_y - y)
                direction = 1.0 if goal_y > y else -1.0
                twist.linear.x = min(5.0, 2.0 * direction * distance_to_goal)
            else:
                self.get_logger().info(f"✅ Chegou no ponto {self.current_index}")
                self.current_index += 1

                if self.current_index < len(self.path):
                    self.rotating_to_x = True
                    self.moving_in_y = False
                else:
                    self.moving_in_y = False

        # 4️⃣ Girando para voltar ao eixo X
        elif hasattr(self, 'rotating_to_x') and self.rotating_to_x:
            next_goal_x, _ = self.path[self.current_index]
            target_yaw = 0.0 if next_goal_x > x else math.pi
            yaw_diff = self.normalize_angle(target_yaw - yaw)

            print(f"[X] Yaw atual: {math.degrees(yaw):.2f}°, alvo: {math.degrees(target_yaw):.2f}°, diff: {math.degrees(yaw_diff):.2f}°")

            if abs(yaw_diff) > 0.03:
                twist.angular.z = 0.7 * yaw_diff
            else:
                twist.angular.z = 0.0
                self.rotating_to_x = False
                self.moving_in_x = True

        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    caminho = convert_path_to_world_coords_in_expanded_maze()
    print("📍 Caminho convertido:", caminho)
    path_follower = PathFollower(caminho)
    rclpy.spin(path_follower)
    path_follower.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
