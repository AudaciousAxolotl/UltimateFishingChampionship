# ETGG 1803 Lab08 - Rasterizer & Matrix Transofrmations
# Joe McNally
# Section 02
# 04/29/18

from vector import *

class Matrix:
    """Implements a mathematical matrix tool, using vectors in a left-handed way to represent the data"""
    sStrPrecision = None
    def __init__(self, numRows, numCols, dataTuple=None):
        """creates an empty matrix of numRows * nowCols size, if dataTuple is defined and is the right length, adds that data into the matrix"""
        # check dataTuple is the correct length if it's defined
        self.mRows = numRows
        self.mCols = numCols
        if dataTuple != None:
            if len(dataTuple) != numCols * numRows:
                error_string = ""
                error_string += "You must pass exactly "
                error_string += str(numRows * numCols)
                error_string += " values in the data array to populate this "
                error_string += str(numRows)
                error_string += " x "
                error_string += str(numCols)
                error_string += " Matrix"
                raise ValueError(error_string)
            else:
                self.mData = split_tuple_into_vectors(dataTuple, numCols)
        else:
            self.mData = []
            for i in range (numRows):
                self.mData.append(zero_vector(numCols))

    def copy(self):
        """returns a deep copy of the matrix"""
        result = Matrix(self.mRows, self.mCols)
        for i in range(self.mRows):
            result.setRow(i, self.mData[i].copy())
        return result

    def __rmul__(self, other):
        """multiplies matrix on the right side of a vector or a scalar"""
        # handle vector and scalar
        # if vector, handle in left-handed fashion
        if isinstance(other, Vector):
            # we know this should be a left-handed vector multiplication
            # check len is = numRows
            if len(other) != self.mRows:
                error_string = "Vector" + str(len(other)) + " must be of length " + str(self.mRows) + " in order to multiply on the left of this Matrix."
                raise ValueError(error_string)
            else:
                new_vec_data = []
                for i in range(self.mCols):
                    new_vec_data.append(dot(self.getColumn(i), other))
                return Vector(*new_vec_data)
        # if scalar, multiply each element by the scalar
        elif isinstance(other, (float, int)):
            return self * other
        else:
            error_string = "You can only multiply this Matrix by either a scalar(of type int or float) or by a Vector. You attempted to multiply by '" + str(other) + "'"
            raise TypeError(error_string)
    def __mul__(self, other):
        """multiplies matrix on the left side of a vector, scalar, or another matrix"""
        # handle vector, matrix, and scalar
        if isinstance(other, Vector):
            # we know this should be a right-handed vector multiplication
            # check len is = numRows
            if len(other) != self.mCols:
                error_string = "Vector" + str(len(other)) + " must be of length " + str(self.mCols) + " in order to multiply on the right of this Matrix."
                raise ValueError(error_string)
            else:
                new_vec_data = []
                for row in self.mData:
                    new_vec_data.append(dot(row, other))
                return Vector(*new_vec_data)
        elif isinstance(other, Matrix):
        # for other matrix check mN umCols = other.mNumRows
            if self.mCols != other.mRows:
                error_string = "Matrix must have " + str(self.mCols) + "rows in order to multiply on the right of this Matrix."
                raise ValueError(error_string)
            else:
                # create matrix(numRows, other.numCols)
                result_matrix = Matrix(self.mRows, other.mCols)
                for i in range(other.mCols):
                    for j in range(self.mRows):
                        result_matrix[j, i]=dot(self.getRow(j), other.getColumn(i))
                return result_matrix
        # if scalar, multiply each element by the scalar
        elif isinstance(other, (float, int)):
            copyMatrix = self.copy()
            for i in range(copyMatrix.mRows):
                copyMatrix.setRow(i, self.mData[i] * float(other))
            return copyMatrix
        else:
            raise TypeError(
                "You can only multiply this Matrix by either a scalar(of type int or float) or by a Vector. You attempted to multiply by '" + str(
                    other) + "'")

    def __getitem__(self, rowColTuple):
        """Getter method for the matrix, pulls from mData

        @return scalar: float
        """
        return self.mData[rowColTuple[0]][rowColTuple[1]]

    def __setitem__(self, rowColTuple, value):
        """Setter method for the metrix, sets to mData"""
        self.mData[rowColTuple[0]][rowColTuple[1]] = value
    def __str__(self):
        """Outputs a string representing the matrix"""
        stringy = ""
        for row in range(self.mRows):
            # add start character
            if len(self.mData) == 1:
                stringy += "|"
            elif row == 0:
                stringy += "/"
            elif row == self.mRows - 1:
                stringy += "\\"
            else:
                stringy += "|"

            # print each item in the row
            for i in range(self.mCols):
                if Matrix.sStrPrecision != None:
                    stringy += str(round(self.mData[row][i], Matrix.sStrPrecision))
                else:
                    stringy += str(self.mData[row][i])
                if i != self.mCols - 1:
                    stringy += "     "


            # add end character
            if len(self.mData) == 1:
                stringy += "|"
            elif row == 0:
                stringy += "\\"
            elif row == self.mRows - 1:
                stringy += "/"
            else:
                stringy += "|"

            stringy += "\n"
        return stringy

    def transpose(self):
        """creates a transposed matrix"""
        new_matrix = Matrix(self.mCols, self.mRows)
        for i in range(self.mCols):
            new_matrix.setRow(i, self.getColumn(i))
        return new_matrix

    def getRow(self, rowNum):
        """returns a vector of the row at rowNum"""
        the_row = self.mData[rowNum].copy()
        return the_row

    def setRow(self, rowNum, rowVector):
        """sets the values at rowNum using the provided rowVector"""
        if not isinstance(rowVector, Vector):
            TypeError("Row can only be set using a vector as an argument")
        else:
            if len(rowVector) != self.mCols:
                error_string = "Invalid row argument (must be a Vector with size = " + str(self.mCols) + ")"
                raise ValueError(error_string)
            else:
                self.mData[rowNum] = rowVector.copy()

    def getColumn(self, colNum):
        """returns a vector of the column at colNum"""
        colData = []
        for i in range (self.mRows):
            colData.append(self.mData[i][colNum])
        return Vector(*colData)

    def setColumn(self, colNum, colVector):
        """sets the values at colNum using the provided colVector"""
        if not isinstance(colVector, Vector):
            TypeError("Column can only be set using a vector as an argument")
        else:
            if len(colVector) != self.mRows:
                error_string = "Invalid Column Vector.  Vector be of length " + str(self.mRows)
                raise ValueError()
            for i in range(self.mRows):
                self.mData[i][colNum] = colVector[i]

    def mulRowAdd(self, src_row, dest_row, scalar):
        """Adds the row at #src_row times the provided scalar to the row at #dest_row in this matrix"""
        self.mData[dest_row] += float(scalar) * self.mData[src_row]

    def swapRow(self, row1, row2):
        """Swaps row #row1 with row #row2 in this matrix"""
        temp_vector = self.getRow(row1)
        self.mData[row1] = self.getRow(row2)
        self.mData[row2] = temp_vector

    def mulRowByScalar(self, row_num, scalar):
        """Multiplies the row at #row_num by scalar"""
        self.setRow(row_num, scalar * self.getRow(row_num))

    def inverse(self):
        """If it exists, returns the inverse of the given matrix.  If it doesn't exist, returns None"""
        # check that this is a square matrix
        # if not - no inverse
        copyMatrix = self.copy()
        if copyMatrix.mCols != copyMatrix.mRows:
            return None
        # check if there is a zero column or row
        for i in range(copyMatrix.mRows):
            # if so - no inverse
            if copyMatrix.getRow(i).isZero:
                return None
            if copyMatrix.getColumn(i).isZero:
                return None

        # create identity matrix of size mNumRows
        result_matrix = identity(copyMatrix.mRows)

        step_count = 0

        # first for each row
        for i in range(copyMatrix.mRows):
            # if this_row[i] = 0
            if copyMatrix.mData[i][i] == 0:
                # check to see if following rows have row[i] !=0, if so, swap rows, if not, it's not invertible
                if i == copyMatrix.mRows:
                    return None
                swapped = False
                for j in range (i+1, copyMatrix.mRows):
                    if copyMatrix.mData[j][i] != 0:
                        copyMatrix.swapRow(i, j)
                        result_matrix.swapRow(i, j)
                        swapped = True
                        break
                if not swapped:
                    return None

            # now multiply this_row by 1/this_row[i]
            scalar = 1 / copyMatrix.mData[i][i]
            if scalar != 1:
                copyMatrix.mulRowByScalar(i, scalar)
                result_matrix.mulRowByScalar(i, scalar)

            # for each following row,
            for j in range (i+1, copyMatrix.mRows):
                # if that_row[i] != 0
                scalar = -(copyMatrix.mData[j][i])
                if scalar != 0:
                    # mulRowAdd -(that_row[i]) * this_row
                    copyMatrix.mulRowAdd(i, j, scalar)
                    result_matrix.mulRowAdd(i, j, scalar)

            step_count += 1
            # print("Step", step_count, "\n", copyMatrix)
            # print("Inverse Step", step_count, "\n", result_matrix)

        # once we've gone through each row, let's go in reverse!
        for i in range(copyMatrix.mRows - 1, 0, -1):
            for j in range(i-1, -1, -1):
                scalar = -copyMatrix.mData[j][i]
                if scalar != 0:
                    # mulRowAdd -(that_row[i]) * this_row
                    copyMatrix.mulRowAdd(i, j, scalar)
                    result_matrix.mulRowAdd(i, j, scalar)
            step_count += 1
            # print("Step", step_count, "\n", copyMatrix)
            # print("Inverse Step", step_count, "\n", result_matrix)
        return result_matrix

