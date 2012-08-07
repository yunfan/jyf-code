#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import Image
import ImageDraw

def doit(im):
    pen = ImageDraw.Draw(im)
    ct = (im.size[0]/2, im.size[1]/2)

    #pen.line((0, ct[1], im.size[0], ct[1]), fill = '#f00')
    #pen.line((ct[0], 0, ct[0], im.size[1]), fill = '#f00')
    r = im.size[1]/2

    area = ( ct[0] - r, ct[1] - r, ct[0] + r, ct[1]+r)
    #pen.rectangle(area, fill='#0000ff')

    pen.pieslice(area, 0, 120, fill='#00ff00')
    pen.pieslice(area, 120, 170, fill='#ff0000')
    pen.pieslice(area, 170, 240, fill='#ff00ff')
    pen.pieslice(area, 240, 360, fill='#00ffff')
    pen.ellipse((ct[0]-r/2, ct[1]-r/2, ct[0]+r/2, ct[1]+r/2), fill='#fff')
    #im.show()
    pass

def main():
    size = (640, 480)
    fill_color = '#fff'
    im = Image.new('RGB', (size[0]*4, size[1]*4), fill_color)
    doit(im)
    fd = open("test.png", "w")
    im = im.resize(size, Image.ANTIALIAS)
    im.save(fd, "PNG")
    im.show()

main()
