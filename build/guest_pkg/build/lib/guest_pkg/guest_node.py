import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rcl_interfaces.msg import SetParametersResult
import time

class GuestNode(Node):
    def __init__(self):
        super().__init__('guest_node')
        self.declare_parameter('order_message', '鱼香肉丝')
        self.declare_parameter('guest_number', 1)
        self.publisher = self.create_publisher(String, 'order_topic', 10)
        self.subscription = self.create_subscription(String, 'deliver_topic', self.deliver_callback, 10)
        self.add_on_set_parameters_callback(self.parameter_callback)

        # 顾客编号，从1开始
        self.guest_number = self.get_parameter('guest_number').get_parameter_value().integer_value
        self.first_order()  # 立即发布第一份订单

    def first_order(self):
        """发布第一个订单"""
        time.sleep(1)
        self.publish_order()

    def publish_order(self):
        """发布订单"""
        time.sleep(1)
        order_message = self.get_parameter('order_message').get_parameter_value().string_value
        msg = String()
        msg.data = order_message # 加入顾客编号
        self.publisher.publish(msg)
        self.get_logger().info(f"顾客{self.guest_number} 发起订单: {order_message}")

    def deliver_callback(self, msg):
        """接收送餐信息，并触发新顾客点餐"""
        time.sleep(1)
        self.get_logger().info(f"顾客{self.guest_number} 收到送餐信息: {msg.data}")
        
        # 顾客完成订单后，模拟下一个顾客到来
        #time.sleep(5)
        self.guest_number += 1  
        time.sleep(1)
        self.get_logger().info(f"下一位顾客{self.guest_number} 即将点餐...")

        time.sleep(5)
        self.publish_order()  # 触发下一位顾客点餐
        #if self.timer:
        #    self.timer.cancel()  # 取消上一次的定时任务
        #self.timer = self.create_timer(5.0, self.publish_order)  # 5 秒后点餐

    def parameter_callback(self, params):
        """动态修改参数回调"""
        for param in params:
            if param.name == 'guest_number' and param.type_ == param.Type.INTEGER:
                self.guest_number = param.value
                self.get_logger().info(f"顾客编号修改为: {self.guest_number}")
            elif param.name == 'order_message' and param.type_ == param.Type.STRING:
                self.get_logger().info(f"订单内容修改为: {param.value}")
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = GuestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
