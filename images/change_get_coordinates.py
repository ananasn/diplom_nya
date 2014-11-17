# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import json

img = Image.open("ti.jpg")
img = img.transpose(Image.FLIP_LEFT_RIGHT)
imgDraw = ImageDraw.Draw(img)

width = img.size[0]#size возвращает кортеж(ширина,высота).
height = img.size[1]
pixels = img.load()#Выгружаем значения пикселей.Возвращает объект, который по индексу [w,h] возвращает (R,G,B)
#Для получения этого преобразования необходимо «усреднить» каждый пиксель.

heightmap = []
coord = []#вершины
face = [] #треуголиные грани
norm = 2.0
pix_w = 0.5
pix_h = 0.5
x = 0
z = 0

for j in xrange(0,height):
    for i in xrange(0,width):
        res = (pixels[i, j][0]+pixels[i,j][1]+pixels[i,j][2])//3
        imgDraw.point((i, j), (res,res,res)) #градации серого
        h = round(res*(norm/255.0), 2)
        heightmap.append(str(round(res*(norm/255.0),2)))
        if j == 0 :
            coord.append((x, h, z))
            coord.append((x, h, z+pix_h))
            coord.append((x+pix_w/2, h, z+pix_h/2))
            x+=pix_w
            if (i == width-1) :
                coord.append((x, h, z))
                coord.append((x, h, z+pix_h))
        else:
            coord.append((x, h, z+pix_h))
            coord.append((x+pix_w/2, h, z+pix_h/2))
            x+=pix_w
            if (i == width-1) :
                coord.append((x, h, z+pix_h))
    x = 0
    z +=pix_h

#генерируем треугольные грани
step = 0
step2 = 0
temp = 0
for j in xrange(0,height):
    for i in xrange(0,width):
        if j == 0:
            face.append((0, 1+step, 0+step, 2+step))
            face.append((0, 0+step, 3+step, 2+step))
            face.append((0, 3+step, 4+step, 2+step))
            face.append((0, 4+step, 1+step, 2+step))
            step+=3
        elif j==1:
            face.append((0, 1+step, 0+step-(width*3), 2+step)) if i==0 else face.append((0, 1+step, 0+step+1-(width*3), 2+step))
            face.append((0, 0+step-(width*3), 3+step-(width*3), 2+step)) if i==0 else face.append((0, 0+step+1-(width*3), 3+step-(width*3), 2+step))
            face.append((0, 3+step-(width*3), 4+step-1, 2+step))
            face.append((0, 4+step-1, 1+step, 2+step))
            step+=2
        else:
            face.append((0, 1+step, 0+step-(width*2), 2+step))
            face.append((0, 0+step-(width*2), 3+step-(width*2)-1, 2+step))
            face.append((0, 3+step-(width*2)-1, 4+step-1, 2+step))
            face.append((0, 4+step-1, 1+step, 2+step))
            step+=2
    step+=1
    
coords_list = [round(j,2) for i in coord for j in i]
face_list = [j for i in face for j in i]



with open('../app/static/model/model.js', 'w') as outfile:
    json.dump(dict(zip(["vertices","faces"],[coords_list,face_list])+[("metadata",{"formatVersion" : 3})]), outfile)


img.save("grey_mirror_ti.png")
