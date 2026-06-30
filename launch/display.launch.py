# Copyright 2026 ESTUN AUTOMATION CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    # 1) 获取参数
    model_type = LaunchConfiguration("model").perform(context)

    # 2) 获取包路径
    desc_pkg = get_package_share_directory("estun_description")

    # 3) 动态选择标定文件（与 demo.launch.py 使用同一规则）
    actual_path = os.path.join(desc_pkg, "config", model_type, "calibration.yaml")
    nominal_path = os.path.join(desc_pkg, "config", model_type, "default_kinematics.yaml")

    if os.path.exists(actual_path):
        target_calib_file = actual_path
        print(f"[INFO] [Display] 检测到真机标定文件: {actual_path}")
    elif os.path.exists(nominal_path):
        target_calib_file = nominal_path
        print(f"[INFO] [Display] 未发现标定文件，使用默认参数: {nominal_path}")
    else:
        target_calib_file = ""
        print("[WARN] [Display] 未找到任何参数文件，Xacro 解析可能失败。")

    # 4) 使用 ROS 2 Command 动态生成 robot_description
    xacro_file = os.path.join(desc_pkg, "robot", f"{model_type}.urdf.xacro")

    # display.launch 仅用于可视化，固定 use_mock:=true
    robot_description_config = Command(
        [
            "xacro ",
            xacro_file,
            " use_mock:=true",
            " kinematics_file:=",
            target_calib_file,
        ]
    )

    params = {"robot_description": robot_description_config}

    # 5) 仅启动可视化所需节点
    nodes_to_launch = [
        # 发布 TF 树
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[params],
        ),
        # 启动关节滑块 GUI
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen",
        ),
        # 启动 RViz2
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", os.path.join(desc_pkg, "rviz", "view_estun.rviz")],
        ),
    ]

    return nodes_to_launch


def generate_launch_description():
    # 默认机型可通过 model:=xxx 覆盖
    model_arg = DeclareLaunchArgument(
        "model",
        default_value="ER20-1780-A6",
        description="指定要启动查看的埃斯顿机型",
    )

    return LaunchDescription([model_arg, OpaqueFunction(function=launch_setup)])
