import graphics.engine
from math import pi as PI

# ==============================
# CONSTANTS
# ==============================

MODEL = 0
WIDTH, HEIGHT = 960, 540
DISTANCE = 20
SCALE = 40
MARK_ATOMS = [4, 9, 21, 23, 33, 43, 45, 56, 61, 62, 82, 83, 84]

# following CPK coloring
COLORS = {
    "H": "lightgray",
    "C": "black",
    "N": "blue",
    "O": "red",
    "S": "gold",
    "marked": "violet"}

RADII = {
    "H": 0.10,
    "C": 0.16,
    "N": 0.15,
    "O": 0.16,
    "S": 0.17,
    "marked": 0.2
}

if MODEL == 0:
    TITLE = "Molecule Renderer | Oxytocin | src: 3DChem"
    PATH = "./models/oxytocin_3Dchem.txt"
    FORMAT = {'atom': {'len': 70, 'type':31, 'indices':{0:[0, 10], 1:[11, 20], 2:[21, 30]}},
            'bond': {'len': 19, 'indices': {0: [0, 3], 1: [3, 6]}, 'multiplicity':8}}
elif MODEL == 1:
    TITLE = "Molecule Renderer | Oxytocin | src: MolView"
    PATH = "./models/oxytocin_molview.mol"
    FORMAT = {'atom': {'len': 70, 'type':31, 'indices':{0:[0, 10], 1:[11, 20], 2:[21, 30]}},
            'bond': {'len': 22, 'indices': {0: [0, 3], 1: [3, 6]}, 'multiplicity':8}}

# ==============================
# FUNCTIONS
# ==============================

def parseModel():
    FILE = open(PATH)
    atomPoints, bondIndices, bondPoints, i = [], [], [], 0
    for line in FILE:
        if len(line) == FORMAT['atom']['len']:
            x = line[FORMAT['atom']['indices'][0][0]:FORMAT['atom']['indices'][0][1]]
            y = line[FORMAT['atom']['indices'][1][0]:FORMAT['atom']['indices'][1][1]]
            z = line[FORMAT['atom']['indices'][2][0]:FORMAT['atom']['indices'][2][1]]
            t = line[FORMAT['atom']['type']]
            r = RADII[t]
            c = COLORS[t]
            if i in MARK_ATOMS:
                r = RADII['marked']
                c = COLORS['marked']
            #print(i, float(x), float(y), float(z), str(t))
            #print(line)
            atomPoints.append([[float(x), float(y), float(z)], {'num': i, 'type':t, 'col':c, 'rad': r}]) # cant be passed to renderer
            i += 1

        if len(line) == FORMAT['bond']['len']:
            first  = int(line[FORMAT['bond']['indices'][0][0]:FORMAT['bond']['indices'][0][1]]) -1
            second = int(line[FORMAT['bond']['indices'][1][0]:FORMAT['bond']['indices'][1][1]]) -1
            m      = int(line[FORMAT['bond']['multiplicity']])
            #print(first, second, m)
            #print(line)
            bondIndices.append([[first, second], {'multiplicity': m}])                      # cant be passed to renderer
            bondPoints.append([[atomPoints[first][0], atomPoints[second][0]], {'col': None, 'outline': 'black', 'multiplicity':m, 'nums': (first, second)}])
    FILE.close()
    return atomPoints, bondIndices, bondPoints

