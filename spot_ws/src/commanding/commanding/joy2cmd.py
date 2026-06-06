import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from spot_interfaces.msg import StateCmd

class Joy2Cmd(Node):
    def __init__(self):
        super().__init__('joy2cmd')
        self._cmd_pub = self.create_publisher(Twist, 'twist', 10)
        self._state_pub = self.create_publisher(StateCmd, 'state_cmd', 10)
        self._joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self._sit = 1
        self._sit_pressed = False
        self._stop_pressed = False
        self.get_logger().info("Joy2Cmd initialized")
        self.get_logger().info("""
Controller Map:
  X (btn 0)   - Stand/Sit toggle
  O (btn 1)   - Stop
  L stick Y   - Walk forward/backward
  R stick X   - Turn left/right
  L1 (btn 6)  - Failsafe stop
        """)

    def joy_callback(self, msg):
        twist = Twist()
        state = StateCmd()

        # Stand/Sit toggle - X button (0)
        if msg.buttons[0]:
            if not self._sit_pressed:
                self._sit_pressed = True
                self._sit = 0 if self._sit == 1 else 1
                state.sit = self._sit
                self._state_pub.publish(state)
        else:
            self._sit_pressed = False

        # Stop - O button (1)
        if msg.buttons[1]:
            if not self._stop_pressed:
                self._stop_pressed = True
                self._cmd_pub.publish(twist)
        else:
            self._stop_pressed = False

        # Failsafe - L1 button (6)
        if msg.buttons[6]:
            self._cmd_pub.publish(twist)
            state.sit = 1
            self._sit = 1
            self._state_pub.publish(state)
            return

        # Walk - Left stick Y axis (1) - inverted
        twist.linear.x = -msg.axes[1] * 0.8

        # Turn - Right stick X axis (2)
        twist.angular.z = msg.axes[2] * 0.5

        self._cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Joy2Cmd()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
