# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

import copy

def moveVertical(p, U, p_move):
    
    # for a no movement command
    if U == 0: # do not update probability map
        return p
    
    q = []
    pNoMoveTemp = copy.deepcopy(p)
    for i in range( len(p) ):
        for j in range (len(p[i])):
            pNoMoveTemp[i][j] = pNoMoveTemp[i][j] * (1 - p_move)

        
    # move array and calculate probability dist in case robot moves
    for i in range(len(p)):
        s = p[(i-U) % len(p)] # moved probabilities
        s = [ x * p_move for x in s] # multiply the list by probability
        q.append(s) #build shifted array
  
        
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = float(q[i][j]) + float(pNoMoveTemp[i][j])
    return q

def moveHorizontal(p, U, p_move): # move columns left or right

    # for a no movement command
    if U == 0: # do not update probability map
        return p
    
    # for movement commands
    # get move probability dist in case robot doesnt move
    q = []

    pNoMoveTemp = copy.deepcopy(p)
    for i in range( len(p) ):
        for j in range (len(p[i])):
            pNoMoveTemp[i][j] = float(pNoMoveTemp[i][j]) * (1. - float(p_move))
    #move array and calculate probability dist in case robot moves
    arrTemp = []

    for i in range(len(p)):
        for j in range( len(p[i]) ):
           
            s = float(p_move) * float(p[i][(j-U) % len(p[i])]) # moved probabilities
            arrTemp.append(s) #build shifted array
        
        q.append(arrTemp)
        arrTemp = []     # clear shifted array

    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = float(q[i][j]) + float(pNoMoveTemp[i][j])
    
 
    return q
    
    
def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    # >>> Insert your code here <<<
    # first, take the all sensor readings and update the probability map. if sensor = world, multiply by sensor_right probability.
    # assume number of measurements is the same as number or motions
    # assume p is same size as colors (world)
    
    #do robot movement first
    
    for a in range(len(measurements)): # assume measurements length is equal to motions length
    
        # robot moves. Probability map shifted
        p = moveHorizontal(p, motions[a][1], p_move) 
        p = moveVertical(p, motions[a][0], p_move)
     
        # robot senses. Probability map updated
        
        normalizationFactor = 0; 
       
        # update probability map with sensor readings and probability of sensor reading is correct
        for i in range( len(colors) ):
            for j in range (len(colors[i])):
                if (colors[i][j] == measurements[a]) :   # if reading matches world, multiply by probability reading is correct
                    p[i][j] = p[i][j] * sensor_right
                else:                                   # if readings does not match world, multiply by probability reading is not correct
                    p[i][j] = p[i][j] * ( 1. - sensor_right)    # wrong sensor reading means that the bot is not at this location in the world.
                normalizationFactor += p[i][j] # keep normalization factor updated (addition of all probabilities)
        # after multiplying probability, need to normalize the distribution
        
        for i in range( len(colors) ):
            for j in range(len(colors[i]) ):
                p[i][j] = p[i][j] / normalizationFactor
                
        
    
    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
measurements = ['G', 'G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
#motions = [[0,0], [0,1] ]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.7)

show(p) # displays your answer
