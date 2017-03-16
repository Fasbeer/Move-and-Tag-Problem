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


def getCoords(myText):
    splitList = myText.split()
    splitList.pop(0)
    newList = splitList[0]
    bracketCount = 0
    closeBracketCount = 0
    first = False

    for i in range(0,len(newList)-1):
        currentChar = newList[i]
        #while currentChar != '#':
        if currentChar == '#':
            return
        if currentChar == '(':
            bracketCount+=1
            i+=1
            currentChar = newList[i]
        elif currentChar == ')':
            bracketCount+=1
            closeBracketCount+=1
            i+=1
            currentChar = newList[i]


        if bracketCount != 2:
            print(newList)
            while(currentChar!=','):
                print(currentChar)
                i+=1
                currentChar = newList[i]
                first  = True
            while(currentChar!=')' and first):
                print(currentChar)
                i+=1
                currentChar = newList[i]


            bracketCount=0
            first=False
            i+=2
            currentChar = newList[i]





            #return








myText = getText(1)
getCoords(myText)
