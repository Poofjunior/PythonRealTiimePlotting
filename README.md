Python Real Time Plotting
=========================

a minimalistic script for capturing (and plotting) data from the serial port

# Setup
I'll assume you can control the data from the incoming serial port. That said,
data should take the following ascii string format
    
    ...
    [0]: 100
    [1]: 34521
    [0]: 101
    [1]: 34524
    [0]: 102
    [1]: 34527
    ...
    
where **[0]** is the y-axis data and **[1]** is the x-axis data (assumed to be
a timestamp)
