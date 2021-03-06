# Kelvin Silva. Did first part, can pass original test case.
# ----------
# Background
# 
# A robotics company named Trax has created a line of small self-driving robots 
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn. So to make a 
# right turn, A Traxbot will drive forward, stop, turn 90 degrees, then continue
# driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has 
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain 
# amount, and repeating this process... Luckily, the Traxbot is still sending all
# of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and 
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
# 
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon motion
# that is close to circular motion). Assume that Traxbot lives on 
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor 
# measurements. 
#
# With a few measurements you should be able to figure out the step size and the 
# turning angle that Traxbot is moving with.
# With these two pieces of information, you should be able to 
# write a function that can predict Traxbot's next location.
#
# You can use the robot class that is already written to make your life easier. 
# You should re-familiarize yourself with this class, since some of the details
# have changed. 
#
# ----------
# YOUR JOB
#
# Complete the estimate_next_pos function. You will probably want to use
# the OTHER variable to keep track of information about the runaway robot.
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *
from math import *
from matrix import *

import copy
import random


# This is the function you have to write. The argument 'measurement' is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.

dt = 1.041


#### DO NOT MODIFY ANYTHING ABOVE HERE ####
#### fill this in, remember to use the matrix() function!: ####

u = matrix([[0.], [0.], [0.], [0.], [0.], [0.] ]) # external motion inputted to the system


#since we have change in velocity (due to circular motion) need to model  1/2at^2
F =  matrix(
    [ [1., 0., dt, 0.,dt*dt/2., 0.],
      [0., 1., 0., dt, 0., dt*dt/2.],
      [0., 0., 1, 0., dt, 0.],
      [0., 0., 0., 1., 0., dt],
      [0., 0., 0., 0., 1., 0.],
      [0., 0., 0., 0., 0., 1.],
        ]
    )# next state function: generalize the 2d version to 4

Arr = copy.deepcopy(F.value)
for i in range(len(F.value)):
    for j in range(len(F.value[0])):
        Arr[i][j] *= 500
        
Q = matrix(Arr)
Q = Q.transpose()

print Q.value
H =  matrix(
    [ [ 1., 0., 0., 0., 0., 0.],
      [ 0., 1., 0., 0., 0., 0.],
      
        ]
    )# measurement function: reflect the fact that we observe x and y but not the two velocities
    
R = matrix(
    [ [ 0.00001, 0.0],
      [0.0, 0.00001],
        ]
    ) # measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
I = matrix(
    [ [1.0, 0., 0., 0., 0., 0.],
      [0., 1.0, 0., 0., 0., 0.],
      [0., 0., 1.0, 0., 0., 0.],
      [0., 0., 0., 1.0, 0., 0.],
      [0., 0., 0., 0., 1.0, 0.],
      [0., 0., 0., 0., 0., 1.0],
        ]
    )
    

        

P = matrix(
    [ [0., 0., 0., 0., 0., 0.],
      [0., 0., 0., 0., 0., 0.],
      [0., 0., 100., 0., 0., 0.],
      [0., 0., 0., 100., 0., 0.],
      [0., 0., 0., 0., 1000., 0.],
      [0., 0., 0., 0., 0., 1000.],
        ]
    ) # initial uncertainty: 0 for positions x and y, 1000 for the two velocities and accs
    
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    xy_estimate = []
 
    if not OTHER: # this is the first measurement
        OTHER = []
        OTHER.append( measurement)
        OTHER.append(P)
        x = matrix([ [OTHER[0][0]], [OTHER[0][1]], [0.], [0.], [0.], [0.] ]) # initial state (location and velocity, acc)
        OTHER[0] = x
        xy_estimate.append(OTHER[0].value[0][0])
        xy_estimate.append(OTHER[0].value[1][0])
    else:
        measurements = []
        measurements.append(measurement[0])
        measurements.append(measurement[1])

        OTHER[0], OTHER[1] = filterOnce(OTHER[0], OTHER[1], measurements)

        xy_estimate.append(measurement[0] + OTHER[0].value[2][0] + (OTHER[0].value[4][0]) /2. )
        xy_estimate.append(measurement[1] + OTHER[0].value[3][0] + (OTHER[0].value[5][0]) /2. )
        
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    
    
    return xy_estimate, OTHER 
    
def filterOnce(x, P, measurement):
    # prediction
    x = (F * x) + u
    P = F * P * F.transpose() + Q #added process covariance

    # measurement update
    Z = matrix([measurement])
    y = Z.transpose() - (H * x)
    S = H * P * H.transpose() + R
    K = P * H.transpose() * S.inverse()
    x = x + (K * y)

    P = (I - (K * H)) * P

    return x, P;
# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 10: 
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        print "Guess POS:"
        print position_guess
        print "TRUE POS: "
        print true_position
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 10:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(5.4, 4.888, 0.5, 2*pi / 34.0, 1.5)
test_target.set_noise(0.0, 0.0, 0.0)

demo_grading(estimate_next_pos, test_target)
