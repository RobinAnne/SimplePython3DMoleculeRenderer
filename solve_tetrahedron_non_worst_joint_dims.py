from operator import eq
import graphics.engine
from math import pi as PI
from math import sqrt
import numpy
from numpy.linalg import norm
import sympy

# DOES NOT CURRENTLY WORK

RENDER = False
TITLE = 'Tetra'
WIDTH, HEIGHT = 960, 540
DISTANCE = 20
SCALE = 40

def sympyNorm(v):
    s = 0
    for i in v:
        s += i**2
    return s

def angleBetween(v1: numpy.array, v2: numpy.array):
    return numpy.dot(v1, v2) /norm(v1)/norm(v2)

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

def planeEq(pt1, pt2):
    x, y, z, a, b, c, d = sympy.symbols('x,y,z,a,b,c,d')
    eq = sympy.Eq(a*x + b*y + c*z, d)
    eq1 = eq.subs([(x, pt1[0]), (y, pt1[1]), (z, pt1[2])])
    eq2 = eq.subs([(x, pt2[0]), (y, pt2[1]), (z, pt2[2])])
    print(eq1)
    print(eq2)
    s = sympy.solveset(eq1, eq2)
    print(s)

def ortho_vector(v):
    x, y, z = sympy.symbols('x,y,z')
    s = sympy.Array([x, y, z])
    s = sympy.Matrix([x, y, z])
    v = sympy.Matrix(v)
    
    eq1 = sympy.Eq(sympy.DotProduct(s, v), sympyNorm(s) * sympyNorm(v)) # joint direction vector square on bondvector
    eq2 = sympy.Eq(sympyNorm(s), 1)                                     # joint direction vector has len = 1
    print(eq1)
    print(eq2)
    s = sympy.solve([sympy.DotProduct(s, v) - sympyNorm(s)*sympyNorm(v), sympyNorm(s) -1], set=True)    
    print(s)


def solve_tetrahedron_for_ideal(pts):
    sols = []

ortho_vector([1, 1, 1])

r = 4

pts = [
    [[0, 0, 0],   {'type': 'C', 'col': 'violet', 'rad': 0.2, 'num': '0'}],
    [[1, 1, 1],   {'type': 'C', 'col': 'red', 'rad': 0.2, 'num': '0'}],
    [[-1, -1, 0], {'type': 'C', 'col': 'green', 'rad': 0.2, 'num': '0'}],
    [[0, 1, 0],   {'type': 'C', 'col': 'blue', 'rad': 0.2, 'num': '0'}],
    [[1, -2, -1], {'type': 'C', 'col': 'cyan', 'rad': 0.2, 'num': '0'}]]
i = 1

while i < len(pts):
    j = 0
    n = sqrt(pts[i][0][0]**2 + pts[i][0][1]**2 + pts[i][0][2]**2) / r
    while j < 3:
        pts[i][0][j] = pts[i][0][j]/n
        j += 1
    i += 10
atomSurfPoints, atomSurfTriangleIndices, atomSurfTrianglePoints = atomSurfacePointGen(pts)

print(angleBetween(pts[1][0], pts[2][0]))

points = []
lines = []
triangles = atomSurfTrianglePoints

planeEq(pts[0][0], pts[1][0])



if RENDER:
    eng = graphics.engine.Engine3D(points, lines, triangles, width=WIDTH, height=HEIGHT, distance=DISTANCE, scale=SCALE, title=TITLE)

    def animation():
        eng.clear()
        eng.render()
        eng.screen.after(1, animation)

    animation()
    eng.screen.tk.mainloop()
