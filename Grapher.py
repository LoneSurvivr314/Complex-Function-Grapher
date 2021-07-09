import cmath
import math
import random as rand
from PIL import Image
from itertools import repeat

def rephase(phase): # Remaps the phase of a number from (-pi,pi) to (0,2pi)
        return(phase if phase >= 0 else phase + 2*cmath.pi)

def weightedAverage(num1, num2, weight): # weighted average of num1 and num2, weight is between 0 and 1
    #print(num1, num2, weight)
    #print("----")
    return(num1 - weight * (num1 - num2))

def complexToHSV(complex): #return (H,S,V) tuple from a complex input
    phase = rephase(cmath.phase(complex))
    try:
        return((
            round(phase * 40.7436654315), #change angle from (0, 2pi) to (0,256)
            round(256 - 32 * (math.log(abs(complex), 2) % 1)),
            round(256 - 64 * (math.log(abs(complex), 2) % 1))
            ))
    except ValueError:
        return((0, 224, 192))

def render(data, width, height, show = True,
           path = ""): # render data by mapping complexToHSV over it
    print("mapping data")
    print("mapped data")
    image = Image.new("HSV", (width, height))
    image.putdata(list(map(complexToHSV, data)))
    if show:
        image.show()
    if path:
        image.convert("RGB").save(path)

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
    

    def calculateData(self): #calculate complex numbers for each point supplied
        for y in range(self.height):
            for x in range(self.width):
                try:
                    self.data.append(
                    self.equation(complex(
                    x/self.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/self.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    )))
                except (ValueError, ZeroDivisionError):
                    self.data.append(cmath.nan + cmath.nanj)
        print("calculated!")
        
class graph:
    # a graph holds a collection ofn keyframes, and controls them.
    def __init__(self, width = 480, height = 270):
        self.keyframes = []
        self.width = width
        self.height = height

    def addKeyframe(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = 9/16,
                    equation = lambda z: (1j)**(z**2), numberOfFrames = 60):
        self.keyframes.append(keyframe(self, xmin, xmax, ymin, ymax, equation, numberOfFrames))

    def preview(self, keyframe = 0):
        render(data = self.keyframes[keyframe].data, width = self.width, height = self.height, show = True, path = False)
    
    def calculateKeyframe(self, keyframeNumber = 0):
        print("calculating data")
        self.keyframes[keyframeNumber].calculateData()

    def renderAnimation(self):
        print("calculating keyframes")
        name = 0
        for keyframe in self.keyframes: # calculate data for all keyframes
            keyframe.calculateData()
        for keyframeNum in range(1, len(self.keyframes)):
            numberOfFrames = self.keyframes[keyframeNum].numberOfFrames
            firstData = self.keyframes[keyframeNum - 1].data
            secondData = self.keyframes[keyframeNum].data
            for frame in range(0, numberOfFrames): #render each frame by interpolating between keyframes
                render(
                       data = map(weightedAverage, firstData, secondData, repeat(frame / numberOfFrames)),
                       width=self.width, height=self.height, show=False,
                       path = "C:\\Users\\jeffr\\Desktop\\Complex Grapher Output\\" + str(name).rjust(4, "0") + ".png")
                name += 1
                print("C:\\Users\\jeffr\\Desktop\\Complex Grapher Output\\" + str(name).rjust(4, "0") + ".png")
        
        render(data = self.keyframes[len(self.keyframes)-1].data, width=self.width, height=self.height, show=False,
               path = "C:\\Users\\jeffr\\Desktop\\Complex Grapher Output\\" + str(name).rjust(4, "0") + ".png") #render last frame
my_graph = graph(width = 1920, height = 1080)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: z,  numberOfFrames = 10)
#my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: (1j)**(z**2), numberOfFrames = 60)
my_graph.addKeyframe(xmin = -2, xmax = 2, ymin = -9/8, ymax = 9/8, equation = lambda z: (z**(1j) + z**2) / (z**2 + 1j), numberOfFrames = 60)
my_graph.renderAnimation()
#my_graph.calculateKeyframe(1)
#my_graph.preview(1)
