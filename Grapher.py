import cmath
import random as rand

def comlexFunction(complexInput):
    return complexInput**2

print("initializing...")
imageData = []
for pixel in range(1920*1080):
    imageData.append(complex(rand.random(), rand.random()))
print("image list created...")
for pixel in range(0,len(imageData)):
    imageData[pixel] = (pixel % 1920 - 1080 / 2) // 2
print("actually done now!")