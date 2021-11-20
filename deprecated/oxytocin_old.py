import graphics.engine
from math import pi as PI


MODEL = 0
if MODEL == 0:
    PATH = "C:/Users/robin/Documents/Projects/OXYTOCIN 3D/models/Oxytocin.txt"
    FORMAT = {'atom': {'len': 70, 'type':31, 'indices':{0:[3, 10], 1:[13, 20], 2:[23, 30]}},
            'bond': {'len': 19, 'indices': {0: [0, 3], 1: [3, 6]}, 'multiplicity':8}}
elif MODEL == 1:
    PATH = "C:/Users/robin/Documents/Projects/OXYTOCIN 3D/models/oxytocin_molview2.mol"
    FORMAT = {'atom': {'len': 70, 'type':31, 'indices':{0:[3, 10], 1:[13, 20], 2:[23, 30]}},
            'bond': {'len': 22, 'indices': {0: [0, 3], 1: [3, 6]}, 'multiplicity':8}}

COL = {
    "H": "lightgray",
    "C": "black",
    "N": "yellow",
    "O": "red",
    "S": "green",
    "marked": "pink"}

def parseModel():
    FILE = open(PATH)
    atomPoints, bondIndices, bondPoints, i = [], [], [], 0
    for line in FILE:
        if len(line) == FORMAT['atom']['len']:
            x = line[FORMAT['atom']['indices'][0][0]:FORMAT['atom']['indices'][0][1]]
            y = line[FORMAT['atom']['indices'][1][0]:FORMAT['atom']['indices'][1][1]]
            z = line[FORMAT['atom']['indices'][2][0]:FORMAT['atom']['indices'][2][1]]
            t = line[FORMAT['atom']['type']]
            #print(i, float(x), float(y), float(z), str(t))
            #print(line)
            i += 1
            atomPoints.append([[float(x), float(y), float(z)], {'num': i, 'type':str(t)}])
        if len(line) == FORMAT['bond']['len']:
            first  = int(line[FORMAT['bond']['indices'][0][0]:FORMAT['bond']['indices'][0][1]]) -1
            second = int(line[FORMAT['bond']['indices'][1][0]:FORMAT['bond']['indices'][1][1]]) -1
            m      = int(line[FORMAT['bond']['multiplicity']])
            #print(first, second, m)
            #print(line)
            bondIndices.append([[first, second], {'multiplicity': m}])
            bondPoints.append([[atomPoints[first][0], atomPoints[second][0]], {'col': None, 'outline': 'black', 'multiplicity':m}])
    FILE.close()
    return atomPoints, bondIndices, bondPoints

def atomSurfacePointGen2(atomPoints, markAtoms = [], style=['tetrahedron', 0.15]):
    from math import acos, sin, cos
    a = acos(1/3)
    atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints, i = [], [], [], 0
    while i < len(atomPoints):
        p = atomPoints[i]
        co = p[0]
        r = style[1]
        c = COL[p[1]['type']]
        r = style[1]
        if i in markAtoms:
            t = "marked"
            r = 0.3

        atomSurfPoints.append([[co[0]+r*sin(a)          , co[1]                     , co[2] - r*cos(a)], {'col': c, 'outline': 'blue'}])
        atomSurfPoints.append([[co[0]-r*sin(a)*sin(PI/6), co[1] + r*sin(a)*cos(PI/6), co[2] - r*cos(a)], {'col': c, 'outline': 'blue'}])
        atomSurfPoints.append([[co[0]-r*sin(a)*sin(PI/6), co[1] - r*sin(a)*cos(PI/6), co[2] - r*cos(a)], {'col': c, 'outline': 'blue'}])
        atomSurfPoints.append([[co[0]                   , co[1]                     , co[2] + r       ], {'col': c, 'outline': 'blue'}])
        
        l = len(atomSurfPoints) - 4 - 1
        atomSurfTriangleIndices.append([[l,   l+1, l+2], {'col': c, 'outline': None}])
        atomSurfTriangleIndices.append([[l,   l+1, l+3], {'col': c, 'outline': None}])
        atomSurfTriangleIndices.append([[l,   l+2, l+3], {'col': c, 'outline': None}])
        atomSurfTriangleIndices.append([[l+1, l+2, l+3], {'col': c, 'outline': None}])

        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 1, 2]], {'col': c, 'outline': None}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 1, 2]], {'col': c, 'outline': None}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 2, 3]], {'col': c, 'outline': None}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [1, 2, 3]], {'col': c, 'outline': None}])

        i += 1
    return atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints

atomPoints, bondIndices, bondPoints = parseModel()
atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints = atomSurfacePointGen2(atomPoints)

points = []
lines = bondPoints
triangles = atomSurfTrianglePoints


def atomCenterPointGen():
    for i in open(PATH):
        if i[0] != "#" and len(i) == 70:
            x = float(i[4:10])
            y = float(i[13:20])
            z = float(i[23:30])
            t = i[31]
            points.append([x, y, z, "atom", t])
            print([x, y, z, t])