def identity(size):
    """returns an identity matrix of the size specified"""
    resultMatrix = Matrix(size, size)
    for i in range(size):
        resultMatrix.setRow(i, identity_vector(size, i))
    return resultMatrix

def split_tuple_into_vectors(tuple, vector_length):
    """"Splits a tuple into vectors of size vector_length"""
    if len(tuple) % vector_length != 0:
        raise ValueError("Tuple of length", len(tuple), "cannot be split into vectors of length", vector_length)
    else:
        resultVectorList = []
        count = 0
        while count < len(tuple):
            vecData = []
            for i in range(vector_length):
                vecData.append(tuple[count])
                count += 1
            thisVector = Vector(*vecData)
            resultVectorList.append(thisVector)
        return resultVectorList

def translate(tx, ty, tz, is_left = True):
    translation_matrix= Matrix(4, 4, (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, tx, ty, tz, 1))
    if is_left:
        return translation_matrix
    else:
        return translation_matrix.transpose()

def scale(sx, sy, sz):
    return Matrix(4,4, (sx,0,0,0, 0,sy,0,0, 0,0,sz,0, 0,0,0,1))

def rotateX(angle_degrees, is_left = True):
    angle_radians = math.radians(angle_degrees)
    ang_sin = math.sin(angle_radians)
    ang_cos = math.cos(angle_radians)
    rotx_matrix = Matrix(4,4, (1,0,0,0, 0,ang_cos,ang_sin,0, 0,-ang_sin,ang_cos,0, 0,0,0,1))
    if is_left:
        return rotx_matrix
    else:
        return rotx_matrix.transpose()

def rotateY(angle_degrees, is_left = True):
    angle_radians = math.radians(angle_degrees)
    ang_sin = math.sin(angle_radians)
    ang_cos = math.cos(angle_radians)
    roty_matrix = Matrix(4,4, (ang_cos,0,-ang_sin,0, 0,1,0,0, ang_sin,0,ang_cos,0, 0,0,0,1))
    if is_left:
        return roty_matrix
    else:
        return roty_matrix.transpose()

def rotateZ(angle_degrees, is_left = True):
    angle_radians = math.radians(angle_degrees)
    ang_sin = math.sin(angle_radians)
    ang_cos = math.cos(angle_radians)
    rotz_matrix = Matrix(4,4, (ang_cos,ang_sin,0,0, -ang_sin,ang_cos,0,0, 0,0,1,0, 0,0,0,1))
    if is_left:
        return rotz_matrix
    else:
        return rotz_matrix.transpose()

if __name__ == "__main__":
    """test code"""
    z = zero_vector(4)
    print(z)

    I = identity(3)
    print(I)                                                            # /1.0     0.0     0.0\
                                                                        # |0.0     1.0     0.0|
                                                                        # \0.0     0.0     1.0/

    print (translate(5, 8, 9))
    print (translate(5, 8, 9, False))