cmake_minimum_required(VERSION 3.8)
project(estun_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找构建依赖
find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(robot_state_publisher REQUIRED)

install(DIRECTORY
  urdf
  meshes
  launch
  rviz
  config
  robot
  DESTINATION share/${PROJECT_NAME}
  PATTERN "__pycache__" EXCLUDE
  PATTERN "*.pyc" EXCLUDE
  PATTERN "*.pyo" EXCLUDE
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_lint_common REQUIRED)
  # xmllint 依赖远程 schema，离线/受限网络环境下会出现非代码问题导致误失败。
  set(AMENT_LINT_AUTO_EXCLUDE ament_xmllint ament_cmake_xmllint)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