def atomSurfacePointGen(atomPoints, style='tetrahedron'):
    from math import acos, sin, cos
    a = acos(1/3)
    atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints, i = [], [], [], 0
    while i < len(atomPoints):
        p = atomPoints[i]
        co = p[0]
        r = p[1]['rad']
        c = p[1]['col']
        n = p[1]['num']
        atomSurfPoints.append([[co[0]+r*sin(a)          , co[1]                     , co[2] - r*cos(a)], {'col': c, 'outline': None, 'num': n}])
        atomSurfPoints.append([[co[0]-r*sin(a)*sin(PI/6), co[1] + r*sin(a)*cos(PI/6), co[2] - r*cos(a)], {'col': c, 'outline': None, 'num': n}])
        atomSurfPoints.append([[co[0]-r*sin(a)*sin(PI/6), co[1] - r*sin(a)*cos(PI/6), co[2] - r*cos(a)], {'col': c, 'outline': None, 'num': n}])
        atomSurfPoints.append([[co[0]                   , co[1]                     , co[2] + r       ], {'col': c, 'outline': None, 'num': n}])
        
        l = len(atomSurfPoints) - 4
        atomSurfTriangleIndices.append([[l,   l+1, l+2], {'col': c, 'outline': None, 'num': n}])
        atomSurfTriangleIndices.append([[l,   l+1, l+3], {'col': c, 'outline': None, 'num': n}])
        atomSurfTriangleIndices.append([[l,   l+2, l+3], {'col': c, 'outline': None, 'num': n}])
        atomSurfTriangleIndices.append([[l+1, l+2, l+3], {'col': c, 'outline': None, 'num': n}])

        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 1, 2]], {'col': c, 'outline': None, 'num': n}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 1, 2]], {'col': c, 'outline': None, 'num': n}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [0, 2, 3]], {'col': c, 'outline': None, 'num': n}])
        atomSurfTrianglePoints.append([[atomSurfPoints[l+x][0] for x in [1, 2, 3]], {'col': c, 'outline': None, 'num': n}])

        i += 1
    return atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints

def calcDirectionVectors(bondPoints):
    import math
    i = 0
    while i < len(bondPoints):
        d = [bondPoints[i][0][y] - bondPoints[i][1][y] for y in range(0, 3)]
        n = math.sqrt(d[0]**2 + d[1]**2 + d[2]**2)
        d = [x/n for x in d]
        if d[0] < 0:
            d = [-x for x in d]
        #print("Direction vector", d)
        i += 1

def calcBondAngles(atomPoints, bondIndices, bondPoints):
    import math
    p = bondAnglePointGen(atomPoints, bondIndices, bondPoints)
    bondAnglesAround, i = [], 0
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
                    alphas.append(round(alpha/PI*180, 1))
                i2 += 1
            i1 += 1
        bondAnglesAround.append([p[i][0], alphas])
        i += 1
    return bondAnglesAround

def bondAnglePointGen(atomPoints, bondIndices, bondPoints):
    connectedAtomIndices, connectedAtomPoints, i = [], [], 0 # [central point, [connected points]]
    while i < len(atomPoints):
        matchedIndices = []
        for j in bondIndices:
            if j[0][0] == i:
                matchedIndices.append(j[0][1])
            elif j[0][1] == i:
                matchedIndices.append(j[0][0])
        if len(matchedIndices) > 2:
            connectedAtomIndices.append([i, matchedIndices])
        i += 1
    for i in connectedAtomIndices:
        matchedPoints = [atomPoints[x][0] for x in i[1] if atomPoints[x][1]['num'] == x]
        connectedAtomPoints.append([i[0], atomPoints[i[0]][0], matchedPoints])
                                # centre atom index, centre atom point, bonded atom points
    return connectedAtomPoints

def logNonIdealAngles(bondAnglesAround, tolerance):
    a = [90, 120, 109.47, 180]
    for i in bondAnglesAround:
        bad_angle = False
        for j in i[1]:
            if abs(j-a[0]) > tolerance and abs(j-a[1]) > tolerance and abs(j-a[2]) > tolerance and abs(j-a[3]) > tolerance:
                bad_angle = True
                break
        if bad_angle:
            print("Non Ideal Angles (tol=", tolerance, "): ", i)

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

# ==============================
# EXECUTION
# ==============================

atomPoints, bondIndices, bondPoints = parseModel()
atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints = atomSurfacePointGen(atomPoints)

points = []
lines = bondPoints
triangles = atomSurfTrianglePoints

#calcDirectionVectors()
bondAnglesAround = calcBondAngles(atomPoints, bondIndices, bondPoints)
logNonIdealAngles(bondAnglesAround, 1)
#guidePlanes()



eng = graphics.engine.Engine3D(points, lines, triangles, width=WIDTH, height=HEIGHT, distance=DISTANCE, scale=SCALE, title=TITLE)

def animation():
    eng.clear()
    eng.render()
    eng.screen.after(1, animation)

animation()
eng.screen.tk.mainloop()
