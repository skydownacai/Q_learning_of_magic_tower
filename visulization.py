from testmap import *
from floor_style import *
import pygame
import sys
import os
import threading
pygame.init()  # 初始化pygame
pygame.display.set_caption("魔塔")
class GUI:
    game = world
    object = {
    }
    floor_count = 0
    def __init__(self):
        self.screen_row = 11
        self.screen_column = 11
        self.screen_block_width = 32
        self.floor = []
        size = width, height = self.screen_row * self.screen_block_width, self.screen_column * self.screen_block_width  # 设置窗口大小
        self.screen = pygame.display.set_mode(size)  #
        for category in ['doors','walls','background']:
            this_dir = 'img/'+category +'/'
            for file in os.listdir(this_dir):
                door_name = file.split('.')[0]
                GUI.object[door_name] = pygame.image.load(this_dir + file)
    def render_object(self,obj_name,row,coloumn):
        self.screen.blit(GUI.object[obj_name],(coloumn * self.screen_block_width,row * self.screen_block_width))


    def add_floor(self,floor_style_array):
        '''
        floor_style_array 每个元素类似于 (item_name,item_row,item_column)
        :param floor:
        :param floor_style_array:
        :return:
        '''
        self.floor.append(floor_style_array)
        GUI.floor_count += 1
    def drawbackground(self):
        for i in range(self.screen_row):
            for j in range(self.screen_column):
                self.render_object('ground',i,j)
    def render_floor(self,index):
        if len(self.floor) == 0:
            return 0
        for item in self.floor[index]:
            self.render_object(item[0],item[1],item[2])
    def run(self):
        while True:  # 死循环确保窗口一直显示
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
            self.drawbackground()
            self.render_floor(0)
            pygame.display.update()

screen = GUI()
screen.add_floor(floor1)
screen.run()