import graphics.screen
import copy
from time import perf_counter

class Engine3D:
    def __resetDrag(self, event):
        self.__prev = []
    
    def __drag(self, event):
        if self.__prev:
            self.rotate('y', (event.x - self.__prev[0]) / 20)
            self.rotate('x', (event.y - self.__prev[1]) / 20)
            self.clear()
            self.render()
        self.__prev = [event.x, event.y]

    def __select(self, event):
        zeros = self.screen.zeros
        event = (event.x, event.y)
        possibilities = []
        for a in range(-6, 5):
            for b in range(-6, 5):
                possibilities.append((event[0] + a, event[1] + b))
        projectedPoints = []
        for i in self.projectedItems:
            if len(i[0][0]) == 1:
                projectedPoints.append(i[0][0][0])
            elif len(i[0][0]) == 2:
                projectedPoints.append(i[0][0][0])
                projectedPoints.append(i[0][0][1])
            elif len(i[0][0]) == 3:
                projectedPoints.append(i[0][0][0])
                projectedPoints.append(i[0][0][1])
                projectedPoints.append(i[0][0][2])
        matches = []
        for i in self.projectedItems: # filter through all drawn objects in possibilities range and append the 'num' of the associated object to matches
            if len(i[0][0]) == 1:
                if i[0][0][0] in possibilities:
                    matches.append(i[0][1]['num'])
            if len(i[0][0]) == 2:
                pass # bonds are connected to two atoms
            if len(i[0][0]) == 3:
                if i[0][0][0] in possibilities or i[0][0][1] in possibilities or i[0][0][2] in possibilities:
                    matches.append(i[0][1]['num'])
        unique_matches = set(matches)
        weighted_matches = []
        for i in unique_matches: # go through all atom nums and weight them with their prevalence among the matched objects
            n = 0
            for j in matches:
                if j == i:
                    n += 1
            weighted_matches.append((i, n))
        
        weighted_matches = sorted(weighted_matches, key=lambda x: x[1]) # sort matches by weight
        print('weighted matches:', weighted_matches)
        if len(weighted_matches) > 0:
            max_weight = weighted_matches[0][1]
        else:
            print("Nothing selected")
        max_weight_matches = []
        for i in weighted_matches:
            if i[1] == max_weight:
                max_weight_matches.append(i[0])
        if len(max_weight_matches) > 1:
            print("Ambiguous selection. Please try again.")
        else:
            for i in self.triangles:
                if i[1]['num'] == max_weight_matches[0]:
                    selected_coordinate = i[0][0]
    
            self.__moveaxis = None
            self.__selected = selected_coordinate

            i = selected_coordinate
            print(self.__axis)
            print(i)
            self.__axis = [[copy.deepcopy(i) for a in range(2)] for b in range(3)]
            print(self.__axis)
            self.__axis[0][0][0] -= 40 / self.scale
            self.__axis[0][1][0] += 40 / self.scale
            self.__axis[1][0][1] -= 40 / self.scale
            self.__axis[1][1][1] += 40 / self.scale
            self.__axis[2][0][2] -= 40 / self.scale
            self.__axis[2][1][2] += 40 / self.scale
            z0 = self.screen.zeros[0]
            z1 = self.screen.zeros[1]
            self.__axis = [
                [
                    [
                        int(((x[0] * self.distance) / (x[2] + self.distance)) * self.scale) + z0,
                        int(((x[1] * self.distance) / (x[2] + self.distance)) * self.scale) + z1
                    ] 
                    for x in  y
                ]
                for y in self.__axis
            ]
            print(self.__axis)
            #self.__axis = [[point.flatten(self.scale, self.distance) for point in i] for i in self.__axis]
            #self.__axis = [[[i[0] + zeros[0], i[1] + zeros[1]] for i in j] for j in self.__axis]
            self.__axis = [self.screen.createArrow(self.__axis[0], 'red'), self.screen.createArrow(self.__axis[1], 'green'), self.screen.createArrow(self.__axis[2], 'blue')]

    def __selectx(self, event):
        self.__moveaxis = 'x'

    def __selecty(self, event):
        self.__moveaxis = 'y'

    def __selectz(self, event):
        self.__moveaxis = 'z'

    def __moveup(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.points[self.__selected].move(self.__moveaxis, 0.1)
            self.clear()
            self.render()

    def __movedown(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.points[self.__selected].move(self.__moveaxis, -0.1)
            self.clear()
            self.render()
    
    def __zoominout(self, event):
        self.scale += event.delta/80
        self.clear()
        self.render()

    def __zoomin(self, event):
        self.scale += 2.5
        self.clear()
        self.render()

    def __zoomout(self, event):
        self.scale -= 2.5
        self.clear()
        self.render()

    def __deselect(self, event):
        if self.__selected != None:
            self.__selected = None
            self.__axis = [self.screen.delete(line) for line in self.__axis]
            self.__moveaxis = None

    def __cameraleft(self, event):
        self.screen.zeros[0] -= 5
        self.clear()
        self.render()

    def __cameraright(self, event):
        self.screen.zeros[0] += 5
        self.clear()
        self.render()

    def __cameraup(self, event):
        self.screen.zeros[1] -= 5
        self.clear()
        self.render()

    def __cameradown(self, event):
        self.screen.zeros[1] += 5
        self.clear()
        self.render()
        
    def __init__(self, points, lines, triangles, width=1000, height=700, distance=6, scale=100, title='3D', background='white'):
        #object parameters
        self.distance = distance
        self.scale = scale

        #initialize display
        self.screen = graphics.screen.Screen(width, height, title, background)
        self.screen.tk.bind('<B1-Motion>', self.__drag)
        self.__prev = []
        self.screen.tk.bind('<ButtonRelease-1>', self.__resetDrag)
        self.screen.tk.bind("<MouseWheel>", self.__zoominout)

        self.screen.tk.bind('<Up>', self.__zoomin)
        self.screen.tk.bind('<Down>', self.__zoomout)
        self.screen.tk.bind('5', self.__cameraup)
        self.screen.tk.bind('2', self.__cameradown)
        self.screen.tk.bind('1', self.__cameraleft)
        self.screen.tk.bind('3', self.__cameraright)

        # this is for editing the model
        self.__selected = None
        self.__axis = []
        self.__moveaxis = None
        self.screen.tk.bind('<ButtonPress-3>', self.__select)
        self.screen.tk.bind('<ButtonRelease-3>', self.__deselect)
        self.screen.tk.bind('x', self.__selectx)
        self.screen.tk.bind('y', self.__selecty)
        self.screen.tk.bind('z', self.__selectz)
        self.screen.tk.bind('<Left>', self.__movedown)
        self.screen.tk.bind('<Right>', self.__moveup)
        
        self.points    = points
        self.lines     = lines
        self.triangles = triangles

        self.frame_times = [10 for i in range(30)]
        self.old_time = 0

    def clear(self):
        #clear display
        self.screen.clear()

    def rotate(self, axis, angle):
        #rotate model around axis
        from math import pi, sin, cos
        angle = angle / 450 * 180 / pi
        cosa = cos(angle)
        sina = sin(angle)
        i = 0

        def rot(p):
            if axis == 'z':
                return [p[0]*cosa - p[1]*sina, p[1]*cosa + p[0]*sina, p[2]]
            elif axis == 'x':
                return [p[0]                 , p[1]*cosa - p[2]*sina, p[2]*cosa + p[1]*sina]
            elif axis == 'y':
                return [p[0]*cosa - p[2]*sina, p[1]                 , p[2]*cosa + p[0]*sina]
            else:
                raise ValueError('invalid rotation axis')
        
        while i < len(self.points):
            self.points[i][0] = rot(self.points[i][0])
            i += 1
        i = 0
        while i < len(self.lines):
            self.lines[i][0][0] = rot(self.lines[i][0][0])
            self.lines[i][0][1] = rot(self.lines[i][0][1])
            i += 1
        i = 0
        while i < len(self.triangles):
            self.triangles[i][0][0] = rot(self.triangles[i][0][0])
            self.triangles[i][0][1] = rot(self.triangles[i][0][1])
            self.triangles[i][0][2] = rot(self.triangles[i][0][2])
            i += 1

    def render(self):
        projectedItems = []
        #calculate projected coordinates for points, lines, and triangles
        z0 = self.screen.zeros[0]
        z1 = self.screen.zeros[1]
        MODE = 1
        if MODE:

            for point in self.points:
                projectedItems.append(
                    (
                        (
                            (
                                (
                                    int(((point[0][0] * self.distance) / (point[0][2] + self.distance)) * self.scale) + z0,
                                    int(((point[0][1] * self.distance) / (point[0][2] + self.distance)) * self.scale) + z1
                                ),
                            ),
                            point[1]
                        ),
                        point[0][2]
                    )
                )
            
            for line in self.lines:
                projectedItems.append(
                    (
                        (
                            tuple(  
                                (
                                    int(((x[0] * self.distance) / (x[2] + self.distance)) * self.scale) + z0,
                                    int(((x[1] * self.distance) / (x[2] + self.distance)) * self.scale) + z1
                                )
                                for x in line[0]
                            ),
                            line[1]
                        ),
                        -(line[0][0][2] + line[0][1][2]) / 2
                    )
                )

            for triangle in self.triangles:
                projectedItems.append(
                    (
                        (
                        tuple(
                                (
                                    int(((x[0] * self.distance) / (x[2] + self.distance)) * self.scale) + z0,
                                    int(((x[1] * self.distance) / (x[2] + self.distance)) * self.scale) + z1
                                )
                                for x in triangle[0]
                            ),
                            triangle[1]
                        ),
                        -(triangle[0][0][2] + triangle[0][1][2] + triangle[0][2][2]) / 3
                    )
                )

            projectedItems = sorted(projectedItems, key=lambda x: x[1])
            
            for i in projectedItems:
                if len(i[0][0]) == 1:
                    self.screen.drawPoint(i[0])
                elif len(i[0][0]) == 2:
                    self.screen.drawLine(i[0])
                else:
                    self.screen.drawTriangle(i[0])
        elif MODE ==2:
            pass
            # use screen.drawAny

        # FPS counter
        t = perf_counter()
        self.frame_times =  self.frame_times[1:] + [t - self.old_time]
        self.screen.drawFPSCounter(round(1/(t - self.old_time), 1), round(1/(sum(self.frame_times)/len(self.frame_times)), 1))
        self.old_time = t

        #print(projectedItems)
        self.projectedItems = projectedItems

