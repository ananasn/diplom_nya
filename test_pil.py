# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

text = "Nya ^_^"
bg_color = (170,140,170)

img = Image.new('RGB',(200,200),bg_color)
imgDraw = ImageDraw.Draw(img)
imgDraw.text((80,100),text)
img.save("./images/img_test.png")