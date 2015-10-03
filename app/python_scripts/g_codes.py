# -*- coding: utf-8 -*-
import copy
import readimage

class Generator(object):
    
    
    def __init__(self, offset, norm,
                 name, name_image):
        self.name = name
        self.norm = norm
        heightmap, self.h, self. w = readimage.read_image(name_image, norm)
        self.depth = self._depth(heightmap, self.h, self.w)
        self.offset = offset
        self.offset_counter = 0.0
        self.start_block = [
            '%','O01', 'G90', 'G21', 'G00X0Y0',
            'G00Z' + str(0), 
            'G00Z' + str(2),
            'G91', 'M03', 'F300.0S6000'
            ]
        self.body_block_unevenstr = [['G01X-', ''], ['G01Z-', ''], ['G01Z', '']]
        self.body_block_evenstr = [['G01X', ''], ['G01Z-', ''], ['G01Z', '']]
        self.end_block = ['G00X0Y0', 'M05', 'M02', '%']
      
    def generate(self):
        """Generate G-codes list"""
        res = []
        for i in xrange(self.h):
            for j in xrange(self.w):
                if (i%2 == 0) and\
                    (round(float(self.depth[i][j]), 2) <= 0.03):
                    self.offset_counter += self.offset
                    if j == self.w-1:
                        res += ['G01X' + str(self.offset_counter)]
                    continue
                if (i%2 == 1) and\
                     (round(float(self.depth[i][self.w-j-1]), 2) <= 0.03):
                    self.offset_counter += self.offset
                    if j == self.w-1:
                        res += ['G01X-' + str(self.offset_counter)]
                    continue
                if i%2 == 0:
                    res += self._substitution(
                        self.body_block_evenstr,i, j)
                if i%2 == 1:
                    res += self._substitution(
                        self.body_block_unevenstr, i, self.w-j-1)
                self.offset_counter = self.offset
            self.offset_counter = self.offset
            res += ['G01Y-' + str(self.offset)]
        for item in self.end_block: res.append(item)
        for item in self.start_block[::-1]: res.insert(0,item)
        return res
        
    def _substitution(self, block, i, j):
        """depth sybstitution in  g-code blocks"""
        block = copy.deepcopy(block)
        for item in block:
            if (isinstance(item,list) and 
                    item[0].startswith('G01Z')):
                item[1] = str(float(self.depth[i][j]) + 2)
            else:
                item[1] = str(self.offset_counter)
        return block
        
    def write(self, gcode_list):
        """Writes G-codes in fie g_codes.txt"""
        with open(self.name, 'w') as f:
            for item in gcode_list:
                if len(item) == 1:
                    f.write(item + '\n')
                else:
                    f.write(''.join(item) + '\n')
                    
    def _depth(self, heightmap, h, w):
        temp_depth = []
        for i in xrange(h): 
            temp_depth.append([str(self.norm - float(heightmap[i*w + j])) \
                for j in xrange(w)])
        print(len(temp_depth))
        return temp_depth