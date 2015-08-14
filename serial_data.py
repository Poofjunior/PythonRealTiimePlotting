#!/usr/bin/env python
# Plot incoming serial data!
#
# Adapted from: https://hardsoftlucid.wordpress.com/various-stuff/realtime-plotting/
#
import pylab
import serial
from pylab import *
from collections import deque
from matplotlib.lines import Line2D


# Serial Data Settings
serial_port_name = "/dev/ttyACM0"

# Plot Settings
num_data_pts = 100
display_width = num_data_pts
display_y_min = 0
display_y_max = 65535

# How often the graphing utility check for new data and updates the graph.
graph_update_interval_ms = 20



# Setup Plottng Utility
x_axis = pylab.arange(0,100,1)
y_axis = pylab.array([0]*100)
fig = pylab.figure(1)
top = fig.add_subplot(212)
bottom = fig.add_subplot(211)
top.grid(True)
top.set_title("Real Time Plot")
top.set_xlabel("Time [us]")
top.set_ylabel("Amplitude")
line1 = Line2D([], [], color='black')
top.add_line(line1)

manager = pylab.get_current_fig_manager()

# Create a rolling buffer for the input y-axis data.
incoming_data = deque(pylab.arange(0,num_data_pts,1))
incoming_timestamp = deque(pylab.arange(0,num_data_pts,1))

# Setup Serial Port
# assume it's the first serial device
daq_port = serial.Serial(serial_port_name, 115200, timeout=1)

def getNewData():
## strings of data look like
## "[0]: <raw_data>"
## "[1]: <timestamp in microseconds>"
## "[0]: ..."
## "[1]: ..."
    global serial_data, daq_port
    ## don't forget to align to a [0]
    while (daq_port.inWaiting()):
        raw_serial_line = daq_port.readline()
        serial_line_data = raw_serial_line.split(" ")
        ### get the number 0 or 1 from "[0]:" or "[1]:"
        serial_data_type = serial_line_data[0]
        serial_data_type = serial_data_type.rstrip(":")
        serial_data_type = serial_data_type.lstrip("[")
        serial_data_type = serial_data_type.rstrip("]")
        # Discern timestamp from data
        if (int(serial_data_type) == 0): # data!
            # Second stripped value is actual data. Append it.
            incoming_data.append(int(serial_line_data[1]))
            # Remove old data at the start of the ring buffer.
            incoming_data.popleft()
        else: # timestamp!
            incoming_timestamp.append(int(serial_line_data[1]))
            incoming_timestamp.popleft()


def updatePlot(arg):
    global incoming_data, incoming_timestamp, line1, top, manager
    getNewData()
# Setup x and y data to be plotted.
    line1.set_data(incoming_timestamp,incoming_data)
    top.axis([incoming_timestamp[0], incoming_timestamp[-1],display_y_min,display_y_max])
    manager.canvas.draw()


timer = fig.canvas.new_timer(interval=graph_update_interval_ms)
timer.add_callback(updatePlot, ())
timer.start()

pylab.show()
