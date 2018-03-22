# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------
import copy
# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):

    # ----------------------------------------
    # insert code here
    # ----------------------------------------

    checked = []
    open_list = []
    running_cost = 0

    # add init to open list

    open_list.append([0, copy.deepcopy(init)])  # g val starts w zero

    while 1:

        # find thing in open list with smallest g val that is also not in checked

        elem = min(open_list)
        while elem[1] in checked:
            open_list.remove(elem)
            elem = min(open_list)

        checked.append(elem)  # go and check
        open_list.remove(elem)  # remove from open list
        for i in range(len(delta)):  # expand to neighbors
            temp = copy.deepcopy(elem)
   
            temp[1][0] = temp[1][0] + delta[i][0]
            temp[1][1] = temp[1][1] + delta[i][1]

            # keep running g val

            if ( (temp[1][0] < 0 or temp[1][1] < 0) or ( (temp[1][0] >= len(grid) ) or (temp[1][1] >= len(grid[0])) ) ):
                continue
            test = copy.deepcopy([elem[0] + 1,copy.deepcopy(temp[1])])
            if grid[test[1][0]][test[1][1]] == 0:
                matches = [potential for potential in checked
                           if test[1] == potential[1]]
                if len(matches) == 0:
                    open_list.append(test)
            else:
                continue

        matches = [potential for potential in checked if potential[1]
                   == goal]
        if len(matches) > 0:
            return [matches[0][0], matches[0][1][0], matches[0][1][1]]
        elif len(open_list) == 0:
            return 'fail'

print search(grid,init,goal,cost)
