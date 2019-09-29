import pygame
import sys
import os
import json
from world import *
import time
import os
import random
class Dot:
    def __init__(self,row,column):
        self.row = row
        self.column = column
        self.parent = None

    @property
    def children(self):
        raw = [self.up,self.down,self.left,self.right]
        childrens = []
        for children in raw:
            if children  != None and (self.parent == None or [children.row,children.column] != [self.parent.row,self.parent.column]):
                children.parent = self
                childrens.append(children)

        return childrens

    @property
    def up(self):
        if self.row - 1 >= 0:
            return Dot(self.row - 1,self.column)
        else:
            return None
    @property
    def down(self):
        if self.row + 1 <= 10:
            return Dot(self.row + 1,self.column)
        else:
            return None
    @property
    def left(self):
        if self.column - 1 >= 0:
            return Dot(self.row ,self.column - 1)
        else:
            return None
    @property
    def right(self):
        if self.column + 1 <= 10:
            return Dot(self.row ,self.column + 1)
        else:
            return None
class GUI:
    object = {
    }
    floor_count = 0
    FPS = 30
    def __init__(self,world):
        self.screen_row = 11
        self.screen_column = 11
        self.screen_block_width = 32
        pygame.init()  # 初始化pygame
        pygame.display.set_caption("魔塔")
        self.move_steptime = 0.5
        self.visualworld = world
        # 获得pygame的时钟
        self.clock = pygame.time.Clock()
        self.visualworld.gui = self
        self.warrior_direction =["","_leftfoot","_stop","_rightfoot"]
        self.warrior_direction_pointer = 0
        self.monster_direction = ["","_move"]
        self.total_frame = 0

        size = self.screen_row * self.screen_block_width, self.screen_column * self.screen_block_width  # 设置窗口大小
        self.screen = pygame.display.set_mode(size)  #
        for category in ['doors','walls','background','items','monsters','warrior','monsters_move']:
            this_dir = 'img/'+category +'/'
            for file in os.listdir(this_dir):
                door_name = file.split('.')[0]
                GUI.object[door_name] = pygame.image.load(this_dir + file)

        self.init = True
    def render_object(self,obj_name,row,coloumn,row_offset = 0,column_offset = 0):
        self.screen.blit(GUI.object[obj_name],(coloumn * self.screen_block_width + column_offset,row * self.screen_block_width + row_offset))

    def visual_history(self,world):
        pass
    @staticmethod
    def position_to_str(row,col):
        return str(row) + "_" + str(col)
    @staticmethod
    def positionstr_to_tuple(str:str):
        after_split = str.split("_")
        return list(map(int,after_split))

    def add_floor(self,floor_style_array):
        '''
        floor_style_array 每个元素类似于 (item_name,item_row,item_column)
        :param floor:
        :param floor_style_array:
        :return:
        '''
        now_floor = len(self.floor)
        self.floor[now_floor] = {}
        for item in floor_style_array:
            self.floor[now_floor][GUI.position_to_str(item[1],item[2])] = item[0]
            if "stair" in item[0]:
                self.floor[now_floor][item[0]] = (item[1],item[2])

        GUI.floor_count += 1
    def drawbackground(self):
        for i in range(self.screen_row):
            for j in range(self.screen_column):
                self.render_object('ground',i,j)
    def reset(self):
        self.floor_item = {
            0: { }
        }
        self.floor = {}
        self.floor_index = self.visualworld.warrior.floor - 1

        for floor_file in os.listdir("floor"):
            this_floor = json.loads(open("floor/{}".format(floor_file), 'r').read())
            self.add_floor(this_floor)  # 首先载入楼层样式

        for item in self.visualworld.items:
            self.floor[item.floor - 1][GUI.position_to_str(item.row,item.column)] = item

    def render_floor(self,index):
        if len(self.floor) == 0:
            return 0
        gap = 0
        for str_postion in self.floor[index]:
            if "stair" in str_postion:
                continue
            row,col = GUI.positionstr_to_tuple(str_postion)
            item = self.floor[index][str_postion]
            try:
                self.render_object(item,row,col)
            except:
                if item.TYPE == "monster":
                    item.icon_pointer = (int(self.total_frame / 4) + gap) % 2
                    item.now_icon = item.icon + self.monster_direction[item.icon_pointer]
                else:
                    item.now_icon = item.icon
                self.render_object(item.now_icon,row,col)
                gap += 1

    def render_warrior(self):
        warrior = self.visualworld.warrior
        warrior.now_icon = warrior.icon + self.warrior_direction[self.warrior_direction_pointer]
        self.render_object(warrior.now_icon, warrior.row, warrior.column)
        if self.total_frame % 5 == 0:
            self.warrior_direction_pointer = (self.warrior_direction_pointer + 1)%4

    def valid_dot(self,dot : Dot):
        try:
            if self.position_to_str(dot.row,dot.column) in self.floor[self.floor_index]:
                return  False
        except:
            print("dot",(dot.row,dot.column),"floor_index",self.floor_index)
            import traceback
            print(traceback.format_exc())
            print()
        return  True

    def find_way_within_floor(self,target_postion:list,start_postion:list):
        '''
        :param target_postion:
        :return: [next_position,...,target_postition]way sequense
        '''
        target_postion = list(target_postion)
        start  = Dot(start_postion[0],start_postion[1])
        has_visited = [start]
        has_been = [start_postion]
        end = False
        while True:
            this_dot = has_visited.pop()
            self.visualworld.warrior.row = this_dot.row
            self.visualworld.warrior.column = this_dot.column
            for children in this_dot.children:
                children_pos = [children.row,children.column]
                if target_postion == children_pos:
                    end = True
                    break
                if self.valid_dot(children) and children_pos not in has_been:
                    has_visited.append(children)
            if end:
                break
            for dot in has_visited:
               has_been.append([dot.row,dot.column])
        movements = []
        while True:
            movements.append((this_dot.row,this_dot.column))
            this_dot = this_dot.parent
            if this_dot == None:
                break
        return movements[::-1]

    def render_walking(self,position_seq :list):
        '''
        :param position_seq:
        :return:
        '''
        warrior = self.visualworld.warrior
        for move in position_seq:
            warrior.row,warrior.column = move
            time.sleep(0.02)

    def go(self,target : Object):
        '''
        让 warrior 走到 目边旁边
        Object.floor 都是从 1 开始计数
        GUI.floor 从0 开始计数
        :param target:
        :return:
        '''
        target_postion = [target.row,target.column]
        warrior = self.visualworld.warrior
        start_position = [warrior.row,warrior.column]
        target_floor = target.floor
        while True:
            if target_floor == self.floor_index + 1:
                break
            if target_floor > self.floor_index + 1:
                '''上楼'''
                way = self.find_way_within_floor(self.floor[self.floor_index]['stair_up'],start_position)
                self.render_walking(way)
                warrior.row, warrior.column = self.floor[self.floor_index]['stair_up']
                self.floor_index += 1
                start_position = self.floor[self.floor_index]['stair_down']

            if target_floor < self.floor_index + 1:
                '''下楼'''
                way = self.find_way_within_floor(self.floor[self.floor_index]['stair_down'],start_position)
                self.render_walking(way)
                warrior.row, warrior.column = self.floor[self.floor_index]['stair_down']
                self.floor_index -= 1
                start_position = self.floor[self.floor_index]['stair_up']

        way = self.find_way_within_floor(target_postion,start_position)
        self.render_walking(way)

    def run(self):
        while True:  # 死循环确保窗口一直显示
            self.screen.fill((0,0,0))
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
            self.drawbackground()
            if self.init:
                self.reset()
                self.init = False
            self.render_floor(self.floor_index)
            self.render_warrior()
            pygame.display.update()
            self.clock.tick(GUI.FPS)
            self.total_frame += 1