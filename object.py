# ETGG 1803 Lab04b - Collision
# Joe McNally
# Section 02
# 03/14/17

from vector import *
import pygame

class QuickAndDirtyCollisionRect():
    def __init__(self, start_pos, width, height):
        self.mPos = start_pos
        self.mWidth = width
        self.mHeight = height

    def set_pos(self, pos):
        self.mPos = pos

    def collides(self, other_rect):
        if self.x < other_rect.x + other_rect.w and self.x + self.w > other_rect.x and self.y < other_rect.y + other_rect.h and self.y + self.h > other_rect.y:
            return True
        return False

    @property
    def x(self):
        return self.mPos.x

    @property
    def y(self):
        return self.mPos.y


    @property
    def w(self):
        return self.mWidth

    @property
    def h(self):
        """Gives the y value of the 2D Vector"""
        return self.mHeight

    @property
    def center(self):
        return self.mPos + Vector2(self.mWidth/2, self.mHeight/2)

def checkRectCollision(rect1, rect2):
    if rect1.x < rect2.x + rect2.w and rect1.x + rect1.w > rect2.x and rect1.y < rect2.y + rect2.h and rect1.y + rect1.h > rect2.y:
        return True
    return False

class Shape():
    def __init__(self, color_tuple, pos_vector):
        self.mColor = color_tuple
        self.mPos = pos_vector
        self.mRotation_Degrees = 360
        self.mYVector = polar_to_vector2_degrees(self.mRotation_Degrees, 1)
        self.mXVector = self.mYVector.perpendicular

    def pointInShape(self, pos_vector):
        """Checks if point is inside this shape"""
        pass

    def rotate(self, degrees):
        """Rotates the origin Vector of this shape"""
        self.mRotation_Degrees -= degrees
        if self.mRotation_Degrees < 0:
            self.mRotation_Degrees += 360

    def drawPygame(self, screen, is_selected, is_colliding):
        """Draws the shape to the screen"""
        self.mYVector = polar_to_vector2_degrees(self.mRotation_Degrees, 1)
        self.mXVector = self.mYVector.perpendicular
        pygame.draw.line(screen, (255,255,255), self.mPos.i, (self.mPos+(10 * self.mYVector)).i, 4)
        pygame.draw.line(screen, (255,255,255), self.mPos.i, (self.mPos+(10 * self.mXVector)).i, 4)

    def get_normals(self):
        """Returns vectors for the normals of this shape (not defined for Spheres)"""
        pass

class Cuboid(Shape):
    def __init__(self, color_tuple, pos_vector, width_height_tuple):
        super().__init__(color_tuple, pos_vector)
        self.mWidth, self.mHeight = width_height_tuple
        self.mSideOneVector = Vector2(-(self.mWidth/2), -(self.mHeight/2))
        self.mSideTwoVector = Vector2((self.mWidth/2), -(self.mHeight/2))
        self.mSideThreeVector = Vector2((self.mWidth/2), (self.mHeight/2))
        self.mSideFourVector = Vector2(-(self.mWidth/2), (self.mHeight/2))
        self.mPoints=[]
        self.mPoints.append(self.mPos + (self.mSideOneVector.x * self.mXVector) + (self.mSideOneVector.y * self.mYVector))
        self.mPoints.append(self.mPos + (self.mSideTwoVector.x * self.mXVector) + (self.mSideTwoVector.y * self.mYVector))
        self.mPoints.append(self.mPos + (self.mSideThreeVector.x * self.mXVector) + (self.mSideThreeVector.y * self.mYVector))
        self.mPoints.append(self.mPos + (self.mSideFourVector.x * self.mXVector) + (self.mSideFourVector.y * self.mYVector))

    def pointInShape(self, pos_vector):
        normals_list = self.get_normals()
        for normal in normals_list:
            point_projection = dot(pos_vector, normal)
            min, max = find_min_and_max_projection(self.mPoints, normal)
            if ((point_projection < min) or (point_projection > max)):
                return False
        return True

    def updatePos(self, pos_vector):
        self.mPos = pos_vector
        self.mPoints[0] = self.mPos + (self.mSideOneVector.x * self.mXVector) + (self.mSideOneVector.y * self.mYVector)
        self.mPoints[1] = self.mPos + (self.mSideTwoVector.x * self.mXVector) + (self.mSideTwoVector.y * self.mYVector)
        self.mPoints[2] = self.mPos + (self.mSideThreeVector.x * self.mXVector) + (self.mSideThreeVector.y * self.mYVector)
        self.mPoints[3] = self.mPos + (self.mSideFourVector.x * self.mXVector) + (self.mSideFourVector.y * self.mYVector)

    def drawPygame(self, screen, is_selected, is_colliding):
        if is_colliding:
            draw_color = (255,0,0)
        else:
            draw_color = self.mColor

        pygame.draw.polygon(screen, draw_color, (self.mPoints[0].i, self.mPoints[1].i, self.mPoints[2].i, self.mPoints[3].i) )
        if is_selected:
            pygame.draw.polygon(screen, (255,255,255),(self.mPoints[0].i, self.mPoints[1].i, self.mPoints[2].i, self.mPoints[3].i), 2)
        super().drawPygame(screen, is_selected, is_colliding)

    def get_normals(self):
        # just returns side vectors because they're the same as the normals of their perpindicular sides
        return [self.mPoints[1] - self.mPoints[0], self.mPoints[2] - self.mPoints[1]]

