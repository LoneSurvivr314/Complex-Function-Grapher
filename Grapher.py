import cmath
import math
import random as rand
from PIL import Image
def comlexFunction(complexInput):
    return complexInput**2

def rephase(phase): # Remaps the phase of a number from (-pi,pi) to (0,2pi)
        return(phase if phase >= 0 else phase + 2*cmath.pi)

class keyframe:
    def __init__(self, parent, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                 equation = lambda z: (1j)**(z**2)):
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax}
        self.equation = equation
        self.data = []
        self.image = Image.new("HSV", (parent.width, parent.height))
    
    def complexToHSV(self, complex):
        phase = rephase(cmath.phase(complex))
        return((
            round(phase * 40.7436654315), #change angle from (0, 2pi) to (0,256)
            round(256 - 32 * (math.log(abs(complex),2) % 1)),
            round(256 - 64 * (math.log(abs(complex),2) % 1))
            ))

    def render(self, parent, show = True):
        print("starting")
        self.data = []
        for y in range(parent.height):
            for x in range(parent.width):
                self.data.append(
                    self.complexToHSV(self.equation(complex(
                    x/parent.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/parent.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    ))))
        self.image.putdata(self.data)
        print(str(len(self.data)) + " points calculated")
        
        if show:
            self.image.show()


class graph:
    def __init__(self, width = 480, height = 270):
        self.keyframes = []
        self.width = width
        self.height = height

    def addKeyframe(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                    equation = lambda z: (1j)**(z**2)):
        self.keyframes.append(keyframe(self, xmin, xmax, ymin, ymax, equation))

    def preview(self, keyframe = 0):
        self.keyframes[0].render(self, show = True)

my_graph = graph(width = 960, height = 540)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: (1j)**(z**2))
my_graph.preview(keyframe= 0)