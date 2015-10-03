# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

def read_image(name, norm):
    img = Image.open('./app/static/images/' + name)
    width = img.size[0]
    height = img.size[1]
    pixels = img.load()
    heightmap = []

    for j in xrange(0, height):
        for i in xrange(0, width):
            if isinstance(pixels[i,j],int): # sometimes pixel is int, not tuple
                res = pixels[i,j]
            else:
                res = (pixels[i,j][0] + pixels[i,j][1] + pixels[i,j][2]) // 3
            h = round(res * (norm/256.0), 2)
            heightmap.append(h)
    return (heightmap, height, width)