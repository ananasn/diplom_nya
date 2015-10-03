# -*- coding: utf-8 -*-
import struct
import readimage

class Triangle(object):
    """Generate triangular faces in binary form"""


    def __init__(self, vertex_1, vertex_2, vertex_3):
        self.normals = [0, 0, 0]
        self.v_1 = vertex_1
        self.v_2 = vertex_2
        self.v_3 = vertex_3

    def _count_norms(self, v1, v2, v3):
        """Сalculation of normal"""
        i = v1[1] * (v2[2] - v3[2]) + v2[1] * (v3[2] - v1[2]) + v3[1] * (v1[2] - v2[2])
        j = v1[2] * (v2[0] - v3[0]) + v2[2] * (v3[0] - v1[0]) + v3[2] * (v1[0] - v2[0])
        k = v1[0] * (v2[1] - v3[1]) + v2[0] * (v3[1] - v1[1]) + v3[0] * (v1[1] - v2[1])
        return [i, j, k]

    def get_arr(self):
        self.normals = self._count_norms(self.v_1, self.v_2, self.v_3)
        result = self.normals + self.v_1 + self.v_2 + self.v_3 + [0]
        result = struct.pack('12fH', *result)
        return result


def make_stl_model(name):
    norm = 4.0
    pix_w = 0.5
    pix_h = 0.5
    x = 0
    z = 0
    signal = 0
    new_pix_w = 0.5
    heightmap = []
    coord = []
    triangles = []

    heightmap, height, width = readimage.read_image(name,norm)
            
    for j in xrange(0, height):
        for i in xrange(0, width):
            if i == 0:
                saved = heightmap[width * j]
                saved_prev = heightmap[width * j - width]
                coord.append([[[x, saved_prev, z], [x, saved, z + pix_h], [x + pix_w / 2, saved, z + pix_h / 2]],
                 [[x, saved_prev, z], [x + pix_w / 2, saved, z + pix_h / 2], [x + pix_w, saved_prev, z]],
                 [[x + pix_w, saved_prev, z], [x + pix_w / 2, saved, z + pix_h / 2], [x + pix_w, saved, z + pix_h]],
                 [[x, saved, z + pix_h], [x + pix_w, saved, z + pix_h], [x + pix_w / 2, saved, z + pix_h / 2]]])
            else:
                if i != width - 1 and j != height - 1:
                    if heightmap[width * j + i] == heightmap[width * j + i + 1] == heightmap[width * j + i - 1] == heightmap[width * (j - 1) + i] == heightmap[width * (j - 1) + i + 1] == heightmap[width * (j - 1) + i - 1] == heightmap[width * (j + 1) + i] == heightmap[width * (j + 1) + i + 1] == heightmap[width * (j + 1) + i - 1]: #оптимизация для сокращение к-ва полигонов в модели
                        new_pix_w += pix_w
                        signal = 1
                        continue
                saved = heightmap[width * j + i - 1]
                saved_prev = heightmap[width * (j - 1) + i - 1]
                saved_above = heightmap[width * (j - 1) + i]
                saved_cur = heightmap[width * j + i]
                coord.append([[[x, saved_prev, z], [x, saved, z + pix_h], [x + new_pix_w / 2, saved_cur, z + pix_h / 2]],
                 [[x, saved_prev, z], [x + new_pix_w / 2, saved_cur, z + pix_h / 2], [x + new_pix_w, saved_above, z]],
                 [[x + new_pix_w, saved_above, z], [x + new_pix_w / 2, saved_cur, z + pix_h / 2], [x + new_pix_w, saved_cur, z + pix_h]],
                 [[x, saved, z + pix_h], [x + new_pix_w, saved_cur, z + pix_h], [x + new_pix_w / 2, saved_cur, z + pix_h / 2]]])
                saved = heightmap[width * j + i]
            x += new_pix_w
            if signal == 1:
                new_pix_w = 0.5

        x = 0
        z += pix_h

    header = struct.pack('80s', 'Binary STL Writer')        # header in binary form
    number_of_triangles = struct.pack('I', len(coord) * 4)  # amount of faces
    num = struct.pack('I', 1000)
    
    for face in coord:
        for vertex in face:
            tr = Triangle(*vertex)
            triangles.append(tr.get_arr())

    model_name = '.'.join([name.split('.')[0], 'stl'])
    model_name_with_path = './app/static/model/' + model_name
    with open(model_name_with_path, 'wb') as out:
        out.write(header)
        out.write(number_of_triangles)
        for i in triangles:
            out.write(i)

    return (heightmap, width, height, norm, model_name)