# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

img = Image.open("./images/aldnoah.jpg")
imgDraw = ImageDraw.Draw(img)
width = img.size[0]#size возвращает кортеж(ширина,высота).
height = img.size[1]
pixels = img.load()#Выгружаем значения пикселей.Возвращает объект, который по индексу [w,h] возвращает (R,G,B)

#Для получения этого преобразования необходимо «усреднить» каждый пиксель.
for i in range(0,width):
  for j in range(0,height):
     r = pixels[i, j][0]
     g = pixels[i,j][1]
     b = pixels[i,j][2]
     res = (r+g+b)//3
     imgDraw.point((i, j), (res, res, res))

img.save("./images/grey_aldnoah.jpg")
      
