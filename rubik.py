__author__ = 'shish'

import numpy


class Cube:

    def __init__(self):
        self.__edges = numpy.array(['color'] * 3 * 3 * 6)
        self.__edges.shape = (6, 3, 3)
        self.__edges[0, :, :] = 'red'
        self.__edges[1, :, :] = 'yello'
        self.__edges[2, :, :] = 'green'
        self.__edges[3, :, :] = 'white'
        self.__edges[4, :, :] = 'blue'
        self.__edges[5, :, :] = 'black'

    def print(self):
        padding = 6
        for row_num in range(3):
            print(' ' * ((padding + 1) * 3 + 1) + ' '.join(s.rjust(padding) for s in list(self.__edges[0, row_num])))
        for row_num in range(3):
            print('  '.join(' '.join(s.rjust(padding) for s in list(self.__edges[edge_num, row_num])) for edge_num in range(1, 5)))
        for row_num in range(3):
            print(' ' * ((padding + 1) * 3 + 1) + ' '.join(s.rjust(padding) for s in list(self.__edges[5, row_num])))

    def rotate_cube(self, axis):
        assert (axis in ['x', 'y', 'z'])
        if axis in ['y', 'z']:
            new_edges = numpy.array(['color'] * 3 * 3 * 6)
            new_edges.shape = (6, 3, 3)
            if axis == 'z':
                new_edges[1] = self.__edges[4]
                new_edges[2] = self.__edges[1]
                new_edges[3] = self.__edges[2]
                new_edges[4] = self.__edges[3]
                new_edges[0] = numpy.rot90(self.__edges[0], 1)
                new_edges[5] = numpy.rot90(self.__edges[5], 3)
            if axis == 'y':
                new_edges[0] = numpy.rot90(self.__edges[1], 3)
                new_edges[1] = numpy.rot90(self.__edges[5], 3)
                new_edges[2] = numpy.rot90(self.__edges[2], 3)
                new_edges[3] = numpy.rot90(self.__edges[0], 3)
                new_edges[4] = numpy.rot90(self.__edges[4], 1)
                new_edges[5] = numpy.rot90(self.__edges[3], 3)
            self.__edges = new_edges

        if axis == 'x':
            self.rotate_cube('y')
            self.rotate_cube('z')
            self.rotate_cube('z')
            self.rotate_cube('z')
            self.rotate_cube('y')
            self.rotate_cube('y')
            self.rotate_cube('y')

    def __swap(self, edge1, edge2, row_num):
        self.__edges[[edge2, edge1], row_num, :] = self.__edges[[edge1, edge2], row_num, :]

    def __rotate_row_z(self, row_num):
        if row_num == 0:
            self.__edges[5] = numpy.rot90(self.__edges[5], 3)
        if row_num == 2:
            self.__edges[0] = numpy.rot90(self.__edges[0], 1)
        self.__swap(1, 4, row_num)
        self.__swap(2, 4, row_num)
        self.__swap(3, 4, row_num)

    def rotate_row(self, axis, row_num):
        if axis == 'z':
            self.__rotate_row_z(row_num)
        if axis == 'x':
            self.rotate_cube('y')
            self.rotate_cube('y')
            self.rotate_cube('y')
            self.__rotate_row_z(row_num)
            self.rotate_cube('y')
        if axis == 'y':
            self.rotate_cube('x')
            self.__rotate_row_z(row_num)
            self.rotate_cube('x')
            self.rotate_cube('x')
            self.rotate_cube('x')


def main():
    cube = Cube()
    cube.print()
    cube.rotate_row('z', 1)
    cube.print()
    cube.rotate_cube('y')
    cube.print()
    cube.rotate_row('x', 1)
    cube.print()


main()