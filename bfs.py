import collections
from sympy import *
from numpy import arange

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

def insidePolygon(node1, node2, polygons):
    seg = Segment(node1, node2)
    arbPoint = seg.arbitrary_point()
    for polygon in polygons:
        for i in arange(0, 1.1, 0.1):
            p = arbPoint.subs(var('t',real=True), i)
            if polygon.encloses_point(p):
                return True
    return False

#robotCoords = [(0,1),(2,0),(3,5),(6,2),(9,0)]
robotCoords = [(-1,-1),(4,4)]

#obstacles = [[(1,2),(1,4),(3,4),(3,2)], [(8,1),(4,1),(4,4),(5,2)]]
obstacles = [[(1,6),(1,1),(5,1),(5,5),(3,5),(3,3),(4,3),(4,2),(2,2),(2,6),(6,6),(6,0),(0,0),(0,6)]]

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
    nodes.append(Node(len(nodes), thing, []))

# # Goes through obstacles and creates a Polygon object using the set of points of each obstacle
# polygons = []
# for obstacle in obstacles:
#     polygons.append(Polygon(*obstacle))
#
# #Goes through all the nodes and adds edges that don't cross the
# for node in nodes:
#     for other in nodes:
#         if node != other:
#             if not insidePolygon(node.coords, other.coords, polygons):
#                 node.edges.add(other.id)

# Hardcoded edges between the robots and the polygon/s
nodes[14].edges.update([13, 12, 11])
nodes[15].edges.update([3, 4, 5, 6, 2])

# Hardcoded edges between nodes of polygon
nodes[0].edges.update([9, 8])
nodes[1].edges.update([9, 8, 7])
nodes[2].edges.update([6, 7, 8])
nodes[3].edges.update([5, 6, 7])
nodes[4].edges.update([6])

# This turns the directed graph into an undirected graph
for node in nodes:
    for other in nodes:
        if node.id in other.edges:
            node.edges.add(other.id)

# # Prints the edges of the nodes
# for node in nodes:
#     print(str(node.id) + ": " + str(node.edges))

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

cameFrom = breadthFirstSearch(nodes[14].id, nodes[15].id)

print(cameFrom)

#This finds the path from one node to another based on the output of the bfs algorithm
current = nodes[15].id
path = [current]
while current != nodes[14].id:
   current = cameFrom[current]
   path.append(current)
path.reverse()

# Prints the answer in the format requested in the spec
ans = ""
for node in path:
    ans += str(nodes[node].coords) + ", "

print(ans)
