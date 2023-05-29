# DeadReckoning
Code for Dead Reckoning with 2 mice


For setting up the Raspberry Pi with laptop the following steps must be followed - 
1) Install VNC Viewer
2) Install Putty
3) The links to installation and detailed steps are given here - 
https://beebom.com/how-use-windows-laptop-as-monitor-raspberry-pi/

The code has three files - 
1) calib.py - Python file for Calibration that gives out X1, Y1, X2, Y2. It can be used for calibrating the DPI of mice as well as for calculating the distance between mice.
3) dr.py - Dead Reckoning file that gives out X, Y and Theta as the mouse moves.
4) motor_dr.py - Python file which integrates the function of running the motor as well as dead reckoning. This can be extended for purpose of curve following. 
