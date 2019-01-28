#!/usr/bin/env python

import rospy
from control.msg import drive_values
from control.msg import drive_param
from std_msgs.msg import Bool

ang_bias = 10.0 # pwm bias to correct steering angle
pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
em_pub = rospy.Publisher('eStop', Bool, queue_size=10)

# function to map from one range to another, similar to arduino
def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# callback function on occurance of drive parameters(angle & velocity)
def callback(data):
	velocity = data.velocity
	angle = data.angle + ang_bias
	print("Velocity: ",velocity,"Angle: ",angle - ang_bias)
	# Do the computation
	pwm1 = arduino_map(velocity,-100,100,6554,13108);
	pwm2 = arduino_map(angle,-100,100,6554,13108);
	msg = drive_values()
	msg.pwm_drive = pwm1
	msg.pwm_angle = pwm2
	pub.publish(msg)

def talker():
	rospy.init_node('serial_talker', anonymous=True)
	em_pub.publish(False)
	rospy.Subscriber("control/drive_parameters", drive_param, callback)
	
	rospy.spin()

if __name__ == '__main__':
	print("Serial talker initialized")
	talker()
