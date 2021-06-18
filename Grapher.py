import cmath
import random as rand
from PIL import Image
def comlexFunction(complexInput):
    return complexInput**2

class graph:
    def __init__(self, xmin = -1, xmax = 1, ymin = -9/16, ymax = -9/16,
                 width = 1920, height = 1080,
                 equation = lambda z: z):
        self.width = width
        self.height = height
        self.view = {"xmin":xmin,"xmax":xmax,"ymin":ymin,"ymax":ymax}
        self.equation = equation
        self.image = Image.new(mode = "RGB", size = (self.width, self.height))
        self.data = []
    
    def render(self):
        print("starting")
        self.data = []
        for y in range(self.height):
            for x in range(self.height):
                self.data.append(self.equation(complex(
                    x/self.width*(self.view["xmax"]-self.view["xmin"])+self.view["xmin"],
                    y/self.height*(self.view["ymax"]-self.view["ymin"])+self.view["ymin"]
                    )))

my_graph = graph()
my_graph.render()