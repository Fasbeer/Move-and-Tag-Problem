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


print(getRobotCoords(0))
print(getObsCoords(0))


# amountOfRobots = []
# amountOfObstacles = []
# # for i in range(0,29):
# #     myText = getText(i)
# # #
# #     amountOfRobots.append(getRobotCoords(myText))
# #     amountOfObstacles.append(getObsCoords(myText))
# #
# # zippedList = zip(amountOfRobots,amountOfObstacles)
# # print(zippedList)
# for i in range(0,29):
#     myText = getText(i)
#     listOfObs = getObsCoords(myText)
#     mySum = 0
#     for obs in listOfObs:
#         noCoords = len(obs)
#         mySum+=noCoords
#     print(mySum)
# #getObsCoords(myText)