class Sphere(Shape):
    def __init__(self, color_tuple, pos_vector, radius):
        super().__init__(color_tuple, pos_vector)
        self.mRadius = radius
        self.mPoints = [self.mPos]
        print("Why?")

    def pointInShape(self, pos_vector):
        if (self.mPos - pos_vector).magnitude <= self.mRadius:
            return True
        else:
            return False

    def drawPygame(self, screen, is_selected, is_colliding):
        self.mPoints[0] = self.mPos
        if is_colliding:
            draw_color = (255,0,0)
        else:
            draw_color = self.mColor
        pygame.draw.circle(screen, draw_color, self.mPos.i, self.mRadius)
        if is_selected:
            pygame.draw.circle(screen, (255,255,255), self.mPos.i, self.mRadius, 2)

        super().drawPygame(screen, is_selected, is_colliding)

    def get_closest_point(self, point_list):
        """Returns the closest point (from a list of points) to the origin of the sphere"""
        closest_point = Vector2(-100000, -100000)
        for point in point_list:
            if ((self.mPos - point).magnitudeSq < (self.mPos - closest_point).magnitudeSq):
                closest_point = point
        return closest_point

class Triangle(Shape):
    def __init__(self, color_tuple, pos_vector, sides_vector_tuple):
        super().__init__(color_tuple, pos_vector)
        self.mSideOneVector = sides_vector_tuple[0] - self.mPos
        self.mSideTwoVector = sides_vector_tuple[1] - self.mPos
        self.mSideThreeVector = sides_vector_tuple[2] - self.mPos
        self.mPoints = []
        self.mPoints.append(self.mPos + (self.mSideOneVector.x * self.mXVector) + (self.mSideOneVector.y * self.mYVector))
        self.mPoints.append(self.mPos + (self.mSideTwoVector.x * self.mXVector) + (self.mSideTwoVector.y * self.mYVector))
        self.mPoints.append(self.mPos + (self.mSideThreeVector.x * self.mXVector) + (self.mSideThreeVector.y * self.mYVector))

    def pointInShape(self, pos_vector):
        # get area of the whole triangle
        thisArea = area_of_triangle(self.mPoints[0], self.mPoints[1], self.mPoints[2])
        # get area of the sub triangles created with the point being checked
        baryA = area_of_triangle(pos_vector, self.mPoints[1], self.mPoints[2]) / thisArea
        baryB = area_of_triangle(pos_vector, self.mPoints[2], self.mPoints[0]) / thisArea
        baryC = area_of_triangle(pos_vector, self.mPoints[0], self.mPoints[1]) / thisArea
        baryTotal = (baryA + baryB + baryC)

        # if the combined areas of the subtriangle are equal, the point is inside the triangle
        if ((baryTotal > 0.9999) and (baryTotal < 1.0001)):
            return True
        else:
            return False

    def drawPygame(self, screen, is_selected, is_colliding):
        self.mPoints[0] = self.mPos + (self.mSideOneVector.x * self.mXVector) + (self.mSideOneVector.y * self.mYVector)
        self.mPoints[1] = self.mPos + (self.mSideTwoVector.x * self.mXVector) + (self.mSideTwoVector.y * self.mYVector)
        self.mPoints[2] = self.mPos + (self.mSideThreeVector.x * self.mXVector) + (self.mSideThreeVector.y * self.mYVector)
        if is_colliding:
            draw_color = (255,0,0)
        else:
            draw_color = self.mColor
        pygame.draw.polygon(screen, draw_color, (self.mPoints[0].i, self.mPoints[1].i, self.mPoints[2].i) )

        if is_selected:
            pygame.draw.polygon(screen, (255,255,255), (self.mPoints[0].i, self.mPoints[1].i, self.mPoints[2].i), 2)

        super().drawPygame(screen, is_selected, is_colliding)

    def get_normals(self):
        # gets vectors for each side and returns a list of vectors perpendicular to those sides
        return [(self.mPoints[1] - self.mPoints[0]).perpendicular, (self.mPoints[2] - self.mPoints[1]).perpendicular, (self.mPoints[0] - self.mPoints[2]).perpendicular]

