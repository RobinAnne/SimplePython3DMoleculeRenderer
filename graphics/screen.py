import tkinter

class Screen:
    def __init__(self, width, height, title, background):
        #calculate center of screen
        self.zeros = [int(width/2), int(height/2)]

        #initialize tkinter tk for displaying graphics
        self.tk = tkinter.Tk()
        self.tk.title(title)
        self.canvas = tkinter.Canvas(self.tk, width=width, height=height, bg=background)
        self.canvas.pack()

        self.fps_counter_anchor = "se"
        self.fps_counter_fontsize = 20
        self.fpsExt_counter_fontsize = int(0.8*self.fps_counter_fontsize)
        if "e" in self.fps_counter_anchor:
            self.fps_counter_x = width
        elif "w" in self.fps_counter_anchor:
            self.fps_counter_x = 0
        if "n" in self.fps_counter_anchor:
            self.fps_counter_text_anchor = "nw"
            self.fps_counter_y = 0
            self.fpsExt_counter_y = self.fps_counter_y + self.fps_counter_fontsize
        elif "s" in self.fps_counter_anchor:
            self.fps_counter_text_anchor = "sw"
            self.fps_counter_y = height - self.fps_counter_fontsize/2
            self.fpsExt_counter_y = self.fps_counter_y - self.fpsExt_counter_fontsize - 4
    
    def drawPoint(self, point):
        self.canvas.create_line(point[0], fill=point[1]['col'])#, outline=point[1]['outline'])

    def drawLine(self, line):
        self.canvas.create_line(line[0], fill=line[1]['col'])#, outline=line[1]['outline'])
    
    def drawTriangle(self, triangle):
        self.canvas.create_polygon(triangle[0], fill=triangle[1]['col'], outline=triangle[1]['outline'])

    def drawAny(self, object):
        self.canvas.create_polygon(object[0], fill=object[1]['col'], outline=object[1]['outline'])

    def drawFPSCounter(self, fps, fpsExt):
        self.canvas.create_text(self.fps_counter_x, self.fps_counter_y,    anchor="e", text=fps   , font=('Noto Mono', self.fps_counter_fontsize))
        self.canvas.create_text(self.fps_counter_x, self.fpsExt_counter_y, anchor="e", text=fpsExt, font=('Noto Mono', self.fpsExt_counter_fontsize))

    def createArrow(self, points, color):
        a, b = points[0], points[1]
        return self.canvas.create_line(a[0], a[1], b[0], b[1], fill=color, arrow=tkinter.BOTH)

    def clear(self):
        self.canvas.delete('all')

    def delete(self, item):
        self.canvas.delete(item)

    def after(self, time, function):
        self.tk.after(1, function)

