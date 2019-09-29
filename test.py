from copy import copy,deepcopy
class A:
	def __init__(self,name):
		self.name = name
	def get(self):
		return 1
a = [A(1),A(2)]
b = object.__new__(A)
print(b.get())