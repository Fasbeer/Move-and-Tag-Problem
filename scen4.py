import math
from pprint import pprint

def move():
    # Creates a list containing 5 lists, each of 5 items, all set to 0
    w, h = 5, 5;
    matrix = [[0 for x in range(w)] for y in range(h)]
    coords = [(2,7),(2,3),(7,10),(9,5),(7,1)]

    for i in range(0,5):
        for j in range(0,5):
            if i!=j:
                iX = coords[i][0]
                iY = coords[i][1]
                jX = coords[j][0]
                jY = coords[j][1]
                distance = math.sqrt(((jY-iY)**2 + (jX-iX)**2))
                matrix[i][j] = distance



    pprint(matrix)



move()
