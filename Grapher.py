import cmath
import math
import random as rand
from PIL import Image
def comlexFunction(complexInput):
    return complexInput**2

def rephase(phase): # Remaps the phase of a number from (-pi,pi) to (0,2pi)
        return(phase if phase >= 0 else phase + 2*cmath.pi)

class graph:
    def __init__(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                 width = round(1920/4), height = round(1080/4),
                 equation = lambda z: (1j)**(z**2)):
        self.width = width
        self.height = height
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax}
        self.equation = equation
        self.image = Image.new(mode = "HSV", size = (self.width, self.height))
        self.data = []
    
    def complexToHSV(self, complex):
        phase = rephase(cmath.phase(complex))
        return((
            round(phase * 40.7436654315), #change angle from (0, 2pi) to (0,256)
            round(256 - 32 * (math.log(abs(complex),2) % 1)),
            round(256 - 64 * (math.log(abs(complex),2) % 1))
            ))

    def render(self, show = True):
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
        print(str(len(self.data)) + " points calculated")
        #textOutput = open(r"C:\Users\jeffr\Desktop\testOutput.txt","w")
        #textOutput.write(str(self.data))
        if show:
            self.image.show()


my_graph = graph(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, width = 960, height = 540)
my_graph.render(show = True)
