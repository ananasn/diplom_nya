# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

img = Image.open("./images/ti.png")
brush = ImageDraw.Draw(img)
width = img.size[0]
height = img.size[1]
pixels = img.load()
for i in range(0,width//2):
    for j in range(0,height):
        temp = pixels[i,j]
        brush.point((i,j),(pixels[width-i-1,j][0], pixels[width-1-i,j][1], pixels[width-1-i,j][2]))
        brush.point((width-i,j),(temp[0],temp[1],temp[2]))

img.save("./images/ti_mirror.png")