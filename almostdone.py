import copy
import random
import keyboard
import numpy
import pygame
import time
import os, sys
import numpy as np
import math
from operator import xor
np.set_printoptions(threshold=sys.maxsize)
pygame.init()




WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 127, 0)

font = pygame.font.SysFont('Comic Sans MS', 20)

size = (360, 360)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake")

done = False

clock = pygame.time.Clock()

scale = 30
map = np.zeros((int(size[0]/scale), int(size[1]/scale)))
copymap = np.zeros((int(size[0]/scale), int(size[1]/scale)))
realmap = np.zeros((int(size[0]/scale), int(size[1]/scale)))
temptail = False
def a_star_search(start, end):
    global temptail, reallastseentail
    # print(start.x, start.y, '   ', end.x, end.y)
    open_list = []
    close_list = []
    open_list.append(start)
    while len(open_list) > 0:
        current_grid = find_min_gird(open_list)
        open_list.remove(current_grid)
        close_list.append(current_grid)
        neighbors = find_neighbors(current_grid, open_list, close_list)
        for grid in neighbors:
            if grid not in open_list:
                grid.init_grid(current_grid, end)
                open_list.append(grid)
            for grid in open_list:
                if (grid.x == end.x) and (grid.y == end.y):
                    return grid
    return None
def find_min_gird(open_list=[]):
    """
    fing min f_cost
    :param open_list:
    :return:
    """
    temp_grid = open_list[0]
    for grid in open_list:
        if grid.f < temp_grid.f:
            temp_grid = grid
    return temp_grid
def find_neighbors(grid,open_list=[],close_list=[]):
    """
    fin adjecent grid
    :param grid:
    :param open_list:
    :param close_list:
    :return:
    """
    grid_list = []
    if is_valid_grid(grid.x, grid.y-1, open_list, close_list):
        grid_list.append(Grid(grid.x, grid.y-1))
    if is_valid_grid(grid.x, grid.y+1, open_list, close_list):
        grid_list.append(Grid(grid.x, grid.y+1))
    if is_valid_grid(grid.x-1, grid.y, open_list, close_list):
        grid_list.append(Grid(grid.x-1,grid.y))
    if is_valid_grid(grid.x+1, grid.y, open_list, close_list):
        grid_list.append(Grid(grid.x+1, grid.y))
    return grid_list
def is_valid_grid(x,y,open_list=[],close_list=[]):
    """
    decide whether overstep
    :param x:
    :param y:
    :param open_list:
    :param close_list:
    :return:
    """
    #over border
    if x < 0 or x >=len(map) or y < 0 or y >= len(map[0]):
        return False
    #obstacle
    if map[x][y] == 1:
        return False
    #if inopen list
    if contain_grid(open_list, x, y):
        return False
    #if in close list
    if contain_grid(close_list, x, y):
        return False
    return True
def contain_grid(grids, x, y):
    for grid in grids:
        if (grid.x == x) and (grid.y == y):
            return True
    return False
class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None

    def init_grid(self, parent, end):
        self.parent = parent
        if parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 1
        self.h = abs(self.x - end.x) + abs(self.y - end.y)
        self.f = self.g + self.h
class Snake():
    global map
    def __init__(self):
        self.alive = True
        self.length = 1
        self.tail = []
        self.x = 0
        self.y = 0
        self.xV = 0
        self.yV = 1
        self.tick = 0
    def draw(self, vir = 0):
        for section in self.tail:
            if vir == 0:
                pygame.draw.rect(screen, WHITE, (((section[0]) * scale), ((section[1]) * scale) , scale, scale))
            elif vir == 1:
                pygame.draw.rect(screen, (200, 0, 0), (((section[0]) * scale), ((section[1]) * scale), scale, scale))
            else:
                pygame.draw.rect(screen, (200, 0, 200), (((section[0]) * scale), ((section[1]) * scale), scale, scale))
            if section == self.tail[0]:
                pygame.draw.rect(screen, (255, 0, 255), (((section[0]) * scale), ((section[1]) * scale), scale, scale))
            if section == self.tail[len(self.tail)-1]:
                pygame.draw.rect(screen, (0, 0, 255), (((section[0]) * scale), ((section[1]) * scale), scale, scale))

    def update(self):
        if self.alive == True:
            self.x += self.xV
            self.y += self.yV
            tempt = copy.deepcopy(self.tail)

            self.tail.append((self.x, self.y))
            while len(self.tail) > self.length:
                self.tail.pop(0)
        if self.x == -1:
            self.alive = False
            self.x = 0
        if self.x == (size[0] / scale):
            self.alive = False
            self.x = (size[0] / scale) - 1
        if self.y == -1:
            self.alive = False
            self.y = 0
        if self.y == (size[1] ) / scale:
            self.alive = False
            self.y = ((size[1] ) / scale) - 1
        map[:, :] = 0
        for j in self.tail:
            map[j[0], j[1]] = 1
        map[self.x][self.y] = 1
        if self.alive == True:
            for segment in tempt:
                if segment[0] == self.x and segment[1] == self.y:
                    # self.alive = False
                    pass


    def reset(self):
        self.alive = True
        self.length = 1
        self.tail.clear()
        self.x = 0
        self.y = 0
        self.xV = 0
        self.yV = 1
        self.tick = 0
