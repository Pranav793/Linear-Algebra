from math import acos, sqrt, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


class Vector():
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(c) for c in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __getitem__(self, i):
        return self.coordinates[i]

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def magnitude(self):
        return Decimal(sqrt(sum([coord * coord
                                 for coord in self.coordinates])))

    def normalized(self):
        try:
            return self.times_scalar(Decimal('1.0') / self.magnitude())

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def subtract(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        return Vector([Decimal(c) * coord for coord in self.coordinates])

    def dot(self, v):
        multiplied_coords = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(multiplied_coords)

    def get_angle_rad(self, other):
        dot_prod = round(self.normalized().dot(other.normalized()), 3)
        return acos(dot_prod)

    def get_angle_deg(self, other):
        degrees_per_rad = 180. / pi
        return degrees_per_rad * self.get_angle_rad(other)

    # def angle_with(self, v, in_degrees=False):
    #     try: 
    #         u1 = self.normalized()
    #         u2 = v.normalized()
    #         angle_in_radians = acos(u1.dot(u2))

    #         if in_degrees:
    #             degrees_per_radian = 180. / pi
    #             return angle_in_radians * degrees_per_radian
    #         else:
    #             return angle_in_radians

    #     except Exception as e:
    #         if str(e) == "str.CANNOT_NORMALIZE ZERO_VECTOR_MSG":
    #             raise Exception('Cannot compute an angle with the zero vector')
    #         else:
    #             raise e

    def is_parallel(self, other):
        return (self.is_zero() or other.is_zero() or
                self.get_angle_rad(other) in [0, pi])

    def is_orthogonal(self, v):
        return round(self.dot(v), 3) == 0

    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])

    def component_parallel_to(self, b):
        dot = self.dot(b.normalized())
        return b.normalized().times_scalar(dot)

    def component_orthogonal_to(self, b):
        return self.subtract(self.project_on(b))

    def cross(self, v):
        x1, y1, z1 = self.coordinates
        x2, y2, z2 = v.coordinates

        line1 = (y1*z2) - (y2*z1)
        line2 = -((x1*z2) - (x2*z1))
        line3 = (x1*y2) - (x2*y1)
        return Vector([line1, line2, line3])

    def area_parallelogram(self, v):
        new_self = self.cross(v)
        return sqrt(sum([x ** 2 for x in new_self.coordinates]))

    def area_triangle(self, v):
        return 0.5 * self.area_parallelogram(v)

# # init ex:
# my_vector = Vector([1,2,3])

# # str ex:
# print(my_vector)

# # eq ex:
# my_vector2 = Vector([1,2,3])
# my_vector3 = Vector([-1,2,3])

# print my_vector == my_vector2 //true
# print my_vector == my_vector3 //false

  