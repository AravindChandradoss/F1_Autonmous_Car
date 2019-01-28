#!/usr/bin/env python

import rospy
from control.msg import drive_param
from control.msg import pid_input

def stop():
	rospy.init_node('stop_node', anonymous=True)
	pub = rospy.Publisher('control/drive_parameters', drive_param, queue_size=10)
	rate = rospy.Rate(10)
	msg = drive_param()
	msg.velocity = 0
	msg.angle = 0
	while not rospy.is_shutdown():
		pub.publish(msg)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		stop()
	except rospy.ROSInterruptException:
		pass