class Food():
    global map
    def __init__(self):
        self.x = random.randrange((size[0] / scale) - 1)
        self.y = random.randrange(((size[1]) / scale) - 1)
        map[self.x][self.y] = 3

    def draw(self):
        pygame.draw.rect(screen, RED, ((self.x * scale), (self.y * scale), scale, scale))
    def update(self):
        map[self.x][self.y] = 3
        if snake.x == self.x and snake.y == self.y:
            # print('apple eaten')
            # time.sleep(1)
            self.reset()
            snake.length += 1

    def reset(self):
        success = False
        while success == False:
            self.x = random.randrange((size[0] / scale))
            self.y = random.randrange(((size[1]) / scale))
            if map[self.x][self.y] == 0:
                success = True
        map[self.x][self.y] = 3
class Utility():
    def __init__(self):
        return

    def draw(self):
        pygame.draw.line(screen, BLACK, (0, 0), (size[0], 0), 7)
        if snake.alive == False:
            print('snake dead')
            # time.sleep(50)

        if int(size[1]) > int(size[0]):
            for i in range(int(size[1] / scale)):
                pygame.draw.line(screen, BLACK, (0, ((i * scale) + scale)), (size[0], ((i * scale) + scale)), 3)
                pygame.draw.line(screen, BLACK, (((i * scale) + scale), 0), (((i * scale) + scale), size[1]), 3)
        else:
            for i in range(int(size[0] / scale)):
                pygame.draw.line(screen, BLACK, (0, ((i * scale) + scale)), (size[0], ((i * scale) + scale)), 3)
                pygame.draw.line(screen, BLACK, (((i * scale) + scale), 0), (((i * scale) + scale), size[1]), 3)

    def update(self):
        return
def fakeupdate(roadd):
    global fakesnake, snake
    fakesnake = copy.deepcopy(snake)
    if abs(roadd[1][0] - snake.x) == 1 and roadd[1][1] - snake.y == 0:
        if roadd[1][0] - snake.x == 1:
            fakesnake.yV = 0
            fakesnake.xV = 1
        else:
            fakesnake.yV = 0
            fakesnake.xV = -1
    if roadd[1][0] - snake.x == 0 and abs(roadd[1][1] - snake.y) == 1:
        if roadd[1][1] - snake.y == 1:
            fakesnake.xV = 0
            fakesnake.yV = 1
        else:
            fakesnake.xV = 0
            fakesnake.yV = -1
    fakesnake.update()
def dect(x, y):
    global map, snake, food, scale, trysnake, size, reallastseentail, temptail
    trysnake.reset()
    trysnake = copy.deepcopy(snake)
    trysnake.xV = x
    trysnake.yV = y
    trysnake.update()
    map[snake.x][snake.y] = 1
    map[trysnake.x][trysnake.y] = 0
    map[reallastseentail[0]][reallastseentail[1]] = 0
    copymap[snake.x][snake.y] = 0
    copymap[food.x][food.y] = 0
    np.savetxt('map.txt', map.T, fmt='%d')
    pygame.draw.rect(screen, (0, 255, 0), (((trysnake.x) * scale), ((trysnake.y) * scale), scale, scale))
    # pygame.draw.rect(screen, (0, 255, 255), (((reallastseentail[0]) * scale), ((reallastseentail[1]) * scale), scale-5, scale-5))
    if trysnake.x == reallastseentail[0] and trysnake.y == reallastseentail[1]:
        return 1
    else:
        path = []
        road = []
        start_grid = Grid(int(trysnake.x), int(trysnake.y))
        end_grid = Grid(int(reallastseentail[0]), int(reallastseentail[1]))
        result_grid = a_star_search(start_grid, end_grid)
        if temptail is True:
            temptail = False
            return 1
        else:
            while result_grid is not None:
                path.append(Grid(result_grid.x, result_grid.y))
                result_grid = result_grid.parent
            for paths in path:
                road.append((paths.x, paths.y))
            if (abs(trysnake.x - reallastseentail[0]) + abs(trysnake.y - reallastseentail[1]) == 1) and (abs(trysnake.x - reallastseentail[0]) + abs(trysnake.y - reallastseentail[1]) == 0):
                print('besisde')
                time.sleep(2)
                debug = True
            else:
                debug = False
            if len(road) == 0 and debug is False:
                return 0
            else:
                return 1



