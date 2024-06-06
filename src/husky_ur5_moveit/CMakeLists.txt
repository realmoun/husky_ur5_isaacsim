cmake_minimum_required(VERSION 2.8.3)
project(husky_ur5_moveit)

# Install files
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}  # ROS 1 uses share
        PATTERN ".setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES .setup_assistant DESTINATION share/${PROJECT_NAME})

