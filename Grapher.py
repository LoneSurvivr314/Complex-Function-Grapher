import cmath
import random as rand
from PIL import Image
def comlexFunction(complexInput):
    return complexInput**2

class graph:
    def __init__(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                 width = round(1920/4), height = round(1080/4),
                 equation = lambda z: z):
        self.width = width
        self.height = height
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax}
        self.equation = equation
        self.image = Image.new(mode = "HSV", size = (self.width, self.height))
        self.data = []

    def complexToHSV(self, complex):
        angle = cmath.phase(complex)
        positiveAngle = angle if angle >= 0 else angle + 2*3.14159265358979 #change angle from (-pi, pi) to (0, 2pi)
        return((round(positiveAngle * 40.7436654315),256,256)) #change angle from (0, 2pi) to (0,256)

    def render(self):
        print("starting")
        self.data = []
        for y in range(self.height):
            for x in range(self.width):
                self.data.append(
                    self.complexToHSV(self.equation(complex(
                    x/self.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/self.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    ))))
        self.image.putdata(self.data)
        print(len(self.data) + "points calculated")
        #textOutput = open(r"C:\Users\jeffr\Desktop\testOutput.txt","w")
        #textOutput.write(str(self.data))
        self.image.show()


my_graph = graph()
my_graph.render()