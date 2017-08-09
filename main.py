#!/usr/bin/python

import rosbag
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import easygui
import random as rd
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("bag_num", nargs='?', default="check_string_for_empty")
parser.add_argument("variable_plot1", nargs='?', default="check_string_for_empty")
parser.add_argument("variable_plot2", nargs='?', default="check_string_for_empty")
parser.add_argument("variable_plot3", nargs='?', default="check_string_for_empty")
parser.add_argument("variable_plot4", nargs='?', default="check_string_for_empty")
args = parser.parse_args()

if args.bag_num == '1':
    print 'Please wait! Executing script'
    bags = 1
elif args.bag_num == '2':
    print 'Please wait! Executing script'
    bags = 2
elif args.bag_num == '3':
    print 'Please wait! Executing script'
    bags = 3
elif args.bag_num == '4':
    print 'Please wait! Executing script'
    bags = 4
else:
    sys.exit("Error! Not a valid argument. Please enter 1 or 2 or 3 or 4")

bag_name = []

mpl.rcParams.update({'font.size': 36})


# Loop for number of desired graphs
for i in range(bags):
	bag_name.append(easygui.fileopenbox())


for i in range(bags):
	filename = bag_name[i]
	bag = rosbag.Bag(filename)
	x_pos=[]
	y_pos=[]
	z_pos=[]
	time_Flight_sec=[]
	time_Flight_nsec=[]
	time_Flight=[]
	x_Vicon=[]
	y_Vicon=[]
	z_Vicon=[]
	time_Vicon_sec=[]
	time_Vicon_nsec=[]
	time_Vicon=[]

	# Read time and z position form bagfile for estimate
	for topic, msg, t in bag.read_messages(topics='/crazyflie1/measured'):
		state=msg.values
		time_Flight_sec.append(msg.header.stamp.secs)
		time_Flight_nsec.append(msg.header.stamp.nsecs)
		x_pos.append(state[0])
		y_pos.append(state[1])
		z_pos.append(state[2])

	# Read time and z position form bagfile for vicon
	for topic2, msg2, t2 in bag.read_messages(topics='/vicon/markers'):
		for m in msg2.markers:
			if (m.translation.z/1000)>0:
				x_Vicon.append((m.translation.x/1000)-0.2)
				y_Vicon.append((m.translation.y/1000)-0.2)
				z_Vicon.append((m.translation.z/1000)-0.2)
				time_Vicon_sec.append(msg2.header.stamp.secs)
				time_Vicon_nsec.append(msg2.header.stamp.nsecs)
	bag.close()

	# ADD Seconds to nanoseconds
	for k in range(len(time_Flight_sec)):
		time_Flight_nsec[k]=float(time_Flight_nsec[k])/1000000000
		time_Flight.append(time_Flight_sec[k] + time_Flight_nsec[k])

	for k in range(len(time_Vicon_sec)):
		time_Vicon_nsec[k]=float(time_Vicon_nsec[k])/1000000000
		time_Vicon.append(time_Vicon_sec[k] + time_Vicon_nsec[k])

	# Make the vicon time the same as the flight time
	x_Vicon_adj=[]
	y_Vicon_adj=[]
	z_Vicon_adj=[]
	time_match=[]
	for k in range(len(time_Flight)):
		time_match=(min(range(len(time_Vicon)), key=lambda i: abs(time_Vicon[i]-time_Flight[k])))
		x_Vicon_adj.append(x_Vicon[time_match])
		y_Vicon_adj.append(y_Vicon[time_match])
		z_Vicon_adj.append(z_Vicon[time_match])

	print str((float(i+1)/float(bags))*100.0) + "% compleated"

	if bags == 1:
		if args.variable_plot1 == 'x':
			plot1 = x_pos
			plot2 = x_Vicon_adj
		elif args.variable_plot1 == 'y':
			plot1 = y_pos
			plot2 = y_Vicon_adj
		elif args.variable_plot1 == 'z':
			plot1 = z_pos
			plot2 = z_Vicon_adj
		axis = args.variable_plot1

		fig_1=plt.subplot(1, 1, i+1)
		fig_1.grid(True, lw = 2, ls = '--', c = '.75')
		fig_1.plot(time_Flight, plot1,linewidth=2, c='blue',label='Estimated Position')
		fig_1.plot(time_Flight, plot2,linewidth=2, c='red',label='Actual Position')
		fig_1.set_title('Comparing estimated posotion and real position', fontsize=70, y=1.5)
		fig_1.set_xlabel('time (s)', fontsize=50)
		fig_1.set_ylabel(axis + '-position (m)', fontsize=50)
		fig_1.legend(loc='best')

	elif bags == 2:
		fig_1=plt.subplot(2, 1, i+1)
		if i == 0:
			fig_1.set_title('Comparing estimated posotion and real position', fontsize=70)
			if args.variable_plot1 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot1 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot1 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot1

		if i == 1:
			if args.variable_plot2 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot2 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot2 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot2

		
		fig_1.grid(True, lw = 2, ls = '--', c = '.75')
		fig_1.plot(time_Flight, plot1,linewidth=2, c='blue',label='Estimated Position')
		fig_1.plot(time_Flight, plot2,linewidth=2, c='red',label='Actual Position')
		fig_1.set_xlabel('time (s)', fontsize=50)
		fig_1.set_ylabel(axis + '-position (m)', fontsize=50)
		fig_1.legend(loc='best')
	else:
		fig_1=plt.subplot(2, 2, i+1)
		if i == 0:
			fig_1.set_title('Comparing estimated posotion and real position', fontsize=70)
			if args.variable_plot1 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot1 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot1 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot1

		if i == 1:
			if args.variable_plot2 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot2 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot2 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot2

		if i == 2:
			if args.variable_plot3 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot3 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot3 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot3

		if i == 3:
			if args.variable_plot4 == 'x':
				plot1 = x_pos
				plot2 = x_Vicon_adj
			elif args.variable_plot4 == 'y':
				plot1 = y_pos
				plot2 = y_Vicon_adj
			elif args.variable_plot4 == 'z':
				plot1 = z_pos
				plot2 = z_Vicon_adj
			axis = args.variable_plot4

		
		fig_1.grid(True, lw = 2, ls = '--', c = '.75')
		fig_1.plot(time_Flight, plot1,linewidth=2, c='blue',label='Estimated Position')
		fig_1.plot(time_Flight, plot2,linewidth=2, c='red',label='Actual Position')
		fig_1.set_xlabel('time (s)', fontsize=50)
		fig_1.set_ylabel(axis + '-position (m)', fontsize=50)
		fig_1.legend(loc='best')


plt.show()
