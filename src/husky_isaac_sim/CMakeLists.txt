cmake_minimum_required(VERSION 2.8.3)
project(husky_isaac_sim)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED)

################################################################################
# Install
################################################################################
#install(
 # DIRECTORY launch urdf meshes rviz
  #DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
#)

################################################################################
# Catkin package definition
################################################################################
catkin_package()

