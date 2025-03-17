import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
from rcl_interfaces.msg import SetParametersResult
import rclpy.parameter
import time

class WaiterNode(Node):
    def __init__(self):
        super().__init__('waiter_node')
        self.declare_parameter('order_prefix', '订单编号')
        self.declare_parameter('order_counter', 1)

        self.subscription = self.create_subscription(String, 'order_topic', self.order_callback, 10)
        self.publisher = self.create_publisher(String, 'deliver_topic', 10)
        self.cli = self.create_client(Trigger, 'order_service')

        # 注册参数修改回调
        self.add_on_set_parameters_callback(self.parameter_callback)

    def order_callback(self, msg):
        """处理顾客订单"""
        time.sleep(1)
        self.get_logger().info(f"服务员收到点餐信息: {msg.data}")

        order_prefix = self.get_parameter('order_prefix').get_parameter_value().string_value
        order_counter = self.get_parameter('order_counter').get_parameter_value().integer_value

        order_info = f"{order_prefix}{order_counter},{msg.data}"
        time.sleep(1)
        self.get_logger().info(f"服务员生成订单信息: {order_info}")

        # 更新订单编号
        self.set_parameters([rclpy.parameter.Parameter('order_counter', rclpy.Parameter.Type.INTEGER, order_counter + 1)])

        if self.cli.service_is_ready():
            req = Trigger.Request()
            future = self.cli.call_async(req)
            future.add_done_callback(self.chef_response_callback)
        else:
            time.sleep(1)
            self.get_logger().warn("厨师服务不可用，稍后再试...")

    def chef_response_callback(self, future):
        """处理厨师的服务返回信息"""
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f"服务调用失败: {e}")
        else:
            time.sleep(1)
            self.get_logger().info(f"服务员收到厨师返回信息: {response.message}")

            deliver_msg = String()
            deliver_msg.data = response.message
            self.publisher.publish(deliver_msg)
            time.sleep(1)
            self.get_logger().info("服务员已送餐")

    def parameter_callback(self, params):
        """监听参数修改"""
        for param in params:
            if param.name == 'order_counter' and param.type_ == rclpy.Parameter.Type.INTEGER:
                self.get_logger().info(f"订单编号修改为: {param.value}")
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = WaiterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
