cmake_minimum_required(VERSION 2.8.3)

project(ur5_isaac_simulation)

# Find ROS libraries (if using ROS 1 build tools like catkin)
# If you're not using catkin, you'll need to find and link libraries manually
find_package(geometry_msgs REQUIRED)
find_package(control_msgs REQUIRED)

# Add your source files here (replace with your actual file names)
set(SOURCE_FILES src/main.cpp src/node.cpp)

# Create an executable target
#add_executable(ur5_isaac_sim_node ${SOURCE_FILES})

# Target dependencies (link against ROS libraries)
#target_link_libraries(ur5_isaac_sim_node geometry_msgs control_msgs)

# Optional: install target (consider if you want to install the executable)
# install(TARGETS ur5_isaac_sim_node DESTINATION bin)

