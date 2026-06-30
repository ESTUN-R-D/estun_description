# estun_description

Language: [Chinese](./README.zh-CN.md) | English

This repository contains ESTUN robot model descriptions, mesh assets, kinematic parameters, machine limits, and an RViz-based visualization entry point.

## Installation

This repository is maintained as an independent ROS 2 package repository. It is normally used as a sibling of the [`estun_ros2`](https://github.com/ESTUN-R-D/estun_ros2) main repository under the workspace `src/` directory.

For workspace creation, Git LFS (Large File Storage) setup, and the complete build procedure, see the [`estun_ros2` main repository README](https://github.com/ESTUN-R-D/estun_ros2/blob/main/README.md).

To validate this package only:

```bash
git lfs install

cd ~/estun_ws
colcon build --packages-select estun_description
source install/setup.bash
```

## Repository structure

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
│   └── ... other models
├── robot
│   ├── ER20-1780-A6.urdf.xacro
│   ├── iER10-900-MI.urdf.xacro
│   └── ... other top-level model entries
├── rviz
│   └── view_estun.rviz
├── urdf
│   ├── ER20-1780-A6-macro.xacro
│   ├── iER10-900-MI-macro.xacro
│   └── ... other model macros
├── config
│   ├── ER20-1780-A6
│   │   ├── calibration.yaml
│   │   ├── default_kinematics.yaml
│   │   ├── joint_limits.yaml
│   │   └── cartesian_limits.yaml
│   └── ... other models
├── CMakeLists.txt
├── package.xml
└── README.md
```

Description assets are organized by ESTUN robot model.

### Package structure

- `meshes/`: visual and collision mesh assets for each robot model
- `urdf/`: base `xacro` macro files used to generate a robot description
- `robot/`: top-level `xacro` files that generate a complete robot `URDF`
- `config/`: model-specific kinematics, calibration, and machine-limit parameters
- `launch/` and `rviz/`: launch files and RViz configurations for visualization

## Visualization

Launch model visualization:

```bash
ros2 launch estun_description display.launch.py model:=ER20-1780-A6
```

To switch models, replace the `model` argument directly.

`display.launch.py` selects the kinematic parameter file in the following order:

1. `config/<MODEL>/calibration.yaml`
2. `config/<MODEL>/default_kinematics.yaml`

If a real-robot calibration file exists, `calibration.yaml` is used first; otherwise the logic falls back to `default_kinematics.yaml`.

## Package relationships

- `estun_hardware`: reuses this repository's robot descriptions in control scenarios
- `estun_moveit_config`: reuses this repository's robot descriptions and model limit data in planning scenarios

This repository only handles robot descriptions and visualization. It does not provide a `ros2_control` hardware interface.

## Licensing

This repository is licensed under [Apache-2.0](./LICENSE).
