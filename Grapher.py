import cmath
import math
import random as rand
from PIL import Image

def rephase(phase): # Remaps the phase of a number from (-pi,pi) to (0,2pi)
        return(phase if phase >= 0 else phase + 2*cmath.pi)

class keyframe:
    # a keyframe holds data about view are and equation, and knows how to render itself.
    def __init__(self, parent, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                 equation = lambda z: (1j)**(z**2)):
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax}
        self.equation = equation
        self.data = []
        self.image = Image.new("HSV", (parent.width, parent.height))
        self.data = []
    
    def complexToHSV(self, complex): #return (H,S,V) tuple from a complex input
        phase = rephase(cmath.phase(complex))
        return((
            round(phase * 40.7436654315), #change angle from (0, 2pi) to (0,256)
            round(256 - 32 * (math.log(abs(complex),2) % 1)),
            round(256 - 64 * (math.log(abs(complex),2) % 1))
            ))

    def calculateData(self, parent): #calculate complex numbers for each point supplied
        for y in range(parent.height):
            for x in range(parent.width):
                self.data.append(
                    self.equation(complex(
                    x/parent.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/parent.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    )))
        
    def render(self, parent, show = True):
        if self.data == []: #if data is not calculated yet, calculate, then run render again
            print("calculating data")
            self.calculateData(parent)
            print("calculated data")
            self.render(parent, show = show)
        else:
            print("mapping data")
            self.data = list(map(self.complexToHSV, self.data)) #if data is calculated, map complexToHSV over the data
            print("mapped data")
        print()
        self.image.putdata(self.data) #write data to image
        if show:
            self.image.show()


class graph:
    # a graph holds a collection ofn keyframes, and controls them.
    def __init__(self, width = 480, height = 270):
        self.keyframes = []
        self.width = width
        self.height = height

    def addKeyframe(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                    equation = lambda z: (1j)**(z**2)):
        self.keyframes.append(keyframe(self, xmin, xmax, ymin, ymax, equation))

    def preview(self, keyframe = 0):
        self.keyframes[0].render(self, show = True)

my_graph = graph(width = 480, height = 270)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: (1j)**(z**2))
my_graph.preview(keyframe= 0)