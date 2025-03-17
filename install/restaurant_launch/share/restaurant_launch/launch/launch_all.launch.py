from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 启动第一个节点
        Node(
            package='chef_pkg',
            executable='chef_node',
            name='chef_node',
            output='screen',
        ),
        # 延迟启动第二个节点
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='waiter_pkg',
                    executable='waiter_node',
                    name='waiter_node',
                    output='screen',
                ),
            ]
        ),
        # 延迟启动第三个节点
        TimerAction(
            period=10.0,
            actions=[
                Node(
                    package='guest_pkg',
                    executable='guest_node',
                    name='guest_node',
                    output='screen',
                ),
            ]
        ),
    ])
