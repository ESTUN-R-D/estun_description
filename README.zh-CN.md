# estun_description

语言：中文 | [English](./README.md)

本仓库包含 ESTUN 机器人机型描述文件、网格资源、运动学参数、机型限速参数，以及基于 RViz 的可视化入口。

## 安装

本仓库作为独立 ROS 2 包仓库维护，通常与 [`estun_ros2`](https://github.com/ESTUN-R-D/estun_ros2) 主仓库同级放在工作区 `src/` 下使用。

工作区创建、Git LFS（大文件存储）启用和完整构建说明，请参考 [`estun_ros2` 主仓库说明](https://github.com/ESTUN-R-D/estun_ros2/blob/main/README.zh-CN.md)。

如果只验证本包，可以执行：

```bash
git lfs install

cd ~/estun_ws
colcon build --packages-select estun_description
source install/setup.bash
```

## 仓库结构

```text
├── launch
│   └── display.launch.py
├── meshes
│   ├── ER20-1780-A6
│   │   ├── collision
│   │   │   └── ...
│   │   └── visual
│   │       └── ...
│   ├── iER10-900-MI
│   │   ├── collision
│   │   │   └── ...
│   │   └── visual
│   │       └── ...
│   └── ... 其他机型
├── robot
│   ├── ER20-1780-A6.urdf.xacro
│   ├── iER10-900-MI.urdf.xacro
│   └── ... 其他机型顶层入口
├── rviz
│   └── view_estun.rviz
├── urdf
│   ├── ER20-1780-A6-macro.xacro
│   ├── iER10-900-MI-macro.xacro
│   └── ... 其他机型宏文件
├── config
│   ├── ER20-1780-A6
│   │   ├── calibration.yaml
│   │   ├── default_kinematics.yaml
│   │   ├── joint_limits.yaml
│   │   └── cartesian_limits.yaml
│   └── ... 其他机型
├── CMakeLists.txt
├── package.xml
└── README.zh-CN.md
```

描述文件按 ESTUN 机器人机型组织。

### 包结构

- `meshes/`：各机型的 visual / collision 网格资源
- `urdf/`：用于生成机器人描述的基础 `xacro` 宏文件
- `robot/`：生成完整机器人 `URDF` 的顶层 `xacro` 入口
- `config/`：机型运动学、标定和限速参数
- `launch/` 与 `rviz/`：机器人可视化启动文件和 RViz 配置

## 可视化

启动模型可视化：

```bash
ros2 launch estun_description display.launch.py model:=ER20-1780-A6
```

切换机型时，直接替换 `model` 参数即可。

`display.launch.py` 会按下面顺序选择运动学参数文件：

1. `config/<MODEL>/calibration.yaml`
2. `config/<MODEL>/default_kinematics.yaml`

如果存在真机标定文件，会优先使用 `calibration.yaml`；否则回退到 `default_kinematics.yaml`。

## 配套关系

- `estun_hardware`：在控制场景下复用本仓库的机器人描述
- `estun_moveit_config`：在规划场景下复用本仓库的机器人描述和机型限速参数

本仓库只负责机器人描述与可视化，不提供 `ros2_control` 硬件接口。

## 许可

本仓库采用 [Apache-2.0](./LICENSE)。
