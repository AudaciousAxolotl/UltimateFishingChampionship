# ETGG 1803 Lab08 - Rasterizer & Matrix Transformations
# Joe McNally
# Section 02
# 04/29/18

import math     # Sin, Cos, Arctan all used for Vector2 calculations
import matrix

class Vector:
    """ This class represents a general-purpose vector class.  We'll
        add more to this in later labs.  For now, it represents a
        position and/or offset in n-dimensonal space. """
    def __init__(self, *args):
        """Initializes the vector, changing the class to Vector2 for a vector created with
        two scalars and changing it to Vector3 for a vector created with three scalars"""
        self.mData=[]
        if len(args) == 2:
            self.__class__ = Vector2
        elif len(args) == 3:
            self.__class__ = Vector3
        for scalar in args:
            self.mData.append(float(scalar))
        self.mDim = len(self.mData)

    def __str__(self):
        """Returns string representation of the vector"""
        stringified = "<Vector" + str(self.mDim) + ":"
        for scalar in self.mData:
            stringified += " "
            stringified += str(scalar)
            stringified += ","
        stringified = stringified[:-1] # chop off the final comma
        stringified += ">"
        return stringified

    def __len__(self):
        """Gives number of scalars in the vector"""
        return self.mDim

    def __getitem__(self, item_index):
        """Getter method for the vector, pulls from mData

        @return scalar: float
        """
        return self.mData[item_index]

    def __setitem__(self, key, value):
        """Setter method for the vector, sets to mData"""
        self.mData[key] = float(value)

    def copy(self):
        """Returns a new vector which is a copy of this vector"""
        return Vector(*self.mData)  # return self.__class__(*self.mData)

    def __eq__(self, other):
        """Tests for equality with other vectors"""
        # need to check for class type, see if it works even for Vector2 and Vector3
        if (isinstance(other, Vector) == True) and (len(other) == len(self)):
            for scalar_index in range(0, len(self)):
                if self[scalar_index] != other[scalar_index]:
                    return False
            return True
        else:
            return False

    def __add__(self, other):
        """Adds two vectors of the same dimension together"""
        if (isinstance(other, Vector) == True) and (len(other) == len(self)):
            addData = []
            for scalar_index in range(0, len(self)):
                addData.append(self[scalar_index] + other[scalar_index])
            return Vector(*addData)
        else:
            raise TypeError("TypeError: You can only add another Vector" + str(self.mDim) + " to this Vector" + str(self.mDim)+ " (you passed '" + str(other)+ "')")

    def __sub__(self, other):
        """Subtracts one vector from another"""
        if (isinstance(other, Vector) == True) and (len(other) == len(self)):
            return self + -other
        else:
            raise TypeError("TypeError: You can only subtract another Vector" + str(self.mDim) + " from this Vector" + str(self.mDim)+ " (you subtracted '" + str(other)+ "')")

    def __neg__(self):
        """Returns a new vector that is the negation of this vector"""
        negData = []
        for scalar in self.mData:
            negData.append(-scalar)
        return Vector(*negData)

    def __mul__(self, other):
        """Multiplies together a vector with a scalar"""
        if isinstance(other, (int, float)):
            mulData = []
            for scalar in self.mData:
                mulData.append(float(other) * scalar)
            return Vector(*mulData)
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Multiplies together a scalar with a vector"""
        return self * other

    def __truediv__(self, other):
        """Divides a vector by a scalar"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("You can't divide a vector by 0")
            else:
                return self * (1/float(other))
        else:
            raise TypeError("You can only divide this Vector" + str(self.mDim) + " by a scalar. You attempted to divide by '" + str(other) + "'")

    @property
    def magnitudeSq(self):
        """Gives the squared magnitude of the vector"""
        # add each scalar squared and then take the square root of the sum
        return dot(self, self)

    @property
    def magnitude(self):
        """Gives the magnitude of the vector"""
        return (dot(self, self))**(1/2)

    @property
    def normalized(self):
        """Returns a vector in the direction of this vector with the unit length of 1"""
        if self.isZero == False:
            return self / self.magnitude
        else:
            return self.copy()

    @property
    def isZero(self):
        """returns true if the vector is the zero vector"""
        for scalar in self.mData:
            if scalar != 0:
                return False
        return True

    @property
    def i(self):
        """returns a tuple of the integer values of the scalars in the vector"""
        int_scalars = []
        for scalar in self.mData:
            int_scalars.append(int(scalar))
        return tuple(int_scalars)

    @property
    def i2(self):
        """returns tuple of the integer value of the x and y coordinates of a vector of any size"""
        return (int(self.mData[0]), int(self.mData[1]))

    @property
    def v2(self):
        """returns a vector of the x and y values of a vector of any size"""
        return Vector2(self.mData[0], self.mData[1])

    @property
    def v3(self):
        """returns a vector of the x y and z values of a vector of any size"""
        return Vector3(self.mData[0], self.mData[1], self.mData[2])

