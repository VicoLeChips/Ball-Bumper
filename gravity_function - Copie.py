import math #to use angle functions
import time #to reboot time each impact

#pivot is an object  which represents the next pivot.
#arrlstpos is an array of integers with coordinates (only y axis because x doesn't change) of the ball at 5 last positions.
#impact is a boolean, it indicates if there is an impact with a pivot.
#angle is a float, it is the last angle of the ball in its trajectory.
#v0 is a float, it is the initial speed.
#xSsize and ySsizeare integers, they define the size of the screen.
#ball is the parameter of the ball which is an object.
def position(pivot, arrlstpos, impact, angle, v0, xSsize, ySsize):
    x = xSsize/10
    g = 9.81
    alpha = angleImpact(arrnpvt, arrlstpos, impact, angle)
    vx = math.cos(alpha) * v0
    y = (- x**2 / (((math.cos(alpha))**2) * 2 * v0)+ x * math.tan(alpha))* ySsize
    return (x,y,vx)


"""to compute the new angle when the ball bump,
   we need firstly to compute the tangent of the curve when the ball tuch the pivot,
   so we need the equation y = f'(a) (x-a) + f(a).
   Then we compute its angle wrt the window reference
"""
def angleImpact(pivot, arrlstpos, impact, angle):
    if (impact == True):
        alphatan = angleTangeante(xImpact, yImpact, v0, x, alpha)
        alphapiv = anglePivot()
        alpha = 2 * alphapiv + math.pi - alphatan
    else:
        alpha = angle
    return alpha


def impact(pivot, xSsize, ySsize, ball):
    

    return impact

def angleTangeante(xImpact, yImpact, v0, x, alpha):
    adjacent = 1
    opposate = (-yImpact) + (-(2*(x-1)*(v0*(math.cos(alpha))**2)-(v0-2*math.sin(alpha)*math.cos(alpha))*(x-1)**2) / (v0*(math.cos(alpha))**2)**2) + (math.tan(alpha) + x*(1+(math.tan(alpha))**2))  *  ((- (x-1)**2 / (((math.cos(alpha))**2) * 2 * v0)+ (x-1) * math.tan(alpha))* ySsize)
    #f'(a)(x-a)+f(a)
    alphatan = math.atan(opposate/adjacent)
    return alphatan

def anglePivot
def coordinateImpact(x, y, impact):
    if impacte == True :
        xImpact = x
        yImpact = y
        return xImpact, yImpact