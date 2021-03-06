#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from control_sn.msg import param
import time
import math
import os

x = 0
y = 0
a_p = 0
ot_p = 0
ox_p = 0
a_y = 0
ot_y = 0
ox_y = 0
v = [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
tor =  [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]


def effic(vel, torq, eng):
    eng += 1/100 * (torq[0] * vel[0] + torq[1] * vel[1] + torq[2] * vel[2] + torq[3] * vel[3] + torq[4] * vel[4] + torq[5] * vel[5] + torq[6] * vel[6] + torq[7] * vel[7] + torq[8] * vel[8] + torq[9] * vel[9] + torq[10] * vel[10] + torq[11] * vel[11] + torq[12] * vel[12] + torq[13] * vel[13])
    return eng;

def Callback1(data):
    global x, y
    x = data.x - 0.7
    y = data.y

def Callback2(data):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, V_m, Ph, k, count
    a_p = data.A_p
    ot_p = data.Ot_p
    ox_p = data.Ox_p
    a_y = data.A_y
    ot_y = data.Ot_y
    ox_y = data.Ox_y
    V_m = data.V_m
    Ph = data.Ph
    k = data.K
    count = data.COUNTER

def Callback3(data):
    global v, tor
    v = data.velocity
    tor = data.effort

p_path = os.path.dirname(os.path.realpath(__file__))
rospy.init_node('writer_csv')

with open("/home/andrea/Desktop/results/test2.csv", "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerow(['Attempt', 'Amplitude Pitch', 'Spatial frequency Pitch', 'Spatial frequency Pitch', 'Amplitude Yaw', 'Spatial frequency Yaw', 'Temporal frequency Yaw', 'Mean value', 'Phase', 'Constant', 'x', 'y', 'Distanza Totale', 'Distanza Percorsa', 'Energy'])
    wr.writerow([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    writeFile.close()

act_count = 1
act_x = 0
act_y = 0
dist_per = 0
r = rospy.Rate(100)
en = 0

rospy.Subscriber('/snake/joint_states', JointState, Callback3)
rospy.Subscriber('/my_odom', Pose2D, Callback1)
rospy.Subscriber('/param', param, Callback2)

time.sleep(1.)

while not rospy.is_shutdown():
    
    rospy.Subscriber('/snake/joint_states', JointState, Callback3)
    rospy.Subscriber('/my_odom', Pose2D, Callback1)
    rospy.Subscriber('/param', param, Callback2)
    
    dist = math.sqrt(x**2+y**2)
    dist_rel = math.sqrt((x-act_x)**2+(y-act_y)**2)
    dist_per += dist_rel
    en += 1/100 * (tor[0] * v[0] + tor[1] * v[1] + tor[2] * v[2] + tor[3] * v[3] + tor[4] * v[4] + tor[5] * v[5] + tor[6] * v[6] + tor[7] * v[7] + tor[8] * v[8] + tor[9] * v[9] + tor[10] * v[10] + tor[11] * v[11] + tor[12] * v[12] + tor[13] * v[13])
    if not a_p:
        pass

    else:
        
        line_to_override = {act_count:['Tentativo ' + str(act_count), a_p, ox_p, ot_p, a_y, ox_y, ot_y, V_m, Ph, k, round(x,3), round(y,3), round(dist,3), round(dist_per,3), en]}
        act_x = x
        act_y = y
        if act_count == count:
            empty = []
            with open(str(p_path)+"/results/test2.csv", 'r') as readFile:
                read = csv.reader(readFile, dialect='excel')
                empty.extend(read)
            with open(str(p_path)+"/results/test2.csv", 'w') as writeFile:
                wr = csv.writer(writeFile, dialect='excel')
                for line, row in enumerate(empty):
                    data = line_to_override.get(line, row)
                    wr.writerow(data)
                writeFile.close()
            pd = True

            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
            
        else:
            act_count = count
            dist_per = 0
            with open(str(p_path)+"/results/test2.csv", "a") as fp:
                wr = csv.writer(fp, dialect="excel")
                line_to_override = ['Tentativo ' + str(act_count), a_p, ox_p, ot_p, a_y, ox_y, ot_y, V_m, Ph, k, round(x,3), round(y,3), round(dist,3), round(dist_per,3), en]
                wr.writerow(line_to_override)
                fp.close()
            pd = True

            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
