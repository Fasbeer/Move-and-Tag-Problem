# This solution doesn't allow the robots to move at the same time and doesn't allow for obstacles. These are the next steps with obstacles being a priority.

import math
# Use pprint to print a matrix in a clearer way
from pprint import pprint

class Robot:
    def __init__(self, number, coords):
        self.number = number
        self.coords = coords
        self.isAwake = 0

class Movement:
    def __init__(self, robotNumber, startCoords, endCoords):
        self.robotNumber = robotNumber
        self.startCoords = startCoords
        self.endCoords = endCoords

numRobots = 7

robot0 = Robot(0, (0, 0))
robot1 = Robot(1, (10, 10))
robot2 = Robot(2, (8, 10))
robot3 = Robot(3, (9, 9))
robot4 = Robot(4, (5, 0))
robot5 = Robot(5, (0, 7))
robot6 = Robot(6, (1, 8))

robots = [robot0, robot1, robot2, robot3, robot4, robot5, robot6]
movements = []

# This replaces distance values in the matrix with None values for robots that have been woken
# Right now I don't understand why it works so don't touch it lol
def cleanMatrix(matrix, number):
    for row in matrix:
        if matrix.index(row) == number:
            for value in row:
                value = None
        else:
            row[number] = None
    return matrix

# This function returns 0 when all the robots are awake in order to stop the while loop at the bottom
def notAwake():
    for robot in robots:
        if not robot.isAwake:
            return 1
    return 0

# This just returns the robot instance by providing its robot number
def findRobot(number):
    for robot in robots:
        if robot.number == number:
            return robot

# This finds the shortest distance in a row in the matrix and returns a tuple like this: (index, value)
def shortest(list):
    min = 999
    minValue = None
    for value in list:
        if value[1] != None and value[1] < min:
            min = value[1]
            minValue = value
    return minValue

#This finds the distance of the robots from each other and fills the matrix
def distance(matrix):
    for i in range(0,numRobots):
        for j in range(0,numRobots):
                iX = robots[i].coords[0]
                iY = robots[i].coords[1]
                jX = robots[j].coords[0]
                jY = robots[j].coords[1]
                distance = math.sqrt(((jY-iY)**2 + (jX-iX)**2))
                if distance == 0:
                    matrix[i][j] = None
                else:
                    matrix[i][j] = round(distance)
    return matrix

# This creates the matrix/2d array
matrix = distance([[0 for x in range(numRobots)] for y in range(numRobots)])

# This initialises the process by waking up the first robot
currentRobot = robot0
robot0.isAwake = 1

# This is the main process
while notAwake():
    # This finds the next robot the current robot will wake up by finding the shortest distance in its row in the matrix
    # It uses enumerate which is a function that provides the index of the value with the value in the tuple
    next = findRobot(shortest(list(enumerate(matrix[currentRobot.number])))[0])
    # This adds the movement of the robot to a list that is then printed at the end
    movements.append(Movement(currentRobot.number, currentRobot.coords, next.coords))
    # Wakes up the robot that has just been travelled to
    next.isAwake = 1
    # For this look at the comment on the function
    matrix = cleanMatrix(matrix, currentRobot.number)
    # The next robot is then selected to move for the next iteration
    currentRobot = next

#This prints the movements of each robot between coordinates
for movement in movements:
    print(str(movement.robotNumber) + ": " + str(movement.startCoords) + " -> " + str(movement.endCoords))
