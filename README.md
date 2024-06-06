catkin build the packages
- Run isaacsim with ros_bridge extension and load usd/husky_ur5.usd
- Husky control
```shell  
rosrun teleop_twist_keyboard teleop_twist_keyboard
```
- ur5&robotiq moveit2
```shell  
roslaunch husky_ur5_moveit_config demo.launch
```
