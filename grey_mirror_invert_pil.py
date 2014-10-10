# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

img = Image.open("./images/ti.jpg")
img = img.transpose(Image.FLIP_LEFT_RIGHT)
imgDraw = ImageDraw.Draw(img)

width = img.size[0]#size возвращает кортеж(ширина,высота).
height = img.size[1]
pixels = img.load()#Выгружаем значения пикселей.Возвращает объект, который по индексу [w,h] возвращает (R,G,B)
#Для получения этого преобразования необходимо «усреднить» каждый пиксель.

for i in xrange(0,width):
  for j in xrange(0,height):
     res = (pixels[i, j][0]+pixels[i,j][1]+pixels[i,j][2])//3
     imgDraw.point((i, j), (255-res, 255-res, 255-res)) #градации серого и инвертирование

img.save("./images/grey_mirror_invert_ti.jpg")
      
