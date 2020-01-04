from ActionsAndObjects import *

class 骷髅人(Monster):

	def __init__(self):

		super().__init__(name = "骷髅人",health = 50,attack = 42, defense = 6, gold = 6)

class 骷髅士兵(Monster):

	def __init__(self):

		super().__init__(name = "骷髅士兵",health = 55,attack = 52, defense = 12, gold = 8)

class 小蝙蝠(Monster):

	def __init__(self):

		super().__init__(name = "小蝙蝠",health = 35,attack = 38, defense = 3, gold = 3)

class 初级法师(Monster):
	def __init__(self):

		super().__init__(name = "初级法师",health = 60,attack = 32, defense = 8, gold = 5)

class 绿色史莱姆(Monster):
	def __init__(self):

		super().__init__(name = "绿色史莱姆",health = 35,attack = 18, defense = 1, gold = 1)

class 红色史莱姆(Monster):
	def __init__(self):

		super().__init__(name = "红色史莱姆",health = 45,attack = 20, defense = 2, gold = 2)

class 初级士兵(Monster):
	def __init__(self):

		super().__init__(name = "初级士兵",health = 48,attack = 48, defense = 22, gold = 20)

class yellow_key(Bonus_Item):

	def __init__(self):

		super().__init__(name = "yellow_key", bonus = "yellow_key",bonus_value = 1)

class blue_key(Bonus_Item):

	def __init__(self):

		super().__init__(name="blue_key", bonus="blue_key", bonus_value=1)

class red_key(Bonus_Item):

	def __init__(self):

		super().__init__(name="red_key", bonus="red_key", bonus_value=1)


class health50(Bonus_Item):

	def __init__(self):
		super().__init__(name="50health", bonus="health", bonus_value=50)

class health100(Bonus_Item):

	def __init__(self):
		super().__init__(name="100health", bonus="health", bonus_value=100)
class health200(Bonus_Item):

	def __init__(self):
		super().__init__(name="200health", bonus="health", bonus_value=200)
class health400(Bonus_Item):

	def __init__(self):
		super().__init__(name="400health", bonus="health", bonus_value=400)

class oneattackup(Bonus_Item):
	def __init__(self):
		super().__init__(name="1attack", bonus="attack", bonus_value=1)

class twoattackup(Bonus_Item):
	def __init__(self):
		super().__init__(name="2attack", bonus="attack", bonus_value=2)

class sword(Bonus_Item):

	def __init__(self):
		super().__init__(name="sword", bonus="attack", bonus_value=10)

class sheld(Bonus_Item):

	def __init__(self):
		super().__init__(name="sheld", bonus="defense", bonus_value=10)

class onedefenseup(Bonus_Item):

	def __init__(self):
		super().__init__(name="1defense", bonus="defense", bonus_value=1)


class twodefenseup(Bonus_Item):
	def __init__(self):

		super().__init__(name="2defense", bonus="defense", bonus_value=2)

class yellow_door(Door):

	def __init__(self):

		self.color = 'yellow'

		self.key_need =self.color+ "_key"

		super().__init__(name = self.color + "_door")

class blue_door(Door):

	def __init__(self):
		self.color = 'blue'

		self.key_need = self.color + "_key"

		super().__init__(name=self.color + "_door")

class red_door(Door):

	def __init__(self):
		self.color = 'yellow'

		self.key_need = self.color + "_key"

		super().__init__(name=self.color + "_door")
