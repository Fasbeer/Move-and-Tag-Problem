import collections
import matplotlib.path as mplPath
import numpy as np
import math
from shapely.geometry import LineString, Point, Polygon
import readFileFloat

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class Node:
    def __init__(self, id, coords, edges):
        self.id = id
        self.coords = coords
        self.edges = set(edges)

# Global variables

robotCoords = []

obstacles = []

# List of all the nodes that represent robots
nodes = []

robots = []

def insidePolygon2(node1, node2, polygons):
    ls = LineString([node1, node2])
    for polygon in polygons:
        if polygon.crosses(ls):
            return True
    return False

def checkIntersect(node1, node2, walls):
    ls = LineString([node1, node2])
    for wall in walls:
        if ls.crosses(wall):
            return True
    return False

def wallify(obstacles):
    walls = []
    for obstacle in obstacles:
        for i in range(0, len(obstacle)):
            if i == (len(obstacle) - 1):
                walls.append(LineString([obstacle[i], obstacle[0]]))
            else:
                walls.append(LineString([obstacle[i], obstacle[i + 1]]))
    return walls

def addEdges(walls, polygons):
    # Goes through all the nodes and adds edges that don't cross the polygons
    for node in nodes:
        for other in nodes:
            if node != other:
                if checkIntersect(node.coords, other.coords, walls):
                    continue
                if insidePolygon2(node.coords, other.coords, polygons):
                    continue
                else:
                    node.edges.add(other.id)

def listify(list, index):
    listified = []
    for tuple in list:
        listified.append(tuple[index])
    return listified

def containsRobots(obstacle):
    polygon = Polygon(obstacle)
    for robot in robotCoords:
        p = Point(robot)
        if polygon.contains(p):
            return True
    return False

def containObs():
    finalObs = []
    for obstacle in obstacles:
        listx = listify(obstacle, 0)
        listy = listify(obstacle, 1)
        slistx = sorted(listx)
        slisty = sorted(listy)
        lx = slistx[-1]
        sx = slistx[0]
        ly = slisty[-1]
        sy = slisty[0]
        final = [(lx, ly), (lx, sy), (sx, sy), (sx, ly)]
        if len(obstacle) <= 4 or containsRobots(final):
            finalObs.append(obstacle)
            continue
        finalObs.append(final)
    return finalObs

def initGraph():
    # Contain the obstacles
    containedObs = containObs()

    # This creates nodes from the obstacles and adds the edges to form the polygons
    counter = 0
    for obstacle in containedObs:
        for vertex in obstacle:
            if obstacle.index(vertex) == (len(obstacle) - 1):
                nodes.append(Node(counter, vertex, [counter - len(obstacle) + 1]))
                counter += 1
            else:
                nodes.append(Node(counter, vertex, [counter + 1]))
                counter += 1

    # Adds the robots as nodes
    for thing in robotCoords:
        robot = Node(len(nodes), thing, [])
        nodes.append(robot)
        robots.append(robot)

    # Goes through obstacles and creates a Polygon object using the set of points of each obstacle
    polygons = []
    for obstacle in containedObs:
        polygons.append(Polygon(obstacle))

    walls = wallify(containedObs)

    addEdges(walls, polygons)
    # This turns the directed graph into an undirected graph ?Maybe unnecessary
    for node in nodes:
        for other in nodes:
            if node.id in other.edges:
                node.edges.add(other.id)

#This finds the path from one node to another based on the output of the bfs algorithm
def findPath(dict, start, goal):
    current = goal
    path = [current]
    while current != start:
       current = dict[current]
       path.append(current)
    path.reverse()
    return path

def breadthFirstSearch(start, goal):
    queue = Queue()
    queue.put(start)
    cameFrom = {}
    cameFrom[start] = None

    while not queue.empty():
        current = queue.get()
        if current == goal:
            break

        for next in nodes[current].edges:
            if next not in cameFrom:
                queue.put(nodes[next].id)
                cameFrom[next] = current

    return cameFrom

# Gets distance between two coordinates
def getDistance(start, end):
    startX = start[0]
    startY = start[1]
    endX = end[0]
    endY = end[1]
    distance = math.sqrt(((endY-startY)**2 + (endX-startX)**2))
    return distance

# Gets distances from a list of paths represented as lists of coordinates
def getDistances(pathsCoords):
    distances = []
    for pathCoords in pathsCoords:
        distance = 0
        for i in range(0, len(pathCoords) - 1):
            distance += getDistance(pathCoords[1][i], pathCoords[1][i + 1])
        distances.append(distance)
    return distances

# Gets the coordinates of each node the path includes and appends the node the path leads to as a tuple
def getPathCoords(paths):
    pathsCoords = []
    for path in paths:
        pathCoords = []
        for node in path:
            pathCoords.append(nodes[node].coords)
        pathsCoords.append(pathCoords)
    # This bit appends the node the path leads to
    enumPathCoords = []
    for i in range(0, len(paths)):
        enumPathCoords.append((paths[i][-1], pathsCoords[i]))
    return enumPathCoords

# Runs bfs to find the path from a robot to the next closest robot
def getPath(movingRobot, sleepingRobots):
    paths = []
    # Finds the path between the nodes from the start robot to all the other robots and appends the path to paths
    for robot in sleepingRobots:
        path = findPath(breadthFirstSearch(movingRobot, robot), movingRobot, robot)
        paths.append(path)
    return paths

def getShortest(list):
    min = 999
    minValue = None
    for value in list:
        if value[1] != None and value[1] < min:
            min = value[1]
            minValue = value
    return minValue

# Appends the node/id of the robot to correspond the distance with the node
def enum(distances, sleepingRobots):
    enumDistances = []
    for i in range(0, len(distances)):
        enumDistances.append((sleepingRobots[i], distances[i]))
    return enumDistances

file = open("answers.txt", "w")
file.write("wolpertinger\n")
file.write("jgolc6tu0qtdtv55kqrljn1doe\n")

i = 2

robotCoords = readFileFloat.getRobotCoords(i - 1)
obstacles = readFileFloat.getObsCoords(i - 1)
initGraph()

# # Prints the edges of the nodes
# for node in nodes:
#     print(str(node.id) + ": " + str(node.edges))

awakeRobots = []
asleepRobots = []
awakeRobots.append(robots[0].id) # Add first robot to awakeRobots
for robot in robots[1:]: # Add the rest of the robots to asleepRobots
    asleepRobots.append(robot.id)

movements = [] # Where the final path is stored

while len(asleepRobots) > 0: # Runs until all the robots are awake
    paths = getPath(awakeRobots[-1], asleepRobots) # Gets path between the moving robot and robots that are asleep
    pathsCoords = getPathCoords(paths)
    distances = getDistances(pathsCoords)
    enumDistances = enum(distances, asleepRobots)
    shortest = getShortest(enumDistances)
    nextRobot = shortest[0] # Picks the next robot to be awoken based on the distance from the moving robot

    # Adds the path the robot has taken but needs some unpacking because of all the enum bullshit
    movement = []
    for robotPath in pathsCoords:
        if robotPath[0] == nextRobot:
            movement = robotPath[1]
            break
    movements.append(movement)

    # Changes the lists according to what robots have been awoken
    awakeRobots.append(nextRobot)
    asleepRobots.remove(nextRobot)

# Prints the answer in the format requested in the spec
ans = str(i) + ": "
for movement in movements:
    for node in movement:
        if node == movement[-1]:
            ans += str(node)
        else:
            ans += str(node) + ","
    if not movement == movements[-1]:
        ans += "; "
print(ans)
file.write(ans)
file.close()