def findToTail():
    global direction, u, d, l, r, trysnake, snake, map

    if u != -1:
        if dect(0, -1):
            direction[0] = 2
        else:
            direction[0] = 1
            pygame.draw.rect(screen, (200, 100, 100), (((trysnake.x) * scale), ((trysnake.y) * scale), scale, scale))
    else:
        direction[0] = 1
    if d != -1:
        if dect(0, 1):

            direction[1] = 2
        else:
            direction[1] = 1
            pygame.draw.rect(screen, (200, 100, 100), (((trysnake.x) * scale), ((trysnake.y) * scale), scale, scale))
    else:
        direction[1] = 1
    if l != -1:

        if dect(-1, 0):

            direction[2] = 2
        else:
            direction[2] = 1
            pygame.draw.rect(screen, (200, 100, 100), (((trysnake.x) * scale), ((trysnake.y) * scale), scale, scale))
    else:
        direction[2] = 1
    if r != -1:

        if dect(1, 0):

            direction[3] = 2
        else:
            direction[3] = 1
            pygame.draw.rect(screen, (200, 100, 100), (((trysnake.x) * scale), ((trysnake.y) * scale), scale, scale))
    else:
        direction[3] = 1
    utility.draw()
    pygame.display.update()

snake = Snake()
virsnake = Snake()
fakesnake = Snake()
trysnake = Snake()
food = Food()
virfood = Food()
utility = Utility()
eatenVirApple = False
lastseentail = [-1, -1]
snake.update()
food.update()
utility.update()
foundtail = True
reallastseentail = [-1, -1]
direction = [0, 0, 0, 0]
while not done:
    reallastseentail = snake.tail[0]
    realmap = copy.deepcopy(map)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.set_caption('snake')
    screen.fill((0, 0, 0))

    safe = True

    copymap = copy.deepcopy(map)
    virsnake = copy.deepcopy(snake)
    virfood = copy.deepcopy(food)

    while eatenVirApple == False:   #開始跑虛擬吃蘋果
        # map[virsnake.tail[0][0]][virsnake.tail[0][1]] = 0
        lastseentail = virsnake.tail[0]
        virpath = []
        virroad = []
        virstart_grid = Grid(virsnake.x, virsnake.y)
        virend_grid = Grid(virfood.x, virfood.y)
        drawVirPath = False
        while drawVirPath is False:
            virresult_grid = a_star_search(virstart_grid, virend_grid)
            while virresult_grid is not None:
                virpath.append(Grid(virresult_grid.x, virresult_grid.y))
                virresult_grid = virresult_grid.parent
            for virpaths in virpath:
                virroad.append((virpaths.x, virpaths.y))
            virroad.reverse()
            if len(virroad) == 0:
                virpath.clear()
                virroad.clear()
                safe = False
                eatenVirApple = True
                drawVirPath = True
                continue
            else:
                drawVirPath = True
        if safe == True:
            if abs(virroad[1][0] - virsnake.x) == 1 and virroad[1][1] - virsnake.y == 0:
                if virroad[1][0] - virsnake.x == 1:
                    virsnake.yV = 0
                    virsnake.xV = 1
                else:
                    virsnake.yV = 0
                    virsnake.xV = -1
            if virroad[1][0] - virsnake.x == 0 and abs(virroad[1][1] - virsnake.y) == 1:
                if virroad[1][1] - virsnake.y == 1:
                    virsnake.xV = 0
                    virsnake.yV = 1
                else:
                    virsnake.xV = 0
                    virsnake.yV = -1

            virsnake.update()
            if virfood.x == virsnake.x and virfood.y == virsnake.y:
                eatenVirApple = True
                foundtail = False
            else:
                virfood.update()

    #                   吃完虛擬蘋果看尾  以下是尾吧
    if safe is True:
        while foundtail is False:
            virtailpath = []
            virtailroad = []
            virtailstart_grid = Grid(virsnake.x, virsnake.y)
            virtailend_grid = Grid(lastseentail[0], lastseentail[1])
            while 1:
                virtailresult_grid = a_star_search(virtailstart_grid, virtailend_grid)
                while virtailresult_grid is not None:
                    virtailpath.append(Grid(virtailresult_grid.x, virtailresult_grid.y))
                    virtailresult_grid = virtailresult_grid.parent
                for virtailpaths in virtailpath:
                    virtailroad.append((virtailpaths.x, virtailpaths.y))
                virtailroad.reverse()
                #bug應該在這邊  假設蘋果在旁邊但是是死路 還是會走過去自殺
                if (abs(virsnake.x - virfood.x) + abs(virsnake.y - virfood.y) == 1):
                    debug = True
                else:
                    debug = False
                if len(virtailroad) == 0 and debug is False:
                    print('snake pos', snake.x, snake.y, '  /  debug = ', debug)
                    virtailpath.clear()
                    virtailroad.clear()
                    safe = False
                    foundtail = True
                    map = copy.deepcopy(copymap)
                    break
                else:
                    foundtail = True
                    map = copy.deepcopy(copymap)
                    break

