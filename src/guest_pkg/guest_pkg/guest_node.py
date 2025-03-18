import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rcl_interfaces.msg import SetParametersResult
import time
import random

class GuestNode(Node):
    def __init__(self):
        # 设置节点名称为guest_node
        super().__init__('guest_node')
        # 声明参数：可用菜品列表、顾客编号
        self.declare_parameter('available_dishes', ['鱼香肉丝','宫保鸡丁','番茄鸡蛋','辣椒炒肉'])
        self.declare_parameter('guest_number', 1)

        self.publisher = self.create_publisher(String, 'order_topic', 10)
        self.subscription = self.create_subscription(String, 'deliver_topic', self.deliver_callback, 10)
        self.add_on_set_parameters_callback(self.parameter_callback)

        # 初始化参数
        self.available_dishes = self.get_parameter('available_dishes').get_parameter_value().string_array_value
        self.guest_number = self.get_parameter('guest_number').get_parameter_value().integer_value
        self.first_order()  # 立即发布第一份订单

    def first_order(self):
        # 节点启动后，立即发布第一份订单
        time.sleep(1)
        self.publish_order()

    def publish_order(self):
        # 循环发布订单
        time.sleep(1)
        # 菜品在可用菜品列表中随机选择
        order_message = random.choice(self.available_dishes)
        msg = String()
        msg.data = order_message 
        # 记录顾客编号和订单菜品
        self.publisher.publish(msg)
        self.get_logger().info(f"顾客{self.guest_number} 发起订单: {order_message}")

    def deliver_callback(self, msg):
        # 接收送餐信息，并触发新顾客点餐
        time.sleep(1)
        self.get_logger().info(f"顾客{self.guest_number} 收到送餐信息: {msg.data}")
                
        self.guest_number += 1  
        time.sleep(1)
        self.get_logger().info(f"下一位顾客{self.guest_number} 即将点餐...")

        time.sleep(5)
        self.publish_order()  # 触发下一位顾客点餐
        
    def parameter_callback(self, params):
        # 动态修改参数回调，更新顾客编号和订单编号
        for param in params:
            if param.name == 'guest_number' and param.type_ == param.Type.INTEGER:
                self.guest_number = param.value
                self.get_logger().info(f"顾客编号修改为: {self.guest_number}")
            elif param.name == 'available_dishes'and param.type_ == param.Type.STRING_ARRAY:
                self.available_dishes = param.value
                self.get_logger().info(f"菜单更新: {param.value}")
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