class Vector2(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 2d applications and makes
        accessing the components (by name) a little easier as well as adding some polar conversion properties """
    def __init__(self, *args):
        """Initializes the Vector2, checking to make sure exactly two scalars were passed to it"""
        if len(args) != 2:
            raise ValueError("ERROR: Vector2 May Only Be Called With Two Scalar Arguments")
        else:
            super().__init__(*args)

    @property
    def x(self):
        """Gives the x value of the 2D Vector"""
        return self.mData[0]

    @x.setter
    def x(self, other):
        """Sets the x value of the 2D Vector"""
        self.mData[0] = float(other)

    @property
    def y(self):
        """Gives the y value of the 2D Vector"""
        return self.mData[1]

    @y.setter
    def y(self, other):
        """Sets the y value of the 2D Vector"""
        self.mData[1] = float(other)

    @property
    def degrees(self):
        """Returns the angle of the vector in polar space (in degrees)"""
        return math.atan2(self.y, self.x) * (180/math.pi)

    @property
    def degrees_inv(self):
        """Returns the angle of the vector in polar space (in degrees) with inverted Y"""
        return math.atan2(-self.y, self.x) * (180 / math.pi)

    @property
    def radians(self):
        """Returns the angle of the vector in polar space (in radians)"""
        return math.atan2(self.y, self.x)

    @property
    def radians_inv(self):
        """Returns the angle of the vector in polar space (in radians) with inverted Y"""
        return math.atan2(-self.y, self.x)

    @property
    def perpendicular(self):
        """Returns a Vector2 perpendicular to this Vector2"""
        return Vector2(-self.y, self.x)

    @property
    def vector_with_inv_y(self):
        """Returns this Vector2 with the y inverted (useful for pygame screen math)"""
        return Vector2(self.x, -self.y)

    @property
    def vector3withZeroZ(self):
        """Returns a Vector3 on the XY plane with Z Value of 0"""
        return Vector3(self.x, self.y, 0)

class Vector3(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 3d applications and makes
            accessing the components (by name) a little easier """
    def __init__(self, *args):
        """Initializes the Vector2, checking to make sure exactly three scalars were passed to it"""
        if len(args) != 3:
            raise ValueError("ERROR: Vector3 May Only Be Created With Three Scalar Arguments")
        else:
            super().__init__(*args)

    @property
    def x(self):
        """Gives the x value of the 3D Vector"""
        return self.mData[0]

    @x.setter
    def x(self, other):
        """Sets the x value of the 3D Vector"""
        self.mData[0] = float(other)

    @property
    def y(self):
        """Gives the y value of the 3D Vector"""
        return self.mData[1]

    @y.setter
    def y(self, other):
        """Sets the y value of the 3D Vector"""
        self.mData[1] = float(other)

    @property
    def z(self):
        """Gives the z value of the 3D Vector"""
        return self.mData[2]

    @z.setter
    def z(self, other):
        """Sets the z value of the 3D Vector"""
        self.mData[2] = float(other)

    @property
    def vector2NoZ(self):
        """Returns a Vector2 of this Vector3, with Z set to 0"""
        return Vector2(self.x, self.y)

    @property
    def i2(self):
        """Returns (x,y) tuple of Vector3, used for drawing on a pygame surface"""
        return (int(self.x), int(self.y))

    @property
    def colorTuple(self):
        """Returns the RGB color tuple of a Vector3 color with R G B values defined from 0.0-1.0 in the X Y Z positions"""
        red = int(min(self.x * 255, 255))
        green = int(min(self.y * 255, 255))
        blue = int(min(self.z * 255, 255))
        return (red, green, blue)

    @property
    def v4(self):
        """Returns vector 4 of vector 3 with 0 in w value"""
        return Vector(self.x, self.y, self.z, 0)

def polar_to_vector2(angle_radians, radius, invert_y=False):
    """Takes polar coordinates and returns the equivalent Vector2"""
    if invert_y == False:
        return Vector2(math.cos(angle_radians)*radius, math.sin(angle_radians)*radius)
    else:
        return Vector2(math.cos(angle_radians) * radius, -(math.sin(angle_radians) * radius))

def polar_to_vector2_degrees(angle_degrees, radius, invert_y=False):
    """Takes polar coordinatates (with angle in degrees) and returns the equivalent Vector2"""
    angle_radians = math.radians(angle_degrees)
    return polar_to_vector2(angle_radians, radius, invert_y)

def dot(vect1, vect2):
    """Performs dot product on 2 Vectors"""
    if((isinstance(vect1, Vector)) and (isinstance(vect2, Vector)) and (len(vect1) == len(vect2)) ):
        sum = 0
        for i in range (0, len(vect1)):
            sum += vect1[i] * vect2[i]
        return sum

def cross(vect1, vect2):
    """Performs cross product on two Vector3s"""
    # (vec1_y*vec2_z - vec1_z*vec2_y, vec1_z*vec2_x - vec1_x*vec2_z, vec1_x*vec2_y - vec1_y*vec2_x)
    if ((isinstance(vect1, Vector3)) and (isinstance(vect2, Vector3))):
        return Vector3(((vect1.y * vect2.z) - (vect1.z * vect2.y)),((vect1.z * vect2.x) - (vect1.x * vect2.z)),((vect1.x * vect2.y) - (vect1.y * vect2.x)))
    else:
        raise TypeError("Two Vector3s expected for cross product")

def center_point(vect1, vect2):
    """Gets the center point between two points"""
    vect_diff = vect2 - vect1
    return vect1 + (vect_diff / 2)

def zero_vector(size):
    """"returns a zero vector of length size"""
    vectorData = []
    vectorData += size * [0]
    return Vector(*vectorData)

def identity_vector(size, row_num):
    """returns the identity vector of the row at row_num in an identity matrix of size size"""
    identityVector = zero_vector(size)
    identityVector[row_num] = 1
    return identityVector

if __name__ == "__main__":
    # testing that copied vectors take the right class
    # and are not weakly copied
    v = Vector(5, -2, 1, 0.5)
    w = Vector(7, 3, 4.5, 2.1)
    z = Vector(5, 0, 3)
    q = Vector(0, 0, 0)
    print("v =", v)  # v = <Vector4: 5.0, -2.0, 1.0, 0.5>
    print("w =", w)  # w = <Vector4: 7.0, 3.0, 4.5, 2.1>
    print("z =", z)  # z = <Vector3: 5.0, 0.0, 3.0>
    print("q =", q)  # q = <Vector3: 0.0, 0.0, 0.0>
    print("v + w =", v + w)  # v + w = <Vector4: 12.0, 1.0, 5.5, 2.6>
    # print("v + 5 =", v + 5) # TypeError: You can only add another Vector4 to this
    # Vector4 (you passed '5')
    print("v =", v)  # v = <Vector4: 5.0, -2.0, 1.0, 0.5> (unchanged by addition
    # or similar methods)
    print("v - w =", v - w)  # v - w = <Vector4: -2.0, -5.0, -3.5, -1.6>
    # print("v - 5 =", v - 5) # TypeError: You can only subtract another Vector4 from
    # this Vector4 (you subtracted '5')
    print("-v =", -v)  # -v = <Vector4: -5.0, 2.0, -1.0, -0.5>
    print("2 * v =", 2 * v)  # 2 * v = <Vector4: 10.0, -4.0, 2.0, 1.0>
    print("v * 2 =", v * 2)  # v * 2 = <Vector4: 10.0, -4.0, 2.0, 1.0>
    print("v / 2 =", v / 2)  # v / 2 = <Vector4: 2.5, -1.0, 0.5, 0.25>
    print("v * 1.5 =", v * 1.5)  # v * 1.5 = <Vector4: 7.5, -3.0, 1.5, 0.75>
    # print("v * w =", v * w) # TypeError: You can only multiply this Vector4 and a scalar. You
    # attempted to multiply by '<Vector4: 7.0, 3.0, 4.5, 2.1>'
    # print("2 / v =", 2 / v) # TypeError: unsupported operand type(s) for /: 'int' and 'Vector'
    print("v.magnitude =", v.magnitude)  # v.magnitude = 5.5
    print("v.magnitudeSq =", v.magnitudeSq)  # v.magnitudeSquared = 30.25
    print("v.normalized =", v.normalized)  # v.normalized = <Vector4: 0.9090909090909091,
    # -0.36363636363636365, 0.18181818181818182, 0.09090909090909091>
    print("z.isZero =", z.isZero)  # z.isZero = False
    print("q.isZero =", q.isZero)  # q.isZero = True


    two = Vector(5.5, 3.3)
    print(two)
    two_copy = two.copy()
    two_copy.x = 9
    print(two)
    print(two_copy)
    three = Vector(6.681, 4.472, 2.263)
    print(three)
    three_copy = three.copy()
    three_copy.z = "88"
    print(three)
    print(three_copy)

    v = Vector(0, 0, 0, 0, 0)
    print(v)                                            # <Vector5: 0.0, 0.0, 0.0, 0.0, 0.0>
    w = Vector(1.2, "7", 5)
    # q = Vector(pygame.Surface((10,10)))               # Should raise an exception
    # q = Vector(1.2, "abc", 5)                         # Should raise an exception
    print(w)                                            # <Vector3: 1.2, 7.0, 5.0>
    z = w.copy()
    print(z[0])                                         # 1.2
    z[0] = 9.9
    z[-1] = "6"
    # z["abc"] = 9.9					                # Should raise an exception
    print(z)                                            # <Vector3: 9.9, 7.0, 6.0>
    print(w)                                            # <Vector3: 1.2, 7.0, 5.0>
    print(z == w)                                       # False    [same as print(z.__eq__(w))]
    print(z == Vector(9.9, "7", 6))                     # True
    print(z == 5)                                       # False
    print(z[0])                                         # 9.9
    print(len(v))                                       # 5
    print(w.i)        	  	                            # (1, 7, 5)
    w = Vector2(5, "3")
    k = Vector(-1.4, 2)		                            # Vector constructor should set this to Vector2
    print(w.x)                                          # 5.0
    print(w.y)                                          # 3.0
    w.x = 6
    w.y = 4
    print(w)                                            # <Vector2: 6.0, 4.0>
    print("Radians:", w.radians)                                    # 0.5880026035475675
    print("Radians Inv:", w.radians_inv)
    print("Degrees:", w.degrees)                                    # 33.690067525979785
    print("Degrees Inv:", w.degrees_inv)
    print(k.radians)		                            #
    print(w.i)
    print(isinstance(w.i, tuple))

    q = Vector3(9, 0, -2)
    q.z += 5
    print(q)                                            # <Vector3: 9.0, 0.0, 3.0>

    print("Polar to Vector2:", polar_to_vector2(1.459, 10.0))                # <Vector2: 1.1156359273295111, 9.937572967161127>
    print("Polar to Vector2 (Inv Y):", polar_to_vector2(1.459, 10.0, True))

    v = Vector3(1, 3, -2)
    w = Vector3(0, 4, 5)
    print("V =", v)
    print ("W =", w)
    print("V x W =", cross(v, w))
    print("W x V =", cross(w, v))

    v = Vector3(1,2,3)
    w = Vector3(4,-5,6)
    print("V =", v)
    print ("W =", w)
    print("V dot W =", dot(v, w))
    print("W dot V =", dot(w, v))

    v = Vector2(-4, -9)
    w = Vector2(-1, 2)
    print("V =", v)
    print ("W =", w)
    print("V dot W =", dot(v, w))
    print("W dot V =", dot(w, v))

    # Wikipedia Example
    v = Vector3(1,3,-5)
    w = Vector3(4,-2,-1)
    print("V =", v)
    print ("W =", w)
    print("V dot W =", dot(v, w))
    print("W dot V =", dot(w, v))