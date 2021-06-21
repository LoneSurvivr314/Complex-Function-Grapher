import cmath
def complexToHSV(complex):
    angle = cmath.phase(complex)
    positiveAngle = angle if angle >= 0 else angle + 2*3.14159265358979 #change angle from (-pi, pi) to (0, 2pi)
    return((round(positiveAngle * 40.7436654315),256,256)) #change angle from (0, 2pi) to (0,256)

print(complexToHSV(-1+0j))