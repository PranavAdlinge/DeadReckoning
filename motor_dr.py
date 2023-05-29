from evdev import InputDevice, categorize, ecodes
import math
import time
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

AN2 = 25 #pwm2 pin on Driver to GPIO25
AN1 = 24 #pwm1 pin on Driver to GPIO24
DIG2 = 23 #dir2 pin on Driver to GPIO23
DIG1 = 18 #dir1 pin on Driver to GPIO18

GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)

sleep(2)
p1 = GPIO.PWM(AN1, 100) #set pwm for M1
p2 = GPIO.PWM(AN2, 100) #set pwm for M2


device1 = InputDevice('/dev/input/event1')
device2 = InputDevice('/dev/input/event4')


#Always put the marked mouse at position 1
dpc1 = 1963.535
dpc2 = 1973.95
X, Y , Theta = 0,0,0
D = 9.1
count = 0
max_mov = 0
time_mean = 0
try:
    while True:
        s = time.time()
        count += 1
        ####################################################
        #Equation
        
        itera = 1000000
        #per second
        speed = 4
        #v(t) as a function of x and y
        v_y = speed/itera
        v_x = 0
        
        
        
        
        event1 = device1.read_one()
        event2 = device2.read_one()
        x1_d, y1_d = 0, 0
        x2_d, y2_d = 0, 0
        if event1 is not None:
            if event1.type == ecodes.EV_REL:
                if event1.code == ecodes.REL_X:
                    x1_d = event1.value
                elif event1.code == ecodes.REL_Y:
                    y1_d = -event1.value
        if event2 is not None:
            if event2.type == ecodes.EV_REL:
                if event2.code == ecodes.REL_X:
                    x2_d = event2.value
                elif event2.code == ecodes.REL_Y:
                    y2_d = -event2.value
                    
        max_mov = max(x1_d, y1_d, x2_d, y2_d,max_mov)
        #Converting to centimeters for First mouse
        x1_c = x1_d/dpc1
        y1_c = y1_d/dpc1
        
        #Converting to centimeters for Second mouse
        x2_c = x2_d/dpc2
        y2_c = y2_d/dpc2
        
        
        
        delta_x = (x1_c+x2_c)/2
        delta_y = (y1_c+y2_c)/2
        
        #u vector
        u_x = delta_x
        u_y = delta_y
        
        delta_theta = math.atan2(y1_c - y2_c, x1_c - x2_c + D)
        Theta += delta_theta
        
        delta_x_global = math.cos(Theta)*delta_x + math.sin(Theta)*delta_y
        delta_y_global = -math.sin(Theta)*delta_x + math.cos(Theta)*delta_y
        
        X += delta_x_global
        Y += delta_y_global
        e = time.time()
        time_mean += (e-s)
        
        #p vector
        p_x = 0
        p_y = speed*time
        
        #q vector
        q_x = X
        q_y = Y
        
        
        if count%50000==0:
            print("C:%d, X:%f, Y:%f, Theta:%f\n"%(count/50000 ,X, Y,math.degrees(Theta)))
            #print("Maximum Movement:",max_mov)
            #print("Average time:",time_mean/count)
            

except KeyboardInterrupt:     
    device1.close()
    device2.close()
    
 
    

