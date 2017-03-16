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


def getRobotCoords(myText): #Outputs a list of tupples containing the coordinates of the robots
    myXList = []
    myYList = []
    splitList = myText.split('#') #Splits list into two sections - before and after the #
    newTest = splitList[0] #Turns the list into a string - the list above only contains one long element
    newTest1 = newTest.split(':') #Splits into before question marker and after - e.g 1: .....
    newTest1.pop(0) #Removes 1: from line
    robots2 = newTest1[0] #We just want first half of list now which contains the robot coordinates - the second half contains the obstacle coordinates
    robots1 = robots2.split(',') #Split list by commas for ease
    lenList = len(robots1)
    lenList1 = len(robots1)-1
    i = 0
    j = i+1

    while i <= lenList/2: #Looping through the list that we are left with from creations above
        while j <= lenList1:
            fixedx = robots1[i][1:] #Due to formatting issues, we need to clean up the numbers by removing the ( before x value
            fixedy = robots1[j][:-1] #Removing the ) after the y value
            newFix = fixedx[1:]
            myXList.append(float(newFix)) #Adding found values to our lists
            myYList.append(float(fixedy))
            i+=2
            j+=2

    zipped = zip(myXList, myYList) #Zip the x and y lists to create a list of tuples - remember haskell :)
    print(zipped)


def getObsCoords(myText): #Returns a list of lists with coordinates of each obstacle in a list
    myXList = []        #Uses list comprehension and shit
    myYList = []
    testList = []
    finalList = []
    splitList = myText.split('#')
    splitList.pop(0)
    newTest = splitList[0]
    testList.append(newTest)
    finalTest = newTest.split(';')
    for i in range(0,len(finalTest)-1):
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
    return finalList



myText = getText(2)

#getRobotCoords(myText)
obs = getObsCoords(myText)

polys = []
for ob in obs:
    polygon = []
    for coords in ob:
        polygon.append(vg.Point(*coords))
    polys.append(polygon)

#print(polygons)


#polys = [[vg.Point(1.0,6.0), vg.Point(1.0,1.0), vg.Point(5.0,1.0),vg.Point(5.0,5.0), vg.Point(3.0,5.0), vg.Point(3.0,3.0),vg.Point(4.0,3.0),vg.Point(4.0,2.0),vg.Point(2.0,2.0),vg.Point(2.0,6.0),
#vg.Point(6.0,6.0),vg.Point(6.0,0.0),vg.Point(0.0,0.0),vg.Point(0.0,6.0)]]

# g = vg.VisGraph()
# ans = g.build(polys)
g = vg.Graph(polys)
print(g)
#shortest = g.shortest_path(vg.Point(-29.0939934671409, -26.282070505327646), vg.Point(27.277154257681794, 29.286506198923735))
#print(shortest)

# g.save('graph.pk1')
# #g2 = VisGraph()
# g.load('graph.pk1')
