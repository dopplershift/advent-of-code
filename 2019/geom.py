from dataclasses import dataclass


#@dataclass
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def up(self):
        return Point(self.x, self.y + 1)
    
    @property
    def down(self):
        return Point(self.x, self.y - 1)
    
    @property
    def right(self):
        return Point(self.x + 1, self.y)

    @property
    def left(self):
        return Point(self.x - 1, self.y)
    
    @property
    def neighbors(self):
        yield self.up
        yield self.right
        yield self.down
        yield self.left
        #return iter((self.up, self.right, self.down, self.left))

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

@dataclass
class Vector:
    x: int
    y: int
    z: int

    @staticmethod
    def i():
        return Vector(1, 0, 0)
    
    @staticmethod
    def j():
        return Vector(0, 1, 0)

    @staticmethod
    def k():
        return Vector(0, 0, 1)

    
    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y + self.z + other.z
    
    def dot(self, other):
        return self @ other
    
    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)