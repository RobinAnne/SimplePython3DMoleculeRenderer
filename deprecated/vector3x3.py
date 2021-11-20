class Vector3x3:
    def __init__(self, vertices):
        #store point indexes
        (a, b, c, color, outline) = vertices
        self.a = a 
        self.b = b
        self.c = c
        self.color = color
        self.outline = outline
