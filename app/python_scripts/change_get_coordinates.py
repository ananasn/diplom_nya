# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import json

def make_json_model(name):
    img = Image.open(name)
    imgDraw = ImageDraw.Draw(img)
    
    width = img.size[0]#size возвращает кортеж(ширина,высота).
    height = img.size[1]
    pixels = img.load()#Выгружаем значения пикселей.Возвращает объект, который по индексу [w,h] возвращает (R,G,B)
    #Для получения преобразования необходимо «усреднить» каждый пиксель.
    
    heightmap = []
    coord = []#вершины
    face = [] #треуголиные грани
    norm = 1.0
    pix_w = 0.5
    pix_h = 0.5
    x = 0
    z = 0
    for j in xrange(0, height):
        for i in xrange(0, width):
            res = (pixels[i, j][0] + pixels[i,j][1] + pixels[i,j][2])//3
            imgDraw.point((i, j), (res,res,res)) #градации серого
            h = round(res * (norm/255.0), 2)
            heightmap.append(str(h))
            if j == 0 :
                coord.extend([x, h, z, x, h, z + pix_h, x + pix_w/2, h, z + pix_h/2])
                x+=pix_w
                if (i == width-1) :
                    coord.extend([x, h, z, x, h, z + pix_h])
            else:
                coord.extend([x, h, z + pix_h, x + pix_w/2, h, z + pix_h/2])
                x+=pix_w
                if (i == width-1) :
                    coord.extend([x, h, z + pix_h])
        x = 0
        z +=pix_h
    
    #генерируем треугольные грани
    step = 0
    step2 = 0
    temp = 0
    for j in xrange(0,height):
        for i in xrange(0,width):
            if j == 0:
                face.extend([0, 1+step, 0+step, 2+step,\
                            0, 0+step, 3+step, 2+step,\
                            0, 3+step, 4+step, 2+step,\
                            0, 4+step, 1+step, 2+step])
                step+=3
            elif j==1:
                face.extend([0, 1+step, 0+step-(width*3), 2+step]) \
                if i==0 else face.extend([0, 1+step, 0+step+1-(width*3), 2+step])
                face.extend([0, 0+step-(width*3), 3+step-(width*3), 2+step])\
                if i==0 else face.extend([0, 0+step+1-(width*3), 3+step-(width*3), 2+step])
                face.extend([0, 3+step-(width*3), 4+step-1, 2+step,\
                            0, 4+step-1, 1+step, 2+step])
                step+=2
            else:
                face.extend([0, 1+step, 0+step-(width*2), 2+step,\
                0, 0+step-(width*2), 3+step-(width*2)-1, 2+step,\
                0, 3+step-(width*2)-1, 4+step-1, 2+step,\
                0, 4+step-1, 1+step, 2+step])
                step+=2
        step+=1
    out = str(json.dumps(dict(zip(["vertices","faces"], 
                    [coord,face])+[("metadata",{"formatVersion" : 3})])) )
    with open('./app/static/model/model_1.js', 'w') as outfile:
        outfile.write(out)
    return heightmap,width,height,norm
#make_json_model('../images/upload_pictures/upload_picture.jpg')