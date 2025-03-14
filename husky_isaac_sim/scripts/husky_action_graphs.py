# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import omni
import omni.graph.core as og
from omni.isaac.core.utils import stage
from omni.isaac.core_nodes.scripts.utils import set_target_prims
from pxr import Gf, UsdGeom
from omni.kit import commands
from pxr import Sdf, Usd
from omni.isaac.core.utils.prims import set_targets

def create_camera(robot_name, number_camera, camera_frame, camera_stage_path, camera_name, stereo_offset=[0.0, 0.0]):
    
    ros_camera_graph_path = f"/{robot_name}/ROS_CameraGraph_{camera_name}"
    viewport_name = f"Viewport{number_camera}"
    
    # Creating an on-demand push graph with cameraHelper nodes to generate ROS image publishers
    keys = og.Controller.Keys
    (ros_camera_graph, _, _, _) = og.Controller.edit(
        {
            "graph_path": ros_camera_graph_path,
            "evaluator_name": "push",
            "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION,
        },
        {
            keys.CREATE_NODES: [
                (f"{camera_name}_OnTick", "omni.graph.action.OnTick"),
                (f"{camera_name}_createViewport", "omni.isaac.core_nodes.IsaacCreateViewport"),
                (f"{camera_name}_getRenderProduct", "omni.isaac.core_nodes.IsaacGetViewportRenderProduct"),
                (f"{camera_name}_setViewportResolution", "omni.isaac.core_nodes.IsaacSetViewportResolution"),
                (f"{camera_name}_setCamera", "omni.isaac.core_nodes.IsaacSetCameraOnRenderProduct"),
                (f"{camera_name}_cameraHelper", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
                (f"{camera_name}_cameraHelperInfo", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
            ],
            keys.CONNECT: [
                (f"{camera_name}_OnTick.outputs:tick", f"{camera_name}_createViewport.inputs:execIn"),
                (f"{camera_name}_createViewport.outputs:execOut", f"{camera_name}_getRenderProduct.inputs:execIn"),
                (f"{camera_name}_createViewport.outputs:execOut", f"{camera_name}_setViewportResolution.inputs:execIn"),
                (f"{camera_name}_createViewport.outputs:viewport", f"{camera_name}_getRenderProduct.inputs:viewport"),
                (f"{camera_name}_createViewport.outputs:viewport", f"{camera_name}_setViewportResolution.inputs:viewport"),
                (f"{camera_name}_setViewportResolution.outputs:execOut", f"{camera_name}_setCamera.inputs:execIn"),
                (f"{camera_name}_getRenderProduct.outputs:renderProductPath", f"{camera_name}_setCamera.inputs:renderProductPath"),
                (f"{camera_name}_setCamera.outputs:execOut", f"{camera_name}_cameraHelper.inputs:execIn"),
                (f"{camera_name}_setCamera.outputs:execOut", f"{camera_name}_cameraHelperInfo.inputs:execIn"),
                (f"{camera_name}_getRenderProduct.outputs:renderProductPath", f"{camera_name}_cameraHelper.inputs:renderProductPath"),
                (f"{camera_name}_getRenderProduct.outputs:renderProductPath", f"{camera_name}_cameraHelperInfo.inputs:renderProductPath"),
            ],
            keys.SET_VALUES: [
                (f"{camera_name}_createViewport.inputs:name", viewport_name),
                (f"{camera_name}_createViewport.inputs:viewportId", number_camera),
                (f"{camera_name}_setViewportResolution.inputs:width", 640),
                (f"{camera_name}_setViewportResolution.inputs:height", 480),
                (f"{camera_name}_cameraHelper.inputs:frameId", f"{camera_frame}"),
                (f"{camera_name}_cameraHelper.inputs:topicName", f"/front/stereo_camera/{camera_name}/rgb"),
                (f"{camera_name}_cameraHelper.inputs:type", f"rgb"),
                (f"{camera_name}_cameraHelperInfo.inputs:frameId", f"{camera_frame}"),
                (f"{camera_name}_cameraHelperInfo.inputs:topicName", f"/front/stereo_camera/{camera_name}/camera_info"),
                (f"{camera_name}_cameraHelperInfo.inputs:type", "camera_info"),
                (f"{camera_name}_cameraHelperInfo.inputs:stereoOffset", stereo_offset),
            ],
        },
    )

    set_targets(
        prim=stage.get_current_stage().GetPrimAtPath(ros_camera_graph_path + f"/{camera_name}_setCamera"),
        attribute="inputs:cameraPrim",
        target_prim_paths=[camera_stage_path],
    )


def create_camera_rgb_depth(robot_name, number_camera, camera_frame, camera_depth_frame, camera_stage_path, camera_name, stereo_offset=[0.0, 0.0]):
    
    ros_camera_graph_path = f"/{robot_name}/ROS_CameraGraph_{camera_name}"
    viewport_name = f"Viewport{number_camera}"
    
    # Creating an on-demand push graph with cameraHelper nodes to generate ROS image publishers
    keys = og.Controller.Keys
    (ros_camera_graph, _, _, _) = og.Controller.edit(
        {
            "graph_path": ros_camera_graph_path,
            "evaluator_name": "push",
            "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION,
        },
        {
            keys.CREATE_NODES: [
                ("OnTick", "omni.graph.action.OnTick"),
                ("createViewport", "omni.isaac.core_nodes.IsaacCreateViewport"),
                ("getRenderProduct", "omni.isaac.core_nodes.IsaacGetViewportRenderProduct"),
                ("setViewportResolution", "omni.isaac.core_nodes.IsaacSetViewportResolution"),
                ("setCamera", "omni.isaac.core_nodes.IsaacSetCameraOnRenderProduct"),
                ("cameraHelper", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
                ("cameraDepth", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
                ("cameraHelperInfo", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
            ],
            keys.CONNECT: [
                ("OnTick.outputs:tick", "createViewport.inputs:execIn"),
                ("createViewport.outputs:execOut", "getRenderProduct.inputs:execIn"),
                ("createViewport.outputs:execOut", "setViewportResolution.inputs:execIn"),
                ("createViewport.outputs:viewport", "getRenderProduct.inputs:viewport"),
                ("createViewport.outputs:viewport", "setViewportResolution.inputs:viewport"),
                ("setViewportResolution.outputs:execOut", "setCamera.inputs:execIn"),
                ("getRenderProduct.outputs:renderProductPath", "setCamera.inputs:renderProductPath"),
                ("setCamera.outputs:execOut", "cameraHelper.inputs:execIn"),
                ("setCamera.outputs:execOut", "cameraDepth.inputs:execIn"),
                ("setCamera.outputs:execOut", "cameraHelperInfo.inputs:execIn"),
                ("getRenderProduct.outputs:renderProductPath", "cameraHelper.inputs:renderProductPath"),
                ("getRenderProduct.outputs:renderProductPath", "cameraDepth.inputs:renderProductPath"),
                ("getRenderProduct.outputs:renderProductPath", "cameraHelperInfo.inputs:renderProductPath"),
            ],
            keys.SET_VALUES: [
                ("createViewport.inputs:name", viewport_name),
                ("createViewport.inputs:viewportId", number_camera),
                ("setViewportResolution.inputs:width", 640),
                ("setViewportResolution.inputs:height", 480),
                ("cameraHelper.inputs:frameId", f"{camera_frame}"),
                ("cameraHelper.inputs:topicName", f"/front/stereo_camera/{camera_name}/rgb"),
                ("cameraHelper.inputs:type", f"rgb"),
                ("cameraDepth.inputs:frameId", f"{camera_depth_frame}"),
                ("cameraDepth.inputs:topicName", f"/front/stereo_camera/{camera_name}/depth"),
                ("cameraDepth.inputs:type", f"depth"),
                ("cameraHelperInfo.inputs:frameId", f"{camera_frame}"),
                ("cameraHelperInfo.inputs:topicName", f"/front/stereo_camera/{camera_name}/camera_info"),
                ("cameraHelperInfo.inputs:type", "camera_info"),
                ("cameraHelperInfo.inputs:stereoOffset", stereo_offset),
            ],
        },
    )

    set_targets(
        prim=stage.get_current_stage().GetPrimAtPath(ros_camera_graph_path + "/setCamera"),
        attribute="inputs:cameraPrim",
        target_prim_paths=[camera_stage_path],
    )


def build_camera_graph(robot_name):

    camera_left_stage_path = f"/{robot_name}/zed_camera_center/camera_left"
    # Creating a Camera prim
    camera_left_prim = UsdGeom.Camera(omni.usd.get_context().get_stage().DefinePrim(camera_left_stage_path, "Camera"))
    xform_api = UsdGeom.XformCommonAPI(camera_left_prim)
    xform_api.SetTranslate(Gf.Vec3d(0.103, 0.06, 0)) # 0.103 - 0.06 - 0.3095
    xform_api.SetRotate((90, 0, -90), UsdGeom.XformCommonAPI.RotationOrderXYZ)
    camera_left_prim.GetHorizontalApertureAttr().Set(2.0955)
    camera_left_prim.GetVerticalApertureAttr().Set(1.1769)
    camera_left_prim.GetClippingRangeAttr().Set((0.01, 10000))
    camera_left_prim.GetProjectionAttr().Set("perspective")
    camera_left_prim.GetVisibilityAttr().Set("invisible")
    camera_left_prim.GetFocalLengthAttr().Set(2.4)
    camera_left_prim.GetFocusDistanceAttr().Set(4)
    
    camera_right_stage_path = f"/{robot_name}/zed_camera_center/camera_right"
    # Creating a Camera prim
    camera_right_prim = UsdGeom.Camera(omni.usd.get_context().get_stage().DefinePrim(camera_right_stage_path, "Camera"))
    xform_api = UsdGeom.XformCommonAPI(camera_right_prim)
    xform_api.SetTranslate(Gf.Vec3d(0.103, -0.06, 0)) # 0.103 - -0.06 - 0.3095
    xform_api.SetRotate((90, 0, -90), UsdGeom.XformCommonAPI.RotationOrderXYZ)
    camera_right_prim.GetHorizontalApertureAttr().Set(2.0955)
    camera_right_prim.GetVerticalApertureAttr().Set(1.1769)
    camera_right_prim.GetClippingRangeAttr().Set((0.01, 10000))
    camera_right_prim.GetProjectionAttr().Set("perspective")
    camera_right_prim.GetVisibilityAttr().Set("invisible")
    camera_right_prim.GetFocalLengthAttr().Set(2.4)
    camera_right_prim.GetFocusDistanceAttr().Set(4)
    # Create rgb camera
    create_camera_rgb_depth(robot_name, 1, "zed_left_depth_frame", "zed_left_depth_frame", camera_left_stage_path, "rgb")
    create_camera(robot_name, 2, "zed_left_camera_frame", camera_left_stage_path, "left")
    create_camera(robot_name, 3, "zed_right_camera_frame", camera_right_stage_path, "right", stereo_offset=[-175.92, 0])


def build_differential_controller_graph(robot_name):   
    # Creating a action graph with ROS component nodes
    # https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_python.html
    # https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/tutorial_ros2_turtlebot.html#build-the-graph
    try:
        (ros_camera_graph, _, _, _) = og.Controller.edit(
            {
                "graph_path": f"/{robot_name}/ActionGraph",
                "evaluator_name": "execution",
                "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION
            },
            {
                og.Controller.Keys.CREATE_NODES: [
                    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
                    ("ROS2Context", "omni.isaac.ros2_bridge.ROS2Context"),
                    ("ROS2SubscribeTwist", "omni.isaac.ros2_bridge.ROS2SubscribeTwist"),
                    ("scale_to_from_stage_units", "omni.isaac.core_nodes.OgnIsaacScaleToFromStageUnit"),
                    ("break_3_vector_01", "omni.graph.nodes.BreakVector3"),
                    ("break_3_vector_02", "omni.graph.nodes.BreakVector3"),
                    ("DifferentialController", "omni.isaac.wheeled_robots.DifferentialController"),
                    ("array_index_01", "omni.graph.nodes.ArrayIndex"),
                    ("array_index_02", "omni.graph.nodes.ArrayIndex"),
                    ("ConstantToken_01", "omni.graph.nodes.ConstantToken"),
                    ("ConstantToken_02", "omni.graph.nodes.ConstantToken"),
                    ("ConstantToken_03", "omni.graph.nodes.ConstantToken"),
                    ("ConstantToken_04", "omni.graph.nodes.ConstantToken"),
                    ("MakeArray", "omni.graph.nodes.MakeArray"),
                    ("MakeArray_02", "omni.graph.nodes.MakeArray"),
                    ("IsaacArticulationController", "omni.isaac.core_nodes.IsaacArticulationController"),
                    ("IsaacReadSimulationTime", "omni.isaac.core_nodes.IsaacReadSimulationTime"),
                    ("ROS2PublishTransformTree", "omni.isaac.ros2_bridge.ROS2PublishTransformTree"),
                ],
                og.Controller.Keys.CONNECT: [
                    ("OnPlaybackTick.outputs:tick", "ROS2SubscribeTwist.inputs:execIn"),
                    ("ROS2Context.outputs:context", "ROS2SubscribeTwist.inputs:context"),
                    ("ROS2SubscribeTwist.outputs:angularVelocity", "break_3_vector_01.inputs:tuple"),
                    ("ROS2SubscribeTwist.outputs:linearVelocity", "scale_to_from_stage_units.inputs:value"),
                    ("scale_to_from_stage_units.outputs:result", "break_3_vector_02.inputs:tuple"),
                    ("ROS2SubscribeTwist.outputs:execOut", "DifferentialController.inputs:execIn"),
                    ("break_3_vector_01.outputs:z", "DifferentialController.inputs:angularVelocity"),
                    ("break_3_vector_02.outputs:x", "DifferentialController.inputs:linearVelocity"),
                    ("OnPlaybackTick.outputs:tick", "IsaacArticulationController.inputs:execIn"),
                    ("DifferentialController.outputs:velocityCommand", "array_index_01.inputs:array"),
                    ("DifferentialController.outputs:velocityCommand", "array_index_02.inputs:array"),
                    ("array_index_01.outputs:value", "MakeArray_02.inputs:c"),
                    ("array_index_01.outputs:value", "MakeArray_02.inputs:a"),
                    ("array_index_02.outputs:value", "MakeArray_02.inputs:d"),
                    ("array_index_02.outputs:value", "MakeArray_02.inputs:b"),
                    ("MakeArray_02.outputs:array", "IsaacArticulationController.inputs:velocityCommand"),
                    # ("DifferentialController.outputs:velocityCommand", "IsaacArticulationController.inputs:velocityCommand"),
                    ("ConstantToken_01.inputs:value", "MakeArray.inputs:a"),
                    ("ConstantToken_02.inputs:value", "MakeArray.inputs:b"),
                    ("ConstantToken_03.inputs:value", "MakeArray.inputs:c"),
                    ("ConstantToken_04.inputs:value", "MakeArray.inputs:d"),
                    ("MakeArray.outputs:array", "IsaacArticulationController.inputs:jointNames"),
                    ("OnPlaybackTick.outputs:tick", "ROS2PublishTransformTree.inputs:execIn"),
                    ("ROS2Context.outputs:context", "ROS2PublishTransformTree.inputs:context"),
                    ("IsaacReadSimulationTime.outputs:simulationTime", "ROS2PublishTransformTree.inputs:timeStamp"),
                ],
                og.Controller.Keys.SET_VALUES: [
                    # Assigning a Domain ID of 1 to Context node
                    ("ROS2Context.inputs:domain_id", 0),
                    # Assigning topic name to clock publisher
                    ("ROS2SubscribeTwist.inputs:topicName", "/cmd_vel"),
                    # Assigning Differential controller configuration
                    #("DifferentialController.inputs:maxLinearSpeed", 10000.0),
                    ("DifferentialController.inputs:wheelDistance", 0.512),
                    ("DifferentialController.inputs:wheelRadius", 0.1651),
                    # Assign Articulation controller configuration
                    ("IsaacArticulationController.inputs:usePath", False),
                    # Set size array
                    ("array_index_01.inputs:index", 0),
                    ("array_index_02.inputs:index", 1),
                    ("MakeArray.inputs:arraySize", 4),
                    ("MakeArray_02.inputs:arraySize", 4),
                    # Assigning topic name to clock publisher
                    ("ConstantToken_04.inputs:value", "husky_rear_right_wheel_joint"),
                    ("ConstantToken_03.inputs:value", "husky_rear_left_wheel_joint"),
                    ("ConstantToken_02.inputs:value", "husky_front_right_wheel_joint"),
                    ("ConstantToken_01.inputs:value", "husky_front_left_wheel_joint"),
                ]
            },
        )
    except Exception as e:
        print(e)
    
    HUSKY_STAGE_PATH=f"/{robot_name}/base_link"
    # Setting the /Franka target prim to Subscribe JointState node
    set_target_prims(primPath=f"/{robot_name}/ActionGraph/IsaacArticulationController", targetPrimPaths=[HUSKY_STAGE_PATH])
    # Set targets for Husky
    HUSKY_STAGE_WHEELS_PATH=[f"/{robot_name}/front_left_wheel", f"/{robot_name}/front_right_wheel", f"/{robot_name}/rear_left_wheel", f"/{robot_name}/rear_right_wheel"]
    set_target_prims(
        primPath=f"/{robot_name}/ActionGraph/ROS2PublishTransformTree",
        inputName="inputs:parentPrim",
        targetPrimPaths=[HUSKY_STAGE_PATH],
    )
    set_target_prims(
        primPath=f"/{robot_name}/ActionGraph/ROS2PublishTransformTree",
        inputName="inputs:targetPrims",
        targetPrimPaths=HUSKY_STAGE_WHEELS_PATH,
    )
    # Change stiffness and damping
    for joint in ["front_left_wheel", "front_right_wheel", "rear_left_wheel", "rear_right_wheel"]:
        omni.kit.commands.execute('ChangeProperty', prop_path=Sdf.Path(f"{HUSKY_STAGE_PATH}/{joint}_joint.drive:angular:physics:damping"), value=17453.0, prev=0.0)
        omni.kit.commands.execute('ChangeProperty', prop_path=Sdf.Path(f"{HUSKY_STAGE_PATH}/{joint}_joint.drive:angular:physics:stiffness"), value=0.0, prev=0.0)


def build_clock_graph():
    try:
        (ros_camera_graph, _, _, _) = og.Controller.edit(
            {
                "graph_path": f"/Clock",
                "evaluator_name": "execution",
                "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION
            },
            {
                og.Controller.Keys.CREATE_NODES: [
                    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
                    ("IsaacReadSimulationTime", "omni.isaac.core_nodes.IsaacReadSimulationTime"),
                    ("ROS2PublishClock", "omni.isaac.ros2_bridge.ROS2PublishClock"),
                ],
                og.Controller.Keys.CONNECT: [
                    ("OnPlaybackTick.outputs:tick", "ROS2PublishClock.inputs:execIn"),
                    ("IsaacReadSimulationTime.outputs:simulationTime", "ROS2PublishClock.inputs:timeStamp"),
                ]
            },
        )
    except Exception as e:
        print(e)
# EOF