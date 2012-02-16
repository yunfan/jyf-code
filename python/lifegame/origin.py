#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import random
import pygame
import time
import copy
from sys import exit

genint = lambda m: random.randint(0, m)

class GridBox:
    def __init__(self, width, height, cell_size, status_colors):
        self.grid_width = width
        self.grid_height = height
        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]
        self.cells = [None for idx in xrange(width*height)]
        self.status_colors = status_colors
        pygame.init()
        self.screen = pygame.display.set_mode(
            (width*cell_size[0], height*cell_size[1]),
            pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN,    ## 双缓冲
            32)
        self.clear()

    def fill(self, pos, status):
        offset = pos[1] * self.grid_width + pos[0]      # y * width + x
        #print 'offset', offset, 'status', status
        rect = self.cells[offset]
        self.cells[offset] = self.screen.fill(self.status_colors[status],
                                            rect)

    def flush(self):
        pygame.display.update()
        pygame.display.flip()

    def clear(self):
        for y in xrange(self.grid_height):
            for x in xrange(self.grid_width):
                offset = y * self.grid_width + x
                left, top = x*self.cell_width, y*self.cell_height
                cell_w, cell_h = self.cell_width - 1, self.cell_height - 1
                self.cells[offset] = pygame.draw.rect(
                    self.screen, self.status_colors[0],
                    pygame.rect.Rect(left, top, cell_w, cell_h) )
        self.flush()


def TestGridBox():
    x, y = 128, 128
    cell_size = (4, 4)
    colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 255, 255),
    (127, 0, 0),
    (0, 127, 0),
    (0, 0, 127),
    (127, 127, 0),
    (0, 127, 127),
    (127, 127, 127),
    ]
    color_len = len(colors)
    gb = GridBox(x, y, cell_size, colors)
    for idx in xrange(9999):
        color = genint(color_len - 1)
        for n in xrange(100):
            pos_x, pos_y = genint(x-1), genint(y-1)
            gb.fill((pos_x, pos_y), color)

        gb.flush()
        if genint(100) > 90:
            gb.clear()
        time.sleep(0.001)

GenLifeCell = lambda alive, brother: [alive, brother]
GenPos = lambda x,y,world_size: (y%world_size[1])*world_size[0] + x%world_size[0]

class LifeEngine:
    def __init__(self, world_size, keep_numbers, born_numbers):
        self.world_size = world_size
        self.keep_numbers = keep_numbers
        self.born_numbers = born_numbers
        self.world = []
        self.alive_count = 0
        for y in xrange(world_size[1]):
            for x in xrange(world_size[0]):
                offset = GenPos(x, y, self.world_size)
                cell = GenLifeCell(False, 0)  ## dead and no brothers
                self.world.append(cell)

    def iterstep(self):
        old_world = copy.deepcopy(self.world)
        for y in xrange(self.world_size[1]):
            for x in xrange(self.world_size[0]):
                cell = old_world[GenPos(x, y, self.world_size)]
                #print cell
                if cell[0] and cell[1] not in self.keep_numbers:
                    #print 'dead', x, y
                    event = (x, y, False)   ## (pos_x, pos_y, alive)
                elif not cell[0] and cell[1] in self.born_numbers:
                    #print 'born', x, y
                    event = (x, y, True)
                else:
                    event = None
                if event is not None:
                    self.setcell(*event)
                    yield event

    def setcell(self, x, y, alive):
        cell = self.world[GenPos(x, y, self.world_size)]
        plus = 1 if alive else -1

        if cell[0] == alive:
            return

        cell[0] = alive
        #print 'setcell', cell
        self.alive_count += plus
        ## 设置周围节点的兄弟
        self.world[GenPos(x-1, y-1, self.world_size)][1] += plus
        self.world[GenPos(x-1, y, self.world_size)][1] += plus
        self.world[GenPos(x-1, y+1, self.world_size)][1] += plus
        self.world[GenPos(x, y-1, self.world_size)][1] += plus
        self.world[GenPos(x, y+1, self.world_size)][1] += plus
        self.world[GenPos(x+1, y-1, self.world_size)][1] += plus
        self.world[GenPos(x+1, y, self.world_size)][1] += plus
        self.world[GenPos(x+1, y+1, self.world_size)][1] += plus

class DrawShape:
    def __init__(self, engine):
        self.engine = engine

    def glider(self, x, y):
        self.engine.setcell(x, y+1, True)
        self.engine.setcell(x+1, y+2, True)
        self.engine.setcell(x+2, y, True)
        self.engine.setcell(x+2, y+1, True)
        self.engine.setcell(x+2, y+2, True)


def TestLifeEngine():
    world_size = (160, 120)
    keep_numbers = (2, 3)
    born_numbers = (3, )

    eng1 = LifeEngine(world_size, keep_numbers, born_numbers)
    #eng2 = LifeEngine(world_size, keep_numbers, born_numbers)
    #eng3 = LifeEngine(world_size, keep_numbers, born_numbers)

    draw = DrawShape(eng1)
    draw.glider(1,1)
    #draw = DrawShape(eng2)
    #draw.glider(16,1)
    #draw = DrawShape(eng3)
    #draw.glider(1, 48)

    step = 99

    cell_size = (4, 4)
    colors = [  (0, 0, 0), (127, 0, 0),
                (0, 0, 0), (0, 127, 0),
                (0, 0, 0), (0, 0, 127), ]

    gb = GridBox(world_size[0], world_size[1], cell_size, colors)

    for idx in xrange(step):
        for event in eng1.iterstep():
            #print "step", idx, "event", event
            status = 1 if event[2] else 0
            gb.fill(event[:2], status)
        gb.flush()
        #time.sleep(0.001)
    exit()

def test():
    TestLifeEngine()

if "__main__" == __name__:
    test()
