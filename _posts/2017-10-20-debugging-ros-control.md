---
layout: post
title: "Debugging ROS gazebo_ros_control"
description: ""
category: programming
tags: [ROS, python]
---
{% include JB/setup %}

I recently came back to the Robot Operating System after not working with it for nearly 2 years. The great thing about ROS is that everything is a debian package and most of it is written in python, a language that I feel very comfortable with. The bad thing about ROS is that everything is a debian package and most of it is written in a language that I feel comfortable in. In my experience, 90\% of ROS problems are due to not having the right debian packages, including the first problem I encountered out of the gate.

I wanted to get my [ros_realtime_plotter](https://github.com/CatherineH/ros_realtime_plotter) that I made for PyCon Canada 2015 working again. I followed my previous instructions starting with a fresh install of Ubuntu 16.04, but installed Kinetic Kame (instead of Indigo Igloo) and Gazebo 8.0.0 (instead of Gazebo 5.something). The first problem I encountered was some incompatibility between Kinetic Kame and Gazebo 8, so in future I would start off with gazebo 7.

My robot wouldn't move. The only warning or error message was:

```
[WARN] [1508501276.314154, 1090.261000]: Controller Spawner couldn't find the expected controller_manager ROS interface.
```

This error message was not particularly useful to me. I didn't understand what was meant by **ROS interface**. To learn more about this error message, I put [ros_control](https://github.com/ros-controls/ros_control) in my workspace and modified the [spawner script](https://github.com/ros-controls/ros_control/blob/kinetic-devel/controller_manager/scripts/spawner#L138) to print out the actual exception:

```python
        rospy.logwarn("Controller Spawner couldn't find the expected controller_manager ROS interface. %s" % e)
```

The error message was a timeout waiting for the service **/raz\_bot/controller\_manager/load\_controller**. Looking at rosservice, I could confirm that the service did not exist. I confirmed that my URDF had the code to load the gazebo ros controller:

```xml
  <!-- Gazebo plugin for ROS Control -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/</robotNamespace>
    </plugin>
  </gazebo>
```

It seemed like the robot spawner was just dying without a warning. So I set gazebo to have verbose output:

```xml
  <!-- Start the Gazebo simulator, loading a world -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find ros_realtime_plotter)/worlds/camera_above.world"/> <!-- world_name is wrt GAZEBO_RESOURCE_PATH environment variable -->
    <arg name="verbose" value="true" />
  </include>
```

This gave the error:

```
terminate called after throwing an instance of 'boost::exception_detail::clone_impl<boost::exception_detail::error_info_injector<boost::lock_error> >'
  what():  boost: mutex lock failed in pthread_mutex_lock: Invalid argument
```

Not particularly helpful. But, in a semi-related github issue Michael Koval demonstrated how you could isolate problems with the URDF spawner shared object library by [loading it in python](https://github.com/personalrobotics/or_urdf/issues/22#issuecomment-242800013).  

I did that, and had no issues. The next step was to check the gazebo ros control shared object library. I looking for it showed me the source of my problem:

```bash
$ find / 2>/dev/null | grep "gazebo_ros_control" 
/home/cholloway/ros/ros_control_ws/src/ros_control/ros_control/documentation/gazebo_ros_control.png
/home/cholloway/ros/ros_control_ws/src/ros_control/ros_control/documentation/gazebo_ros_control.pdf
/home/cholloway/ros/ros_control_ws/src/ros_control/ros_control/documentation/gazebo_ros_control.odg
```

The only files related to gazebo_ros_control were guides as to how to use ros_control with gazebo in the ros_control repository! I had assumed that the gazebo package came with these, and I was wrong.

The packages I needed were:

```
sudo apt-get install ros-kinetic-gazebo-ros-control ros-kinetic-diff-drive-controller
```

after that, the ros_realtime_plotter worked.




