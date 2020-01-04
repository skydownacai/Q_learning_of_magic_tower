
from errors import  *

from MagicTowerConstants import *

class OBJ:

	def __init__(self,name : str,type : TypeObj ,actions = []):

		self.name = name

		self.type = type

		self.actions = actions

		self._info = "No related infomation"


	def __str__(self):

		return self.info

	@property
	def info(self):

		type = self.type

		if type == TypeObj.Monster:

			self._info = 'Monster :' + self.name + ': Health :' + str(self.health) + " Attack : " + str(

				self.attack) + " Defense : " + str(self.defense) + " gold : " + str(

				self.gold) + "\nActions:\n" + ';'.join([action.info for action in self.actions])

		if type == TypeObj.Bonus:

			info = "Item : {}: \nactions:\n".format(self.name)

			for action in self.actions:
				info += " " + str(action) + "\n"

			self._info = info

		if type == TypeObj.Store:

			info = "This is a store : \n"

			for action in self.actions:
				info += "<Action " + str(self.actions.index(action)) + "> : " + action.info + "\n"

			self._info = info

		if type == TypeObj.Warrior:

			self._info = str(self.__dict__)

		if type == TypeObj.Enviro_Item:

			info = "item : {}\n".format(self.name)

			for action in self.actions:

				info += "<Action " + str(self.actions.index(action)) + "> : " + action.info + "\n"

			self._info = info

		if type == TypeObj.Npc:

			info = "npc : {}\n".format(self.name)

			for action in self.actions:

				info += "<Action " + str(self.actions.index(action)) + "> : " + action.info + "\n"

			self._info = info

		return self._info

	def __getattr__(self, key):

		try:

			return self.__dict__[key]

		except:

			raise AttributeError("Theres No attribution of item named '%s'"%key)

	def __getitem__(self, item):

		return self.__getattr__(item)

	def __setattr__(self, key, value):

		self.__dict__[key] = value

	def __setitem__(self, key, value):

		self.__setattr__(key,value)

class Action:

	Warrior = None

	def __init__(self,name, bind_obj : OBJ):
		'''
		:param name: action的name
		:param bind_obj: 实施action的obj
		'''

		self.name = name

		self.bind_obj = bind_obj

		self._reward = {}


		if Action.Warrior == None:

			raise NoWarrior

	def act(self,callback = None,callback_args = None):

		self.interact()

		if callback != None:

			if callback_args != None:

				callback(callback_args)

			else:
				callback()

	@property
	def rewards(self):
		'''
		实施这个action 对 warrior

		:return:
		'''
		return self._rewards

	def __str__(self):

		return repr(self.info)

	@property
	def info(self):

		return self.name

class Fight(Action):

	'''fight类'''

	def __init__(self,bind_obj : OBJ):

		if isinstance(bind_obj,Monster) == False:

			raise  value_error("You must bind action : Fight on Monster instance")

		super().__init__(name = "Fight vs "+ bind_obj.name, bind_obj = bind_obj)

	def update_fight_value(self):

		if Action.Warrior.attack > self.bind_obj.defense:

			self.attack_time = int(self.bind_obj.health / (Action.Warrior.attack - self.bind_obj.defense))

			self.loss_life = self.attack_time * (self.bind_obj.attack - Action.Warrior.defense)

		else:

			self.loss_life = \
				100000000
		#self.margin_attack_of_life =  [int(self.fight_with.health / (self.interactor.attack + i - self.fight_with.defense))  * (self.fight_with.attack - self.interactor.defense) - self.loss_life for i in range(1,6)]
		#self.margin_defense_of_life = [int(self.fight_with.health / (self.interactor.attack - self.fight_with.defense)) * (self.fight_with.attack - self.interactor.defense - i) - self.loss_life for i in range(1,6)]

	def fightavalibe(self):
		'''判断勇士与这个怪物是否能打架'''
		self.update_fight_value()
		if self.loss_life >= Action.Warrior.health:
			return False
		else:
			return True

	def interact(self):

		self.update_fight_value()

		Action.Warrior.gold += self.bind_obj.gold

		Action.Warrior.health -= self.loss_life

	@property
	def info(self):

		self.update_fight_value()

		return 'Fight with the monster( {} HP↓, {} GOLD ↑)'.format(self.loss_life,self.bind_obj.gold)

	@property
	def rewards(self):

		self.update_fight_value()

		return [

			{'attr':'health', 'value': -1 * self.loss_life},

			{'attr':'gold'  , 'value': self.bind_obj.gold}
		]


