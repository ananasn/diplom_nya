# -*- coding: utf-8 -*-
from change_get_coordinates import heightmap, width, height, norm
import copy

class Generator(object):
    def __init__(self,heightmap,h,w,thickness,offset,norm):
        self.norm = norm
        self.h = h
        self.w = w
        self.depth = self._depth(heightmap,h,w)
        workpiece_thickness = thickness
        self.offset = offset
        self.offset_counter = 0.0
        self.start_block = ['%','O01', 'G90', 'G21', 'G00X0Y0',\
        'G00Z'+str(workpiece_thickness), 'G00Z'+str(workpiece_thickness+2),'G91', 'F300.0S6000M03']
        #блок для нечетных строк
        self.body_block_unevenstr = [['G01X-',''],['G01Z-',''],['G01Z','']]
        #блок для четных строк
        self.body_block_evenstr = [['G01X',''],['G01Z-',''],['G01Z','']]
        self.end_block = ['G00X0Y0', 'M05', 'M02', '%']
    #генерируем список с G-кодами
    def generate(self):
        res = []
        for i in xrange(self.h):
            for j in xrange(self.w):
                if float(self.depth[i][j]) == 0.0:
                    self.offset_counter+= self.offset
                    continue
                if i%2 == 0:
                    res+=self._substitution(self.body_block_evenstr,i,j)
                else:
                    res+= self._substitution(self.body_block_unevenstr,i,j)
                self.offset_counter = self.offset
            res+=['G01Y'+str(self.offset)]
        for item in self.end_block: res.append(item)
        for item in self.start_block[::-1]: res.insert(0,item)
        return res
    #подставляем глубину в списки вида  ['G01Z','']
    def _substitution(self,block,i,j):
        block=copy.deepcopy(block)
        for item in block:
            if isinstance(item,list) and item[0].startswith('G01Z'):
                item[1] = str(float(self.depth[i][j])+2)
            else:
                item[1] = str(self.offset_counter)
        return block
    #запись в файл
    def write(self,gcode_list):
        with open('g_codes.txt','w') as f:
            for item in gcode_list:
                if len(item)==1:
                    f.write(item+'\n')
                else:
                    f.write(''.join(item)+'\n')
    def _depth(self,heightmap,h,w):
        with open('temp.txt','w') as f:
            f = heightmap
        depth = []
        for i in xrange(h): depth.append( [ str(self.norm-float(heightmap[i*w+j])) for j in xrange(w) ])
        return depth
        
g = Generator(heightmap,height,width,3.0, 0.5,norm)
gcode_list = g.generate()
g.write(gcode_list)