import pyvisgraph as vg

def getText(lineNumber): #Returns a specified question line from the file
    f = open("robots.mat.txt")
    s=f.readline()
    for i in range(0,lineNumber+1):
        while s!="":
            if i==lineNumber:
                return s
            else:
                s=f.readline()
                i = i+1


def getRobotCoords(questionNumber): #Returns a list of lists with coordinates of each obstacle in a list
    myText = getText(questionNumber)
    myXList = []        #Uses list comprehension and shit
    myYList = []
    testList = []
    finalList = []
    splitList = myText.split('#')
    robots = splitList.pop(0)
    noColon = robots.split(':')
    noColon.pop(0)
    first = noColon[0].strip()
    #print(first)

    splitFirst = first.split(',')
    lenList = len(splitFirst)
    lenList1 = len(splitFirst)-1
    i = 0
    j = i+1
    even =  splitFirst[0:][::2] # even
    odd = splitFirst[1:][::2] # odd
    removing = [s.strip() for s in even]
    removing1 = [s[1:] for s in removing]
    removingOdd = [s.strip() for s in odd]
    removingOdd1 = [s[:-1] for s in removingOdd]
    evenFloat = [float(i) for i in removing1]
    oddFloat = [float(i) for i in removingOdd1]
    zipped = zip(evenFloat, oddFloat)
    finalList.append(zipped)
    #print(len(finalList[0]))
    return finalList[0]



def getObsCoords(questionNumber): #Returns a list of lists with coordinates of each obstacle in a list
    myText = getText(questionNumber)
    myXList = []        #Uses list comprehension and shit
    myYList = []
    testList = []
    finalList = []
    splitList = myText.split('#')
    splitList.pop(0)
    if len(splitList)>0:
        newTest = splitList[0]
        testList.append(newTest)
        finalTest = newTest.split(';')
        for i in range(0,len(finalTest)):
            first = finalTest[i]
            splitFirst = first.split(',')
            lenList = len(splitFirst)
            lenList1 = len(splitFirst)-1
            i = 0
            j = i+1
            even =  splitFirst[0:][::2] # even
            odd = splitFirst[1:][::2] # odd
            removing = [s.strip() for s in even]
            removing1 = [s[1:] for s in removing]
            removingOdd = [s.strip() for s in odd]
            removingOdd1 = [s[:-1] for s in removingOdd]
            evenFloat = [float(i) for i in removing1]
            oddFloat = [float(i) for i in removingOdd1]
            zipped = zip(evenFloat, oddFloat)
            finalList.append(zipped)
        #print(finalList)
        return finalList
    else:
        return []

def getPath(movingRobot, sleepingRobot):
    polys = []
    for ob in obs:
        polygon = []
        for coords in ob:
            polygon.append(vg.Point(*coords))
        polys.append(polygon)

    g = vg.VisGraph()
    g.build(polys)
    paths = []
    path = shortest = g.shortest_path(movingRobot, sleepingRobot)
    # Finds the path between the nodes from the start robot to all the other robots and appends the path to paths
    # for robot in sleepingRobots:
    #     path = shortest = g.shortest_path(movingRobot, robot)
    #     paths.append(path)

    return path


obs = getObsCoords(11)
robs = getRobotCoords(11)
awakeRobots = []
awakeRobots.append(robs[0])
asleepRobots = []
for robot in robs[1:]: # Add the rest of the robots to asleepRobots
    asleepRobots.append(robot)

awakeRobotsPoint = []
asleepRobotsPoint = []
finalPath = []



for rob in awakeRobots:
    awakeRobotsPoint.append(vg.Point(*rob))
for rob in asleepRobots:
    asleepRobotsPoint.append(vg.Point(*rob))

while len(asleepRobotsPoint) > 0:
    path = getPath(awakeRobotsPoint[-1], asleepRobotsPoint[0])
    finalPath.append(path)
    awakeRobotsPoint.append(asleepRobotsPoint[0])
    asleepRobotsPoint.pop(0)

#print(finalPath)

ans = ""
for movement in finalPath:
    for node in movement:
        if node == movement[-1]:
            ans += str(node)
        else:
            ans += str(node) + ","
    if not movement == finalPath[-1]:
        ans += "; "

print(ans)







#
# polys = []
# for ob in obs:
#     polygon = []
#     for coords in ob:
#         polygon.append(vg.Point(*coords))
#     polys.append(polygon)
#
# #print(polygons)
#
#
# #polys = [[vg.Point(1.0,6.0), vg.Point(1.0,1.0), vg.Point(5.0,1.0),vg.Point(5.0,5.0), vg.Point(3.0,5.0), vg.Point(3.0,3.0),vg.Point(4.0,3.0),vg.Point(4.0,2.0),vg.Point(2.0,2.0),vg.Point(2.0,6.0),
# #vg.Point(6.0,6.0),vg.Point(6.0,0.0),vg.Point(0.0,0.0),vg.Point(0.0,6.0)]]
# g = vg.VisGraph()
# g.build(polys)
#g = vg.Graph(polys)
#print(g)
#shortest = g.shortest_path(robots[0], robots[1])
#print(shortest)

# g.save('graph.pk1')
# #g2 = VisGraph()
# g.load('graph.pk1')