class PickBonus(Action):

	def __init__(self,bind_obj : OBJ):

		if not isinstance(bind_obj,Bonus_Item):

			raise value_error("bind_obj is not an instance of class Bouns_Item")

		super().__init__(name ='Pick' , bind_obj = bind_obj)

		self.bonus = self.bind_obj.bonus

		self.bonus_value = self.bind_obj.bonus_value

	@property
	def rewards(self):

		return [
			{'attr':self.bonus,'value':self.bonus_value}
		]

class Buy(Action):

	def __init__(self,bind_obj : OBJ , expense):

		self.expense = expense

		super().__init__(name = 'Buy {} {} of {} gold'.format(bind_obj.bonus_value,bind_obj.bonus,self.expense),bind_obj = bind_obj)

		if not isinstance(expense,int):

			raise type_error("The type of expense must be int!")

		if not isinstance(bind_obj,Bonus_Item):

			raise value_error("bind_obj is not an instance of class Bouns_Item")

	def interact(self):

		Action.Warrior[self.bind_obj.bonus] += self.bind_obj.bonus_value

		Action.Warrior.gold  -= self.expense

	@property
	def avaliable(self):

		if Action.Warrior.gold < self.expense:

			return False

		return True

	@property
	def rewards(self):

		return [

			{'attr':self.bind_obj.bonus,'value':self.bind_obj.bonus_value},

			{'attr':'gold','value': -1 * self.expense}
		]


class Open(Action):

	def __init__(self, bind_obj):

		if not isinstance(bind_obj,Door):

			raise value_error("bind_obj is not an instance of class Bouns_Item")

		super().__init__(name="Open door :{}".format(bind_obj.name), bind_obj = bind_obj)


	@property
	def info(self):


		if not self.avaliable:

			return  self.name + " (not avaliable now)"

		else:

			return self.name + " (avaliable now)"

	@property
	def avaliable(self):

		if Action.Warrior[self.bind_obj.key_need] > 0:

			return True

		else:

			return False

	@property
	def rewards(self):

		return [
			{'attr': self.bind_obj.key_need, 'value': -1},

		]


class NullObject(OBJ):

	def __init__(self):

		super().__init__(name = "Void object",type = "Void Object", action = [], act_prereq = [])

class Warrior(OBJ):


	def __init__(self,name,health,defense,gold,attack,yellow_key = 0,blue_key = 0,red_key = 0):

		super().__init__(name = name,type = "warrior",)

		self.health = health

		self.defense = defense

		self.attack = attack

		self.gold = gold

		self.yellow_key = yellow_key

		self.blue_key = blue_key

		self.red_key = red_key

	@property
	def status(self):
		'''
		:return: the status dict of warrior
		'''
		keys = ['name','health','attack','defense','gold','yellow_key','blue_key','red_key']

		return dict([key, self[key]] for key in keys)


class Monster(OBJ):

	def __init__(self,name,health,attack,defense,gold):

		super().__init__(name = name,type = TypeObj.Monster)

		self.actions = [Fight(bind_obj = self)]

		self.health = health

		self.attack = attack

		self.defense = defense

		self.gold = gold

	def fight(self):

		self.actions[0].interact()


class Bonus_Item(OBJ):


	def __init__(self,name,bonus,bonus_value):

		'''

		bonus_name:收益加成的属性名成

		bonus_value:收益加成值

		value : 加成

		'''

		self.name = name

		self.bonus = bonus

		self.bonus_value = bonus_value

		super().__init__(name = name,type = TypeObj.Bonus, actions = [PickBonus(bind_obj = self)])


	def pick(self):

		self.actions[0].interact()


class Door(OBJ):


	def __init__(self,name):

		super().__init__(name,type = TypeObj.Enviro_Item)

		self.staus = 1 # status 1 表明可互动 0 表明不可互动

		self.actions = [Open(bind_obj = self)]


class Store(OBJ):


	def __init__(self,name, goods: dict):
		'''

		:param name: name of this stoor

		:param goods: dict of <bonus item,expense>
		'''

		super().__init__(name = name, type= TypeObj.Store)

		self.actions = [

			Buy(good, goods[good] ) for good in goods

		]


class Npc(OBJ):


	def __init__(self,name):

		super().__init__(name = name,type = TypeObj.Npc)

	def interact(self):
		self.interact_actions[0].interact()

Action.Warrior = Warrior(name='skydownacai',health=300,attack=10,defense=10,gold=6,yellow_key=1) #指定warrior