def atomSurfacePointGen():
    import math
    col = {"H": "lightgray",
        "C": "black",
        "N": "yellow",
        "O": "red",
        "S": "green",
        "Mark": "pink"}
    a = math.acos(1/3)
    s = 0.15
    
    markAtom = 1
    i = 0
    while i < len(points):
        p = points[i]
        if len(p) != 4:
            print(i, p)
        if p[3] == "atom":
            t = p[4]
            if i == markAtom:
                t = "Mark"
                s = 0.3
            points.append([p[0]+s*math.sin(a),                     p[1],                                     p[2] - s*math.cos(a)])
            points.append([p[0]-s*math.sin(a)*math.sin(math.pi/6), p[1] + s*math.sin(a)*math.cos(math.pi/6), p[2] - s*math.cos(a)])
            points.append([p[0]-s*math.sin(a)*math.sin(math.pi/6), p[1] - s*math.sin(a)*math.cos(math.pi/6), p[2] - s*math.cos(a)])
            points.append([p[0],                                   p[1],                                     p[2] + s            ])
            if i == markAtom:
                s = 0.15
            l = len(points)-4
            triangles.append([l,   l+1, l+2, col[t]])
            triangles.append([l,   l+1, l+3, col[t]])
            triangles.append([l,   l+2, l+3, col[t]])
            triangles.append([l+1, l+2, l+3, col[t]])
            points[i] = points[i][:3]
        i += 1

def bondLineIndexGen():
    file = open(PATH)
    for i in file:
        if len(i) == FORMAT:
            first = int(i[0:3])
            second = int(i[3:6])
            amount = int(i[6:9])
            lines.append([first-1, second-1, 'black'])
            #print(first, second)
            print("line:", first, second, i)

def calcDirectionVectors():
    import math
    r = 5
    p = bondLinePointGen()
    i = 0
    while i < len(p):
        #d = [p[i][0][0]-p[i][1][0], p[i][0][1]-p[i][1][1], p[i][0][2]-p[i][1][2]]
        d = [p[i][0][y] - p[i][1][y] for y in range(0, 3)]
        n = math.sqrt(d[0]**2 + d[1]**2 + d[2]**2)
        d = [x/n for x in d]
        if d[0] < 0:
            d = [-x for x in d]
        #print("Direction vector", d)
        i += 1

def calcBondAngles():
    import math
    r = 5
    p = bondAnglePointGen()
    i = 0
    while i < len(p):
        directionVectors = []
        p0 = p[i][1]
        for j in p[i][2]:
            directionVectors.append([j[c] - p0[c] for c in range(0, 3)])
        alphas = []
        i1 = 0
        while i1 < len(directionVectors):
            i2 = 0
            while i2 < len(directionVectors):
                if i1 < i2: # removes duplicates --> 12, 13, 14, 23, 24, 34 done
                    j, k = directionVectors[i1], directionVectors[i2]
                    alpha = math.acos(sum(j[x]*k[x] for x in range(0, 3))/math.sqrt((j[0]**2+j[1]**2+j[2]**2)*(k[0]**2+k[1]**2+k[2]**2)))
                    alphas.append(round(alpha/math.pi*180, 1))
                i2 += 1
            i1 += 1

        print("Atom bond angles around ", p[i][0], ": ", alphas)
        i += 1 

def bondLinePointGen():
    p = []
    for i in open(PATH):
        if len(i) == 70:
            x = float(i[4:10])
            y = float(i[13:20])
            z = float(i[23:30])
            t = i[31]
            p.append([x, y, z, t])
            
            #print([x, y, z, t])
        if len(i) == 19:
            first = int(i[0:3])
            second = int(i[3:6])
            amount = int(i[6:9])
            bonds2x3.append([p[first-1], p[second-1]])
            #print(first, second)
    return bonds2x3

def bondAnglePointGen():
    p, bondIndices = [], []
    for i in open(PATH):
        if len(i) == 70:
            x = float(i[4:10])
            y = float(i[13:20])
            z = float(i[23:30])
            t = i[31]
            p.append([x, y, z])
        if len(i) == FORMAT:
            first = int(i[0:3])
            second = int(i[3:6])
            bondIndices.append([first-1, second-1])
    i = 0
    connectedAtomIndices, connectedAtomPoints = [], [] # [central point, [connected points]]
    while i < len(p):
        matchedIndices = []
        for j in bondIndices:
            if j[0] == i:
                matchedIndices.append(j[1])
            elif j[1] == i:
                matchedIndices.append(j[0])
        if len(matchedIndices) > 2:
            connectedAtomIndices.append([i, matchedIndices])
        i += 1

    for i in connectedAtomIndices:
        matchedPoints = [p[x][:3] for x in i[1]]
        connectedAtomPoints.append([i[0], p[i[0]], matchedPoints])

    return connectedAtomPoints

def guidePlanes():
    import math
    a = math.acos(1/3)
    x, y, z = 4, 5, 8
    p1 = [[-x, -y, 0], [x+3, -y, 0], [-x, y, 0], [x+3, y, 0]]
    p2 = [[z*math.sin(a), -y, -z*math.cos(a)], [-z*math.sin(a), -y, -z*math.cos(a)], [z*math.sin(a), y, z*math.cos(a)], [-z*math.sin(a), y, z*math.cos(a)]]
    p3 = [[z*math.sin(a), -y, z*math.cos(a)], [-z*math.sin(a), -y, z*math.cos(a)], [z*math.sin(a), y, -z*math.cos(a)], [-z*math.sin(a), y, -z*math.cos(a)]]
    global points
    points += p1
    points += p2
    points += p3
    l = len(points) - 12
    triangles.append([l  , l+1, l+2, "gray", None])
    triangles.append([l+1, l+2, l+3])
    triangles.append([l+4, l+5, l+6])
    triangles.append([l+5, l+6, l+7])
    triangles.append([l+8, l+9, l+10])
    triangles.append([l+9, l+10, l+11])


#atomCenterPointGen()
#atomSurfacePointGen()
#bondLineIndexGen()
#calcDirectionVectors()
#calcBondAngles()
#guidePlanes()

eng = graphics.engine.Engine3D(points, lines, triangles, width=1800, height=1000, distance=20, scale=40, title='Oxy')

def animation():
    eng.clear()
    eng.render()
    eng.screen.after(1, animation)

animation()
eng.screen.window.mainloop()
