import math


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x + b.x, a. y + b.y)
        return Vector3(a. x +b, a. y + b)

    def __sub__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x -b.x ,a. y -b.y)
        return Vector3(a. x -b ,a. y -b)

    def __mul__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x *b.x ,a. y *b.y)
        return Vector3(a. x *b ,a. y *b)

    def __truediv__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x /b.x ,a. y /b.y)
        return Vector3(a. x /b ,a. y /b)

    def get_tuple(self):
        return (self.x ,self.y)

    def __repr__(self):
        return "Instance of Vector2. Address: " +hex(id(self))

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def __getitem__(self, index):
        if index == 0: return self.x
        elif index == 1: return self.y
        else: raise IndexError

    def dot(self ,b):
        return sum((self * b).get_tuple())

    def cross(self ,b):
        if type(b) == Vector2: return ((self.x*b.y)-(self.y*b.x))
        elif type(b) == list or type(b) == tuple:
            if len(b) == 2: return ((self.x*b[1])-(self.y*b[0]))

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = 0.0

    def __add__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x +b.x ,a. y +b.y ,a. z +b.z)
        return Vector3(a.x +b ,a.y +b ,a.z +b)

    def __sub__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x -b.x ,a. y -b.y ,a. z -b.z)
        return Vector3(a.x -b ,a.y -b ,a.z -b)

    def __mul__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x *b.x ,a. y *b.y ,a. z *b.z)
        elif type(b) == tuple:
            if len(b) == 3:
                return Vector3(a.x * b[0], a.y * b[1], a.z * b[2])
        return Vector3(a.x *b ,a.y *b ,a.z *b)

    def __truediv__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x /b.x ,a. y /b.y ,a. z /b.z)
        return Vector3(a. x /b ,a. y /b ,a. z /b)

    def get_tuple(self):
        return (self.x ,self.y ,self.z)

    def to_Vector2(self):
        return Vector2(self.x,self.y)

    def __repr__(self):
        return "Instance of Vector3. Address: " +hex(id(self))

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        if index == 0: return self.x
        elif index == 1: return self.y
        elif index == 2: return self.z
        else: raise IndexError

    def dot(self ,b):
        return sum(x*y for x, y in zip(self.get_tuple(), b.get_tuple()))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        l = self.length()
        return Vector3(self.x / l, self.y / l, self.z / l)

    def cross(self ,b):
        if type(b) == Vector3:
            return Vector3(((self.y * b.z) - (self.z * b.y)), -((self.x*b.z)-(self.z*b.x)), (self.x*b.y)-(self.y*b.x))
        elif type(b) == list or type(b) == tuple:
            if len(b) == 3:
                return Vector3(((self.y * b[2]) - (self.z * b[1])), -((self.x*b[2])-(self.z*b[0])), (self.x*b[1])-(self.y*b[0]))