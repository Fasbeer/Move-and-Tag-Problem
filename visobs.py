import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cmx
import matplotlib.colors as colors

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

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

def getPath(lineNumber): #Returns a specified question line from the file
    f = open("answers.txt")
    s=f.readline()
    for i in range(0,lineNumber+1):
        while s!="":
            if i==lineNumber:
                return s
            else:
                s=f.readline()
                i = i+1

def getPathCoords(questionNumber): #Returns a list of lists with coordinates of each path in a list
    myText = getPath(questionNumber)
    myXList = []        
    myYList = []
    testList = []
    finalList = []
    splitList = myText.split(':')
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
   
    plt.scatter(evenFloat,oddFloat, label= 'Robots', color='k', s=5)
    plt.scatter(evenFloat[0],oddFloat[0], label= 'Robots', color='r', s=5)
    
    
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


def drawPoly(questionNumber):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    N = 9
    #myPath = getPath(questionNumber)
    #path= []
    '''path = getPathCoords(questionNumber + 2)
    cmap = get_cmap(N)
    for i in range(0,len(path)):
        col = cmap(i)   
        line = plt.Polygon(path[i], closed=None, fill=None, edgecolor=col)
        ax.add_patch(line)'''
    
    getRobotCoords(questionNumber)#gets the robot coordinates from the text file
    
    verts = getObsCoords(questionNumber) #gets the Obs Coordinates from the text file
    for i in range(0,len(verts)):
        poly = plt.Polygon(verts[i])
        ax.add_patch(poly)
    
    

questionNumber = input('question number:');
#questionNumber = 4   
drawPoly(questionNumber)
plt.axis('scaled')
plt.show()
