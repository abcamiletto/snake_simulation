#!/usr/bin/env python

#--------INDICE---------#
#1- importo pacchetti
#2- inizializzo i publisher
#4- definisco i parametri
#5- respawn
#
#1--------------------------------------------------------------------- importo pacchetti
from operator import truediv
import rospy, yaml, sys
from std_msgs.msg import Float64
from numpy import zeros, array, linspace
import math
import rospkg
from control_sn.msg import param
from std_srvs.srv import Empty
import time


rospy.init_node('mycontrol')

time.sleep(4.)

#2--------------------------------------------------------------------- inizializzo i publisher

motor1p = rospy.Publisher('/snake/snake_body_1_joint_position_controller/command',Float64, queue_size = 121)
motor1y = rospy.Publisher('/snake/snake_body_1_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor2p = rospy.Publisher('/snake/snake_body_2_joint_position_controller/command',Float64, queue_size = 121)
motor2y = rospy.Publisher('/snake/snake_body_2_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor3p = rospy.Publisher('/snake/snake_body_3_joint_position_controller/command',Float64, queue_size = 121)
motor3y = rospy.Publisher('/snake/snake_body_3_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor4p = rospy.Publisher('/snake/snake_body_4_joint_position_controller/command',Float64, queue_size = 121)
motor4y = rospy.Publisher('/snake/snake_body_4_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor5p = rospy.Publisher('/snake/snake_body_5_joint_position_controller/command',Float64, queue_size = 121)
motor5y = rospy.Publisher('/snake/snake_body_5_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor6p = rospy.Publisher('/snake/snake_body_6_joint_position_controller/command',Float64, queue_size = 121)
motor6y = rospy.Publisher('/snake/snake_body_6_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor7p = rospy.Publisher('/snake/snake_body_7_joint_position_controller/command',Float64, queue_size = 121)
motor7y = rospy.Publisher('/snake/snake_body_7_aux_joint_position_controller/command',Float64, queue_size = 121)

pub_param = rospy.Publisher('/param', param, queue_size=10)




#4--------------------------------------------------------------------- ricevo i parametri

# def Callback2(data):
#     global a_p, ot_p, ox_p, a_y, ot_y, ox_y, V_m, Ph, k, count
#     a = data.A_p
#     b = data.Ot_p
#     c = data.Ox_p
#     d = data.A_y
#     e = data.Ot_y
#     f = data.Ox_y
#     g = data.V_m
#     h = data.Ph
#     i = data.K
#     count = data.COUNTER
#
# par = rospy.Subscriber ('/param', param, Callback2)


# GRID SEARCH DEFINITIVO
# for ox_y in range()
#     for a_p in range()
#         for a_y in range()
#             for v_med in range()

#
#             for k in range()


a=0
b = 0.88
c = 0.3
d = 0.05
e = 0.88
f = 0.3
g = 0
h = 0
i = 0
counter = 1


P = param()

P.A_p = a
P.Ot_p = b
P.Ox_p = c
P.A_y = d
P.Ot_y = e
P.Ox_y = f
P.V_m = g
P.Ph = h
P.K = i
P.COUNTER = counter

rospy.sleep(0.1)
pub_param.publish(P)


a = range(30)
var1span = [(x*0.35/30 + 0.05) for x in a]




for a in var1span:

    print("Tentativo n: " + str(counter) + "/8000 INIZIATO")
    P = param()

    P.A_p = a
    P.Ot_p = b
    P.Ox_p = c
    P.A_y = d
    P.Ot_y = e
    P.Ox_y = f
    P.V_m = g
    P.Ph = h
    P.K = i
    P.COUNTER = counter

    rospy.sleep(0.1)
    pub_param.publish(P)

    a_p = a * 3.14159
    ot_p = b * 3.14159
    ox_p = c * 3.14159

    a_y = d * 3.14159
    ot_y = e * 3.14159
    ox_y = f * 3.14159

    v_med = g * 3.14159
    ph = h * 3.14159
    k = i * 3.14159


    motor1p.publish(0.)
    motor2p.publish(0.)
    motor3p.publish(0.)
    motor4p.publish(0.)
    motor5p.publish(0.)
    motor6p.publish(0.)
    motor7p.publish(0.)

    motor1y.publish(0.)
    motor2y.publish(0.)
    motor3y.publish(0.)
    motor4y.publish(0.)
    motor5y.publish(0.)
    motor6y.publish(0.)
    motor7y.publish(0.)
    time.sleep(0.15)
    reset = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    resetta_tutto = reset()

    time.sleep(0.15)

    #6--------------------------------------------------------------------- pubblico nel topic
    sec = 1
    t = 0
    tic = rospy.Time.now()
    toc = rospy.Time.now() - tic
    # rateo di pubblicazione in Hz
    r = rospy.Rate(120)
    #da usare quando pubblico
    while t < 12:

        toc = rospy.Time.now() - tic
        t = (toc.secs * (10**9) + toc.nsecs)/(10**9 * 1.0000)
        
        if (sec % 120 == 0):
            print(str(sec/120))

        #ora assegno le sinusoidali al pitch
        msg1p = a_p*math.sin(t * ot_p + ox_p*0)
        msg2p = a_p*math.sin(t * ot_p + ox_p*1)
        msg3p = a_p*math.sin(t * ot_p + ox_p*2)
        msg4p = a_p*math.sin(t * ot_p + ox_p*3)
        msg5p = a_p*math.sin(t * ot_p + ox_p*4)
        msg6p = a_p*math.sin(t * ot_p + ox_p*5)
        msg7p = a_p*math.sin(t * ot_p + ox_p*6)

        #ora allo yaw
        msg1y = a_y * math.sin(t * ot_y + ox_y * 0 + ph) + v_med + 0 * k
        msg2y = a_y * math.sin(t * ot_y + ox_y * 1 + ph) + v_med + 1 * k
        msg3y = a_y * math.sin(t * ot_y + ox_y * 2 + ph) + v_med + 2 * k
        msg4y = a_y * math.sin(t * ot_y + ox_y * 3 + ph) + v_med + 3 * k
        msg5y = a_y * math.sin(t * ot_y + ox_y * 4 + ph) + v_med + 4 * k
        msg6y = a_y * math.sin(t * ot_y + ox_y * 5 + ph) + v_med + 5 * k
        msg7y = a_y * math.sin(t * ot_y + ox_y * 6 + ph) + v_med + 6 * k

        #pubblico

        motor1p.publish(msg1p)
        motor2p.publish(msg2p)
        motor3p.publish(msg3p)
        motor4p.publish(msg4p)
        motor5p.publish(msg5p)
        motor6p.publish(msg6p)
        motor7p.publish(msg7p)

        motor1y.publish(msg1y)
        motor2y.publish(msg2y)
        motor3y.publish(msg3y)
        motor4y.publish(msg4y)
        motor5y.publish(msg5y)
        motor6y.publish(msg6y)
        motor7y.publish(msg7y)

        sec += 1

        pd = True

        while pd:
            try:
                r.sleep()
                pd = False
            except:
                pass
    counter += 1












