import cmath
import math
import random as rand
from PIL import Image

def rephase(phase): # Remaps the phase of a number from (-pi,pi) to (0,2pi)
        return(phase if phase >= 0 else phase + 2*cmath.pi)

def weightedAverage(num1, num2, weight): # weighted average of num1 and num2, weight is between 0 and 1
    return(num1 - weight * (num1 + num2))

class keyframe:
    # a keyframe holds data about view are and equation, and knows how to render itself.
    def __init__(self, parent, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                 equation = lambda z: (1j)**(z**2), numberOfFrames = 60):
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax} #view sqaure of the keyframe in unit space
        self.width = int(parent.width) # width in pixels of keyframe- CANNOT be interpolated
        self.height = int(parent.height) # height in pixels of keyframe- CANNOT be interpolated
        self.equation = equation # equation for the graph
        self.data = [] # data for the keyframe, that holds the complex outputs of each pixel
        self.image = Image.new("HSV", (self.width, self.height)) # the image that
        self.numberOfFrames = int(numberOfFrames)
    
    def complexToHSV(self, complex): #return (H,S,V) tuple from a complex input
        phase = rephase(cmath.phase(complex))
        try:
            return((
                round(phase * 40.7436654315), #change angle from (0, 2pi) to (0,256)
                round(256 - 32 * (math.log(abs(complex), 2) % 1)),
                round(256 - 64 * (math.log(abs(complex), 2) % 1))
                ))
        except ValueError:
            return((0, 224, 192))

    def calculateData(self): #calculate complex numbers for each point supplied
        for y in range(self.height):
            for x in range(self.width):
                self.data.append(
                    self.equation(complex(
                    x/self.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/self.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    )))
        
    def render(self, data, show = True):
        if data == []: #if data is not calculated yet, calculate, then run render again
            print("calculating data")
            self.calculateData()
            print("calculated data")
            self.render(data, show = show)
        else:
            print("mapping data")
            print("mapped data")
            self.image.putdata(list(map(self.complexToHSV, self.data))) #if data is calculated, map complexToHSV over the data and write data to image
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
        self.keyframes[keyframe].render(self.keyframes[keyframe].data, show = True)

    def renderAnimation(self):
        print("calculating keyframes")
        for keyframe in self.keyframes: # calculate data for all keyframes
            keyframe.calculateData()
        for keyframe in range(1, len(self.keyframes)-1):
            print("rendering frames")
            for frame in range(keyframe.numberOfFrames):
                keyframe.render(data = map(weightedAverage(self.keyframes[keyframe - 1], self.keyframes[keyframe], weight = frame / self.keyframes[keyframe])), show = True)
        
my_graph = graph(width = 480, height = 270)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: z)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: (1j)**(z**2), numberOfFrames = 10)
my_graph.renderAnimation()
#my_graph.preview(0)
#my_graph.preview(1)