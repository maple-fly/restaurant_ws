import rclpy
from rclpy.node import Node
import time
from std_srvs.srv import Trigger
from rcl_interfaces.msg import SetParametersResult

class ChefNode(Node):
    def __init__(self):
        super().__init__('chef_node')
        # 声明参数，控制烹饪延时（秒）
        self.declare_parameter('cooking_delay', 5.0)
        self.cooking_delay = self.get_parameter('cooking_delay').get_parameter_value().double_value
        # 创建服务，供服务员调用，模拟接收订单和烹饪过程
        self.srv = self.create_service(Trigger, 'order_service', self.handle_order)

        self.add_on_set_parameters_callback(self.parameter_callback)
    def parameter_callback(self, params):
        """监听参数修改"""
        for param in params:
            if param.name == 'cooking_delay' and param.type_ == param.Type.DOUBLE:
                self.cooking_delay = param.value
                self.get_logger().info(f"烹饪时间已更新为: {self.cooking_delay} 秒")
        return SetParametersResult(successful=True)


    def handle_order(self, request, response):
        time.sleep(1)
        self.get_logger().info("厨师收到订单信息")
        cooking_delay = self.get_parameter('cooking_delay').get_parameter_value().double_value
        time.sleep(1)
        self.get_logger().info(f"厨师开始烹饪，预计时间: {cooking_delay}秒")
        # 模拟烹饪延时
        #time.sleep(cooking_delay)
        time.sleep(1)
        self.get_logger().info("厨师完成烹饪: 已完成")
        response.success = True
        response.message = "已完成"
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ChefNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