#   finish virtual searching//////////////////////////////////////////////////////////

    screen.fill((100, 100, 100))
    food.draw()
    snake.draw()
    utility.draw()
    pygame.display.update()
    if safe is False:

        # print('not safe to move')
        map[reallastseentail[0]][reallastseentail[1]] = 0
        if snake.y != 0:
            if map[snake.x][snake.y-1] == 0:
                u = (food.y-(snake.y-1))**2 + (food.x-snake.x)**2
            else:
                # print('u wall')
                u = -1
        else:
            # print('y = 0')
            u = -1
        if snake.x != (len(map)-1):
            if map[snake.x+1][snake.y] == 0:
                r = (food.y - snake.y )**2 + (food.x-(snake.x+1))**2
            else:
                # print('r wall')
                r = -1
        else:
            # print('x max')
            r = -1
        if snake.y != (len(map[0])-1):
            if map[snake.x][snake.y+1] == 0:
                d = (food.y - (snake.y+1)) ** 2 + (food.x - snake.x) ** 2
            else:
                # print('d wall')
                d = -1
        else:
            # print('d max')
            d = -1
        if snake.x != 0:
            if map[snake.x-1][snake.y] == 0:
                l = (food.y - snake.y) ** 2 + (food.x - (snake.x-1)) ** 2
            else:
                # print('l wall')
                l = -1
        else:
            # print('x = 0')
            l = -1
        direction = [0, 0, 0, 0]
        findToTail()

        while 1:

            if u >= d and u >= l and u >= r:
                if direction[0] == 2:
                    snake.xV = 0
                    snake.yV = -1
                    safe = True
                    eatenVirApple = False
                    # print('moved u')
                    break
                else:
                    direction[0] = 1
                    u = -2
            elif d >= u and d >= l and d >= r:
                if direction[1] == 2:
                    snake.xV = 0
                    snake.yV = 1
                    safe = True
                    eatenVirApple = False
                    # print('moved d')
                    break
                else:
                    direction[1] = 1
                    d = -2
            elif l >= u and l >= d and l >= r:
                if direction[2] == 2:
                    snake.xV = -1
                    snake.yV = 0
                    safe = True
                    eatenVirApple = False
                    # print('moved l')
                    break
                else:
                    direction[2] = 1
                    l = -2
            elif r >= u and r >= d and r >= l:
                if direction[3] == 2:
                    snake.xV = 1
                    snake.yV = 0
                    safe = True
                    eatenVirApple = False
                    # print('moved r')
                    break
                else:
                    direction[3] = 1
                    r = -2
            elif 2 not in direction:
                print('errrorrrrr')
                time.sleep(1000)
        # print('   %d\n%d      %d\n   %d' % (u, l, r, d))
        # print(direction)
    else:
        path = []
        road = []
        start_grid = Grid(snake.x, snake.y)
        end_grid = Grid(food.x, food.y)
        drawPath = False
        while drawPath == False:
            result_grid = a_star_search(start_grid, end_grid)
            while result_grid is not None:
                path.append(Grid(result_grid.x, result_grid.y))
                result_grid = result_grid.parent
            for paths in path:
                road.append((paths.x, paths.y))
            road.reverse()
            if len(road) == 0:
                print('error')
                break
            else:
                drawPath = True
        if abs(road[1][0] - snake.x) == 1 and road[1][1] - snake.y == 0:
            if road[1][0] - snake.x == 1:
                snake.yV = 0
                snake.xV = 1
            else:
                snake.yV = 0
                snake.xV = -1
        if road[1][0] - snake.x == 0 and abs(road[1][1] - snake.y) == 1:
            if road[1][1] - snake.y == 1:
                snake.xV = 0
                snake.yV = 1
            else:
                snake.xV = 0
                snake.yV = -1

    fakeupdate(road)

    if food.x == fakesnake.x and food.y == fakesnake.y:
        eatenVirApple = False


    screen.fill((100, 100, 100))
    snake.update()
    food.update()
    food.draw()
    snake.draw()
    utility.draw()
    pygame.display.update()

    clock.tick(60)
pygame.quit()