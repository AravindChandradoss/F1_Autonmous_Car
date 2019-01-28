#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
import curses
go = True

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
rospy.init_node('goStopNode', anonymous=True)
pub = rospy.Publisher('control/go', Bool, queue_size=10)

stdscr.refresh()

key = ''
stdscr.addstr(2, 5, "Car Status:     N/A    ")
stdscr.addstr(5, 5, "Key: G=Go S=Stop Q=Quit")
while key != ord('q'):
	key = stdscr.getch()
	stdscr.refresh()

	if key == ord('s'):
		go = False
		stdscr.addstr(2, 20, "Stopped")
	elif key == ord('g'):
		go = True
		stdscr.addstr(2, 20, "  GO!  ")

	pub.publish(go)
curses.endwin()
	
