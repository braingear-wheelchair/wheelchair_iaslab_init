#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist

callback_topic = '/cmd_vel_tmp'
vel_topic = '/cmd_vel'
Hz = 100

def vel_callback(data: Twist):
    global current_vel, new_data
    current_vel = data
    current_vel.angular.z *=  (1 / 0.3506)
    new_data = True

def setup_listeners():
    rospy.Subscriber(callback_topic, Twist, vel_callback)

def init_globals():
    global  current_vel, new_data
    current_vel = Twist()
    new_data = False


def main():
    rospy.init_node('CompensateDivision')

    init_globals()
    setup_listeners()

    rate = rospy.Rate(Hz)

    global  current_vel, new_data
    pub = rospy.Publisher(vel_topic, Twist, queue_size=1)


    while not rospy.is_shutdown():
        global  current_vel, new_data
        if new_data:
            pub.publish(current_vel)
            new_data = False
        rate.sleep()
    
if __name__ == '__main__':
    main()
