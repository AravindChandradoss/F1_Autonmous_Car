#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from control.msg import pid_input

desired_trajectory = 0
vel = 9

pub = rospy.Publisher('control/error', pid_input, queue_size=10)

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
	index=(theta)*4
	distance=data.ranges[index]
	return distance

def callback(data):
	theta = 45;   			 #angle between two selected rays
	ray_ll= 270-45;     			 #ANGLE left side left ray	
	ray_lf=ray_ll-theta     	 #ANLGE left side FRONT ray	
	ray_rr=45      		  	 # ""   RIGHT side LEFT ray	
	ray_rf=ray_rr+theta              # ""   RIGHT side FRONT ray
	ray_ff=135				#front ray
	ll = getRange(data,ray_ll)
	lf = getRange(data,ray_lf)   #DISTANCES 
	rf = getRange(data,ray_rf)
	rr = getRange(data,ray_rr)  
	ff = getRange(data,ray_ff)     #front	
	if(rr > ll):
		swing = math.radians(theta)
		x=rf*math.cos(swing)-rr
		y=rf*math.sin(swing)
		print("rr")
		alpha=math.atan(x/y) #equivalent to z=w/y; alpha=math.atan(z);	
	else:
		swing = math.radians(theta)
		x=lf*math.cos(swing)-ll
		y=lf*math.sin(swing)
		print("ll")
		alpha=-(math.atan(x/y)) #equivalent to z=w/y; alpha=math.atan(z);
	el=ll*math.cos(alpha)
	er=rr*math.cos(alpha)
	pl=2*math.sin(alpha)
	bias=0 		#to change the tracking point, if needed 
	error=-(el-er)+pl-bias
	alpha=alpha*180/3.14
	sw = -1
	if(alpha<5 and alpha>-5 and ff <2):
		sw=0 #turning
	elif(alpha<5 and alpha>-5 and ff >2):
		sw=1 #straight
	print("alpha =",alpha,"left dist = ",el,"right dis",er,"error",error, "sw=",sw)

#to turn the bot---------------------------------
#	if (alpha<=0.7 and alpha>=-0.7 and ff<3):
#		i=75:1:195
#		flag=-1;
#		maxi=0;
#		while (i<=195):
#			if((getRange(data,i)-getRange(data,i+1)>maxi):
#				flag=i
#				maxi=getRange(data,i)-getRange(data,i+1);
#			i=i+1
#		if(flag<135 and flag >75):
#			turn=0 #right
#		elif(flag>135 and flag < 195):
#			turn=1 #left
#	if(turn==0):
#		swing = math.radians(theta)
#		x=rf*math.cos(swing)-rr
#		y=rf*math.sin(swing)
#		alpha=math.atan2(x,y) #equivalent to z=w/y; alpha=math.atan(z);
#		er=rr*math.cos(alpha)
#		bias=2.5 		#to change the tracking point, if needed 
#		error=-(-er+bias)
#
#	elif(turn==1):
#		swing = math.radians(theta)
#		x=lf*math.cos(swing)-ll
#		y=lf*math.sin(swing)
#		alpha=-(math.atan2(x,y)) #equivalent to z=w/y; alpha=math.atan(z);
#		el=ll*math.cos(alpha)
#		bias=2.5 		#to change the tracking point, if needed 
#		error=-(el+bias)	
#-------------------------------------------------
	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	msg.pid_switch = sw
	pub.publish(msg)
	

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
