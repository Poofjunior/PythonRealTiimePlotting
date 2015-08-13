#!/usr/bin/env python
# Plot incoming serial data!
#
# Adapted from: https://hardsoftlucid.wordpress.com/various-stuff/realtime-plotting/
#
import pylab
import serial
from pylab import *
from collections import deque

# Serial Data Settings
serial_port_name = "/dev/ttyACM0"

# Plot Settings
num_data_pts = 100
display_width = num_data_pts
display_y_min = 0
display_y_max = 65535



# Setup Plottng Utility
xAchse=pylab.arange(0,100,1)
yAchse=pylab.array([0]*100)
fig = pylab.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Realtime Waveform Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([0,display_width,display_y_min,display_y_max])
line1=ax.plot(xAchse,yAchse,'-')

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
    global incoming_data, incoming_timestamp
    getNewData()
# Setup x and y data to be plotted.
    line1[0].set_data(incoming_timestamp,incoming_data)
    ax.axis([incoming_timestamp[0], incoming_timestamp[-1],display_y_min,display_y_max])
    manager.canvas.draw()


timer = fig.canvas.new_timer(interval=20)
timer.add_callback(updatePlot, ())
timer.start()

pylab.show()
