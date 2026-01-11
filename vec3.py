import math
import random

class vec3:
    def __init__(self, e0=0, e1=0, e2=0):
        self.e= [e0, e1, e2]

    @property    #v.x instead of v.x()
    def x(self): return self.e[0]
    @property
    def y(self): return self.e[1]
    @property
    def z(self): return self.e[2]

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __add__(self, v):
        return vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return vec3(self.x * other, self.y * other, self.z * other)


    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        return self.__mul__(1 / other)
    
    def length(self):
        return math.sqrt(self.length_squared())
    
    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def __str__(self):       #for simplicity, maybe shpuld be a write color function??
        return f"{self.x}, {self.y}, {self.z}"

point3 = vec3    #position = point3(1, 0, 0) one unit to right
color = vec3     #pixel = color(1, 0, 0) red

def dot(u, v):
    return u.x * v.x + u.y * v.y + u.z * v.z

def cross(u, v):
    return vec3(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x
    )

def unit_vector(v):   #normalize
    len = v.length()
    if len == 0:
        return vec3(0.0, 0.0, 0.0)
    return v / len

def random_in_unit_sphere():
    while True:
        p = vec3(random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1))
        if p.length_squared() < 1:
            return p
        
def random_unit_vector():
    while True:
        # Pick a random point in a unit cube
        p = vec3(random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1))
        if p.length_squared() < 1:
            return unit_vector(p)
        
def reflect(v, n):
    return v - 2 * dot(v, n) * n
    