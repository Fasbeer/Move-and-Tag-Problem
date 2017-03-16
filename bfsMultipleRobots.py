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
    def __init__(self, id, coords, edges, isRobot):
        self.id = id
        self.coords = coords
        self.edges = set(edges)
        self.isRobot = isRobot

robotCoords = [(0,1),(2,0),(3,5),(6,2),(9,0)]
#robotCoords = [(-1,-1),(4,4)]

obstacles = [[(1,2),(1,4),(3,4),(3,2)], [(8,1),(4,1),(4,4),(5,2)]]
#obstacles = [[(1,6),(1,1),(5,1),(5,5),(3,5),(3,3),(4,3),(4,2),(2,2),(2,6),(6,6),(6,0),(0,0),(0,6)]]

# Where all the nodes of the graph are stored
nodes = []

# This creates nodes from the obstacles and adds the edges to form the "polygons"
counter = 0
for obstacle in obstacles:
    for vertex in obstacle:
        if obstacle.index(vertex) == (len(obstacle) - 1):
            nodes.append(Node(counter, vertex, [counter - len(obstacle) + 1],False))
            counter += 1
        else:
            nodes.append(Node(counter, vertex, [counter + 1],False))
            counter += 1

# Adds the robots as nodes
for thing in robotCoords:
    nodes.append(Node(len(nodes), thing, [],True))

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
nodes[10].edges.update([1, 2, 3, 4, 5, 6, 11, 12])
nodes[11].edges.update([10, 4, 6, 7])
nodes[12].edges.update([4, 5, 6, 8, 9, 10])

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


def breadthFirstSearch(start, goal):
    queue = Queue()
    queue.put(start)
    cameFrom = {}
    cameFrom[start] = None
    while not queue.empty():
        current = queue.get()
        if current.id == goal.id:
            break
        for next in current.edges:
            if next not in cameFrom:
                queue.put(nodes[next])
                cameFrom[next] = current
    return cameFrom

def getDistance(start, end):
    startX = start[0]
    startY = start[1]
    endX = end[0]
    endY = end[1]
    distance = math.sqrt(((endY-startY)**2 + (endX-startX)**2))
    return distance

def getDistanceList(movingRobot, robotsList):
    distancesList = []
    print(robotsList)
    print(movingRobot)
    for i in range(1,len(robotsList)):
        cameFrom = breadthFirstSearch(nodes[robotsList[0]], nodes[robotsList[i]])
        # This finds the path from one node to another based on the output of the bfs algorithm
        current = nodes[robotsList[i]].id
        path = [current]
        while current != nodes[robotsList[0]].id:
           current = cameFrom[current].id
           path.append(current)
        path.reverse()
        #print(path)

        ans = []
        overallDistance = 0
        for node in path:
            ans.append(nodes[node].coords)
        # print(ans)
        # print("")

        for i in range(0,len(ans)-1):
            startCoord = ans[i]
            if (i+1) < len(ans):
                endCoord = ans[i+1]
            distance = getDistance(startCoord,endCoord)
            overallDistance += distance
        distancesList.append(overallDistance)
    print("Distances list is " + str(distancesList))
    return distancesList


def getShortest(distancesList):
    sortedList = sorted(distancesList)
    shortestValue = sortedList[0]
    for i in range(0,len(distancesList)):
        if distancesList[i] == shortestValue:
            #print("Robot to go to is " + str(i)))

            return i
        else:
            i+=1

def main():
    robotsList = []
    awakeRobots = []
    sleepingRobots = []
    for i in range(0,len(nodes)):
        robotCheck = nodes[i].isRobot
        if robotCheck:
            robotsList.append(i)

    awakeRobots.append(robotsList[0]) #Add first robot to awake robots list
    for i in range(1, len(robotsList)): #Add the rest of the robots to sleeping list
        sleepingRobots.append(robotsList[i])

    while len(sleepingRobots) > 0:
        distanceList = getDistanceList(awakeRobots[-1],robotsList)
        nextRobot = getShortest(distanceList)
        print("Next robot is " + str(nextRobot))
        awakeRobots.append(sleepingRobots[nextRobot])
        sleepingRobots.pop(nextRobot)

    # print(awakeRobots)
    # print(sleepingRobots)

        #add NODE value to awakeRobots

main()
