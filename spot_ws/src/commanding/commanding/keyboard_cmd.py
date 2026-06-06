import sys
import tty
import termios
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from spot_interfaces.msg import StateCmd

class KeyboardCmd(Node):
    def __init__(self):
        super().__init__('keyboard_cmd')
        self._cmd_pub = self.create_publisher(Twist, 'twist', 10)
        self._state_pub = self.create_publisher(StateCmd, 'state_cmd', 10)
        self._sit = 1
        print("""
Keyboard Control:
  w - forward
  s - backward
  a - turn left
  d - turn right
  space - stop
  r - stand
  f - sit
  q - quit
""")

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def run(self):
        while True:
            key = self.get_key()
            twist = Twist()
            state = StateCmd()

            if key == 'w':
                twist.linear.x = 0.5
                self._cmd_pub.publish(twist)
            elif key == 's':
                twist.linear.x = -0.5
                self._cmd_pub.publish(twist)
            elif key == 'a':
                twist.angular.z = 0.5
                self._cmd_pub.publish(twist)
            elif key == 'd':
                twist.angular.z = -0.5
                self._cmd_pub.publish(twist)
            elif key == ' ':
                self._cmd_pub.publish(twist)
            elif key == 'r':
                state.sit = 0
                self._state_pub.publish(state)
            elif key == 'f':
                state.sit = 1
                self._state_pub.publish(state)
            elif key == 'q':
                break

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardCmd()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
