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

	} # item_pic_name => item_surface

	floor_count = 0

	def __init__(self):

		self.screen_row = 15

		self.screen_column = 22

		self.map_row = 11

		self.map_column = 11

		self.screen_block_width = 32

		self.console_msg = ""

		size = self.screen_column * self.screen_block_width, self.screen_row * self.screen_block_width  # 设置窗口大小

		self.screen = pygame.display.set_mode(size)  #

		self.pic = []

		self.pickup = None #现在鼠标选择的item

		for category in ['doors','walls','background','items','monsters','npcs']:

			this_dir = 'img/'+category +'/'

			for file in os.listdir(this_dir):

				file_name = file.split('.')[0]

				VISUAL.object[file_name] = pygame.image.load(this_dir + file)

		self.floor = [] #每个floor需要渲染的item

		self.floor_index = 0 #当前画面的floor

		self.GetEditorItemByPos = {} # GetEditorItemByPos[pos] = item

		self.floor_item = {

		} #每一层楼的item  floor_item[floor][postion] = item

		this_floor_index = 0


		#载入已经有的数据

		for floor_file in os.listdir("floor"):

			self.floor_item[this_floor_index] = {}

			this_floor = json.loads(open("floor/{}".format(floor_file), 'r').read())

			self.floor.append(this_floor)  # 首先载入楼层样式

			for item in this_floor:

				self.floor_item[this_floor_index][str([item[1],item[2]])] = item[0]

			this_floor_index +=1


	def render(self, obj,row, coloumn):
		'''

		:param obj:  要render的item
		:param row:  obj的row
		:param coloumn: obj的column
		:return:
		'''
		if isinstance(obj,str):

			self.screen.blit(VISUAL.object[obj], (coloumn * self.screen_block_width, row * self.screen_block_width))

		if isinstance(obj,pygame.Surface):

			self.screen.blit(obj, (coloumn * self.screen_block_width, row * self.screen_block_width))

	def render_floor(self, index = None):

		'''
		渲染当前所处楼层
		:param index:
		:return:
		'''

		if index == None:

			index = self.floor_index

		if len(self.floor) == 0:

			return 0

		for pos_str in self.floor_item[index]:


			pos = list(map(int,pos_str[1:-1].split(",")))

			self.render(self.floor_item[index][pos_str], pos[0], pos[1])


	def drawbackground(self):

		for i in range(self.map_row):

			for j in range(self.map_column):

				self.render('ground', i, j)

		notice = TEXT.render("Now Floor : {}".format(self.floor_index + 1),0,(255,255,255))

		notice1 = TEXT.render("Item",0,(255,255,255))

		notice2 = TEXT.render("SAVE",0,(255,255,255))

		notice3 = TEXT.render("CLEAR",0,(255,255,255))

		pygame.draw.rect(self.screen,(200,0,0),((11 * self.screen_block_width , 1 * self.screen_block_width),((self.screen_column - self.map_column) * self.screen_block_width,1*self.screen_block_width)))

		pygame.draw.rect(self.screen,(0,200,0),((0 * self.screen_block_width , 11 * self.screen_block_width),(6 * self.screen_block_width,1*self.screen_block_width)))

		pygame.draw.rect(self.screen,(0,0,200),((6 * self.screen_block_width , 11 * self.screen_block_width),(5 * self.screen_block_width,1*self.screen_block_width)))

		pygame.draw.rect(self.screen,(0,0,100),((0 * self.screen_block_width , 12 * self.screen_block_width),(11 * self.screen_block_width,1*self.screen_block_width)))

		self.render("stair_up",0,15)

		self.render("stair_down",0,16)

		self.screen.blit(notice, (11 * self.screen_block_width, 0 * self.screen_block_width + 8))

		self.screen.blit(notice1, (11 * self.screen_block_width, 1 * self.screen_block_width + 8))

		self.screen.blit(notice2, (2 * self.screen_block_width, 11 * self.screen_block_width + 8))

		self.screen.blit(notice3, (8 * self.screen_block_width, 11 * self.screen_block_width + 8))

		console_msg = TEXT.render("console:  " + self.console_msg,0,(255,255,255))

		self.screen.blit(console_msg, (0 * self.screen_block_width, 12 * self.screen_block_width + 8))


		pointer = [2,11]

		for file in VISUAL.object:

			surface = VISUAL.object[file]

			self.GetEditorItemByPos[str(pointer)] = file

			self.render(surface,pointer[0],pointer[1])

			pointer[1] += 1

			if pointer[1] >= self.screen_column:

				pointer[1] -= self.screen_column - self.map_column

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

					if event.button == 2 and col <= self.map_column - 1 and row <= self.map_row - 1:

						try:

							select = self.floor_item[self.floor_index][str([row,col])]

							self.console_msg = "clean " + select

							del self.floor_item[self.floor_index][
							   str([row,col])
							]

						except:

							pass

					if event.button == 1:

						if col <= self.map_column - 1 and row <= self.map_row - 1:

							if self.pickup != None:

								self.console_msg = 'put ' + self.pickup + " on " + str([row,col])

								try:

									origin_pickup = self.floor_item[self.floor_index][str([row, col])]

									self.console_msg = 'replace '+ origin_pickup + " to "+ self.pickup

									del self.floor_item[self.floor_index][
									 str([row,col])
								     ]

								except:

									pass


								self.floor_item[self.floor_index][
									str([row,col])
								] = self.pickup

						if col >= 11 and col <= self.screen_column :

							try:

								self.pickup = self.GetEditorItemByPos[str([row, col])]

								self.pickup_img = VISUAL.object[self.pickup]

								self.console_msg = 'pick up:'+self.pickup

							except:

								pass

						if col <= 5 and row == 11:


							with open("floor/floor.json",'w') as f:

								f.write(json.dumps(self.floor_item))

							self.console_msg = 'save successfully'

						if col >= 6 and col <= 10 and row == 11:

							self.floor_item[self.floor_index] = {}

							self.console_msg = 'clear successfully'

					if event.button == 3:

						self.pickup = None

						self.pickup_img = None


					if col == 15 and row == 0:

						self.floor_index += 1

						self.console_msg = "switch follor to " + str(self.floor_index)

						if self.floor_index >= len(self.floor_item.keys()):

							self.floor_item[self.floor_index] = {}

					if col == 16 and row == 0:

						self.floor_index -= 1

						self.console_msg = "switch follor to " + str(self.floor_index)

						self.floor_index = max(0,self.floor_index)

				if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
					sys.exit()

			pygame.display.update()


screen = VISUAL()
screen.run()