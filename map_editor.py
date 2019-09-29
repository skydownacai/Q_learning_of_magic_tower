import pygame
import sys
import os
import threading
pygame.init()  # 初始化pygame
pygame.display.set_caption("魔塔地图编辑器")
TEXT = pygame.font.SysFont("sans-serif",25)
import json
class VISUAL:
	object = {
	}
	floor_count = 0
	def __init__(self):

		self.screen_row = 11
		self.screen_column = 17
		self.map_row = 11
		self.map_column = 11
		self.screen_block_width = 32
		self.floor = []
		size = self.screen_column * self.screen_block_width, self.screen_row * self.screen_block_width  # 设置窗口大小
		self.screen = pygame.display.set_mode(size)  #
		self.pic = []
		self.pickup = None
		for category in ['doors','walls','background',]:
			this_dir = 'img/'+category +'/'
			for file in os.listdir(this_dir):
				file_name = file.split('.')[0]
				VISUAL.object[file_name] = pygame.image.load(this_dir + file)
		self.floor_index = 0
		self.choose_item = {}
		self.floor_item = {
		}
		this_floor_index = 0
		for floor_file in os.listdir("floor"):
			self.floor_item[this_floor_index] = {}
			this_floor = json.loads(open("floor/{}".format(floor_file), 'r').read())
			self.floor.append(this_floor)  # 首先载入楼层样式
			for item in this_floor:
				self.floor_item[this_floor_index][str([item[1],item[2]])] = item[0]
			this_floor_index +=1
	def render(self, obj,row, coloumn):
		if isinstance(obj,str):
			self.screen.blit(VISUAL.object[obj], (coloumn * self.screen_block_width, row * self.screen_block_width))
		if isinstance(obj,pygame.Surface):
			self.screen.blit(obj, (coloumn * self.screen_block_width, row * self.screen_block_width))
	def render_floor(self, index = None):
		if index == None:
			index = self.floor_index
		if len(self.floor) == 0:
			return 0
		for item in self.floor[index]:
			self.render(item[0], item[1], item[2])
	def drawbackground(self):
		for i in range(self.map_row):
			for j in range(self.map_column):
				self.render('ground', i, j)
		notice = TEXT.render("Now Floor : {}".format(self.floor_index + 1),0,(255,255,255))
		notice1 = TEXT.render("Item".format(self.floor_index),0,(255,255,255))
		notice2 = TEXT.render("SAVE".format(self.floor_index),0,(255,255,255))
		notice3 = TEXT.render("CLEAR".format(self.floor_index),0,(255,255,255))
		pygame.draw.rect(self.screen,(200,0,0),((11 * self.screen_block_width , 1 * self.screen_block_width),(6 * self.screen_block_width,1*self.screen_block_width)))
		pygame.draw.rect(self.screen,(0,200,0),((11 * self.screen_block_width , 5 * self.screen_block_width),(6 * self.screen_block_width,1*self.screen_block_width)))
		pygame.draw.rect(self.screen,(150,200,0),((11 * self.screen_block_width , 6 * self.screen_block_width),(6 * self.screen_block_width,1*self.screen_block_width)))

		self.render("stair_up",0,15)
		self.render("stair_down",0,16)
		self.screen.blit(notice, (11 * self.screen_block_width, 0 * self.screen_block_width + 8))
		self.screen.blit(notice1, (11 * self.screen_block_width, 1 * self.screen_block_width + 8))
		self.screen.blit(notice2, (11 * self.screen_block_width, 5 * self.screen_block_width + 8))
		self.screen.blit(notice3, (11 * self.screen_block_width, 6 * self.screen_block_width + 8))

		pointer = [2,11]
		for file in VISUAL.object:

			surface = VISUAL.object[file]
			self.choose_item[str(pointer)] = file
			self.render(surface,pointer[0],pointer[1])
			pointer[1] += 1
			if pointer[1] >= 17:
				pointer[1] -= 6
				pointer[0] += 1
	def get_mouse_pos(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			col, row = int(x / self.screen_block_width), int(y / self.screen_block_width)
			return (col,row)
	def run(self):
		while True:  # 死循环确保窗口一直显示
			self.screen.fill((0, 0, 0))
			self.drawbackground()
			self.render_floor()
			if self.pickup != None:
				x, y = pygame.mouse.get_pos()
				self.screen.blit(self.pickup_img ,(x, y))

			for event in pygame.event.get():  # 遍历所有事件

				if  event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 3:
						self.pickup = None
						self.pickup_img = None
					col,row = self.get_mouse_pos(event)
					if event.button == 2 and col <= 10 and row <= 10:
						try:
							pickup = self.floor_item[str([row,col])]
							print('clean',pickup)
							self.floor[self.floor_index].remove(
								[pickup,row,col]
							)
						except:
							pass
					if event.button == 1:
						if col <= 10 and row <= 10:
							if self.pickup != None:
								try:
									origin_pickup = self.floor_item[str([row, col])]
									print('clean', origin_pickup)
									self.floor[self.floor_index].remove(
										[origin_pickup, row, col]
									)
								except:
									pass
								self.floor[self.floor_index].append(
									[self.pickup,row,col]
								)
								self.floor_item[
									str([row,col])
								] = self.pickup
						if col >= 11 and col <= 17 and row >= 2 and row <= 4:
							try:
								self.pickup = self.choose_item[str([row, col])]
								self.pickup_img = VISUAL.object[self.pickup]
								print('pick up', self.pickup)
							except:
								pass

						if col >= 11 and row == 5:
							for index in range(len(self.floor)):
								with open("floor/floor_{}.json".format(index + 1),'w') as f:
									f.write(json.dumps(self.floor[index]))
							print('保存成功')
						if col >= 11 and row == 6:
							self.floor[self.floor_index] = []
							self.floor_item[self.floor_index] = {}
							print('清空成功')
					if event.button == 3:
						self.pickup = None
						self.pickup_img = None
					if col == 15 and row == 0:
						self.floor_index += 1
						print("switch follor")
						if self.floor_index >= len(self.floor):
							self.floor.append([])
							self.floor_item[self.floor_index] = {}
					if col == 16 and row == 0:
						self.floor_index -= 1
						print("switch follor")
						self.floor_index = max(0,self.floor_index)

				if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
					sys.exit()

			pygame.display.update()
screen = VISUAL()
screen.run()