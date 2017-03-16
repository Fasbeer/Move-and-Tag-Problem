import collections
import math

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

robotCoords = [(0,1),(2,0),(3,5),(6,2),(9,0)]
#robotCoords = [(-1,-1),(4,4)]

# List of all the nodes that represent robots
robots = []

obstacles = [[(1,2),(1,4),(3,4),(3,2)], [(8,1),(4,1),(4,4),(5,2)]]
#obstacles = [[(1,6),(1,1),(5,1),(5,5),(3,5),(3,3),(4,3),(4,2),(2,2),(2,6),(6,6),(6,0),(0,0),(0,6)]]

# Where all the nodes of the graph are stored
nodes = []

# This creates nodes from the obstacles and adds the edges to form the "polygons"
counter = 0
for obstacle in obstacles:
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

nodes[0].edges.update([8, 1, 3, 5, 9])
nodes[1].edges.update([0, 8, 2, 10, 6])
nodes[2].edges.update([1, 3, 4, 5, 6, 10])
nodes[3].edges.update([0, 2, 5, 6, 8, 9, 10])
nodes[4].edges.update([2, 5, 6, 7, 8, 9, 10, 11, 12])
nodes[5].edges.update([0, 2, 3, 4, 6, 8, 9, 10, 12])
nodes[6].edges.update([1, 2, 3, 4, 5, 7, 9, 10, 11, 12])
nodes[7].edges.update([11, 4, 6])
nodes[8].edges.update([0, 1, 3, 4, 5, 9, 12])
nodes[9].edges.update([0, 3, 4, 5, 6, 8, 12])
nodes[10].edges.update([1, 2, 3, 4, 5, 6, 11])
nodes[11].edges.update([10, 4, 6, 7])
nodes[12].edges.update([4, 5, 6, 8, 9])

# # Hardcoded edges between the robots and the polygon/s
# nodes[14].edges.update([13, 12, 11])
# nodes[15].edges.update([3, 4, 5, 6, 2])
#
# # Hardcoded edges between nodes of polygon
# nodes[0].edges.update([9, 8])
# nodes[1].edges.update([9, 8, 7])
# nodes[2].edges.update([6, 7, 8])
# nodes[3].edges.update([5, 6, 7])
# nodes[4].edges.update([6])

# This turns the directed graph into an undirected graph
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

def getDistance(start, end):
    startX = start[0]
    startY = start[1]
    endX = end[0]
    endY = end[1]
    distance = math.sqrt(((endY-startY)**2 + (endX-startX)**2))
    return distance

def getDistances(pathsCoords):
    distances = []
    for pathCoords in pathsCoords:
        distance = 0
        for i in range(0, len(pathCoords) - 1):
            distance += getDistance(pathCoords[1][i], pathCoords[1][i + 1])
        distances.append(distance)
    return distances

def getPathCoords(paths):
    pathsCoords = []
    for path in paths:
        pathCoords = []
        for node in path:
            pathCoords.append(nodes[node].coords)
        pathsCoords.append(pathCoords)
    enumPathCoords = []
    for i in range(0, len(paths)):
        enumPathCoords.append((paths[i][-1], pathsCoords[i]))
    return enumPathCoords

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

def enum(distances, sleepingRobots):
    enumDistances = []
    for i in range(0, len(distances)):
        enumDistances.append((sleepingRobots[i], distances[i]))
    return enumDistances

awakeRobots = []
asleepRobots = []
awakeRobots.append(robots[0].id) # Add first robot to awakeRobots
for robot in robots[1:]: # Add the rest of the robots to asleepRobots
    asleepRobots.append(robot.id)

movements = []

while len(asleepRobots) > 0:
    paths = getPath(awakeRobots[-1], asleepRobots)
    #print(paths)
    pathsCoords = getPathCoords(paths)
    #print(pathsCoords)
    distances = getDistances(pathsCoords)
    enumDistances = enum(distances, asleepRobots)
    #print(enumDistances)
    shortest = getShortest(enumDistances)
    nextRobot = shortest[0]

    movement = []
    for robotPath in pathsCoords:
        if robotPath[0] == nextRobot:
            movement = robotPath[1]
            break
    movements.append(movement)

    awakeRobots.append(nextRobot)
    asleepRobots.remove(nextRobot)

print(movements)
