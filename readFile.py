def getText(lineNumber):
    f = open("robots.mat.txt")
    s=f.readline()
    for i in range(0,lineNumber+1):
        while s!="":
            if i==lineNumber:
                return s
            else:
                s=f.readline()
                i = i+1


def getRobotCoords(myText):
    myXList = []
    myYList = []
    splitList = myText.split()
    splitList.pop(0)
    new = splitList[0] #gets whole string in list
    new1 = new.split('#')
    #print(new1)
    robots = new1[0]
    #print(splitList)
    #obstacles = new1[1]
    robots1 = robots.split(',')
    #robots1 = [tuple(x) for x in robots1]
    #obstacles1 = obstacles.split(',')
    lenList = len(robots1)
    lenList1 = len(robots1)-1

    #print(robots1)

    i = 0
    j = i+1

    while i <= lenList/2:
        while j <= lenList1:
            xCount = j
            yCount = j+1

            fixedx = robots1[i][1:]
            fixedy = robots1[j][:-1]
            myXList.append(int(fixedx))
            myYList.append(int(fixedy))

            #print(fixedx)
            #print(fixedy)
            xCount+=2
            yCount+=2
            #print("i is " + str(i))
            #print("j is " + str(j))
            i+=2
            j+=2

    zipped = zip(myXList, myYList)
    #print(myXList)
    #print(myYList)
    print(zipped)


def getObsCoords(myText):
    myXList = []
    myYList = []
    splitList = myText.split()
    splitList.pop(0)
    new = splitList[0]
    new1 = new.split('#')
    #print(new1)
    obstacles = new1[1]
    obstacles1 = obstacles.split(',')
    #robots1 = [tuple(x) for x in robots1]
    #obstacles1 = obstacles.split(',')
    lenList = len(obstacles1)
    lenList1 = len(obstacles1)-1

    i = 0
    j = i+1

    while i <= lenList/2:
        while j <= lenList1:
            xCount = j
            yCount = j+1

            fixedx = obstacles1[i][1:]
            fixedy = obstacles1[j][:-1]
            myXList.append(float(fixedx))
            myYList.append(float(fixedy))

            #print(fixedx)
            #print(fixedy)
            xCount+=2
            yCount+=2
            #print("i is " + str(i))
            #print("j is " + str(j))
            i+=2
            j+=2

    zipped = zip(myXList, myYList)
    #print(myXList)
    #print(myYList)
    print(zipped)




myText = getText(1)

getRobotCoords(myText)
#getObsCoords(myText)