def collides(object1, object2):
    normals_to_check = []
    object1pointlist = object1.mPoints
    object2pointlist = object2.mPoints

    if isinstance(object1, Sphere):
        closest_point = object1.get_closest_point(object2pointlist)
        direction = closest_point - object1.mPos
        normals_to_check.append(direction)
        normals_to_check.append(direction.perpendicular)
        object1pointlist = []
        object1pointlist.append(object1.mPos - (direction.normalized * object1.mRadius))
        object1pointlist.append(object1.mPos + (direction.normalized * object1.mRadius))
        object1pointlist.append(object1.mPos - (direction.perpendicular.normalized * object1.mRadius))
        object1pointlist.append(object1.mPos + (direction.perpendicular.normalized * object1.mRadius))
    else:
        the_normals = object1.get_normals()
        for normal in the_normals:
            normals_to_check.append(normal)

    if isinstance(object2, Sphere):
        closest_point = object2.get_closest_point(object1pointlist)
        direction = closest_point - object2.mPos
        normals_to_check.append(direction)
        normals_to_check.append(direction.perpendicular)
        object2pointlist = []
        object2pointlist.append(object2.mPos - (direction.normalized * object2.mRadius))
        object2pointlist.append(object2.mPos + (direction.normalized * object2.mRadius))
        object2pointlist.append(object2.mPos - (direction.perpendicular.normalized * object2.mRadius))
        object2pointlist.append(object2.mPos + (direction.perpendicular.normalized * object2.mRadius))
    else:
        the_normals = object2.get_normals()
        for normal in the_normals:
            normals_to_check.append(normal)

    for normal in normals_to_check:
        obj1min, obj1max = find_min_and_max_projection(object1pointlist, normal)
        obj2min, obj2max = find_min_and_max_projection(object2pointlist, normal)
        if ((obj2max < obj1min) or (obj2min > obj1max)):
            return False
    return True

def area_of_triangle(point_one_vector, point_two_vector, point_three_vector):
    """returns area of a triangle given three vertices"""
    # Utilizes cross product with vectors on the XY plane and Z value of zero
    return (cross((point_three_vector - point_one_vector).vector3withZeroZ, (point_two_vector - point_one_vector).vector3withZeroZ).magnitude) / 2

def find_min_and_max_projection(point_vector_list, vector_to_project_on):
    """Returns tuple of minimum and maximum value of projection from a list of points"""
    max = None
    min = None
    for vector in point_vector_list:
        projected_value = dot(vector, vector_to_project_on)
        if ((max == None) and (min == None)):
            min = projected_value
            max = projected_value
        else:
            if (projected_value < min):
                min = projected_value
            elif (projected_value > max):
                max = projected_value
    return (min, max)