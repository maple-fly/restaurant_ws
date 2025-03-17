from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='waiter_pkg',
            executable='waiter_node',
            name='waiter_node',
            output='screen',
            parameters=[{'param_name': 'param_value'}],  # 可选：节点参数
            remappings=[('/old_topic', '/new_topic')]    # 可选：主题重映射
        ),
    ])
