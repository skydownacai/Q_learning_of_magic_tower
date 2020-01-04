
from MagicTowerItems import *

class game:


	def __init__(self):

		self.obj = []

		self.obj_counter = dict([ typeobj, 0] for typeobj in TypeObj)


	def Constructor(self,map_file : OBJ):

		'''

		传入一个地图文件
		:param object_class:
		:return:

		'''


A = game()

A.Constructor(骷髅人)

print(A.obj[0])