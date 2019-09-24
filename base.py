class invalid_object(Exception):
	def __init__(self,error = None):
		print('Invalid Object!')
		if error == 0:
			print("Please specific the type of the object")
class invalid_attribution(Exception):
	def __init__(self):
		print("This Object doesn't have this attribution!")
class type_error(Exception):
	def __init__(self,info):
		print(info)
class value_error(Exception):
	def __init__(self,info):
		print(info)
class Object:
	type_of_str = {

		0 : "monster",
		1 : "npc",
		2 : "store",
		4 : "enviro_item",
		3 : "bonus",
		5 : "warrior"

	}

	count = {
		"monster" :0,
		"bonus": 0,
		'enviro_item':0,
		'npc':0,
		'store':0,
	}

	index = {

	}

	def __getattr__(self, key):
		'''valid attr:
			- name (str) : the name of object
			- type (int) : the type of object ,eg : 0. monster , 1 npc 2 store 3.bonus_item(eg. a key that you can pick up as a reward) 4 enviro_item (eg.a door)  5.warrior
				exclusive attr with each type of object:
					type 0 & 5:
						1. health
						2. attack
						3. defence
					type 3 :
					    1. bonus
					    2. bonus_value
					type 5 :
						1. gold
						2. status (the combine information of health,attack,defense,gold,postion)

			- interact_prerequiresite (instanse of object) : eg: your need a yellow key
			- as_prerequiresite_to (instanse of object) : eg , only your can fight with this object that you can get into the next floor
			- interact_actions (instanses of action):  the actions that you can interact with this object
				eg. if you interact with the store(in other word the type of object equals 2), your can choose the actions as follows:
					1. buy health
					2. buy attack
					3. buy defense
			- hidden_actions (instanses of action): the actions that you don't know only after you have interacted with it
				eg. you know that can buy 5 yellow keys at the expense of 50 gold after you have talked to the npc
		'''
		self.checkattr(key)
		return self.__dict__[key]
	def __setattr__(self, key, value):
		self.checkattr(key,value)
		self.__dict__[key] = value
	def __setitem__(self, key, value):
		self.__setattr__(key,value)
	def __getitem__(self, item):
		return self.__getattr__(item)
	@property
	def interact_prerequiresite(self):
		if '_interact_prerequiresite' not in self.__dict__:
			self._interact_prerequiresite = NullObject()
		return self._interact_prerequiresite
	@interact_prerequiresite.setter
	def interact_prerequiresite(self,value):
		self._interact_prerequiresite = value
	@property
	def as_prerequiresite_to(self):
		if '_as_prerequiresite_to' not in self.__dict__:
			self._as_prerequiresite_to = NullObject()
		return self._as_prerequiresite_to
	@as_prerequiresite_to.setter
	def as_prerequiresite_to(self,value):
		self._as_prerequiresite_to = value
	@property
	def TYPE(self):
		return Object.type_of_str[self.type]
	def __str__(self):
		return self.info
	def checkattr(self,key,value = None):
		if key in ['health','attack','defence','gold'] and (value != None and not isinstance(value,int)):
			raise type_error("Must Be Int")
		if key in ['health','attack','defence'] and self.type not in [0,5]:
			raise  invalid_attribution()
		if key in ['bonus_name','bonus_value'] and self.type != 3:
			raise  invalid_attribution()
		if key  in ['_interact_prerequiresite','_as_prerequiresite_to']:
			if not isinstance(value,Object):
				raise  type_error("The value for attr <<interact_prerequiresite>> and <<as_prerequiresite_to>> must be the instance of Object Rather than the instance of {}".format(type(value)))
			if type == 5:
				raise  invalid_attribution()
	def add_action(self,action):
		if not isinstance(action,Action):
				raise type_error("If you want to add a action to a object. The action must be the instance of the class Action")
		self.interact_actions.append(action)
	def delete_action(self,action):
		if not isinstance(action,Action):
				raise type_error("If you want to add a action to a object. The action must be the instance of the class Action")
		self.interact_actions.pop(self.interact_actions.index(action))
		print("The object : {} no longer have the action: ".format(action.name))

	@property
	def info(self):
		if self.TYPE == 'monster':
			return 'Monster :' + self.name + ': Health :' + str(self.health) + " Attack : " + str(
				self.attack) + " Defense : " + str(self.defense) + " gold : " + str(
				self.gold) + "\nActions:\n" + ';'.join([action.info for action in self.interact_actions])
		if self.TYPE == 'bonus':
			info = "Item : {}: \nactions:\n".format(self.name)
			for action in self.interact_actions:
				info += "	" + action.name + "\n"
			return info
		if self.TYPE == "store":
			info = "This is a store : \n"
			for action in self.interact_actions:
				info += "<Action " + str(self.interact_actions.index(action)) + "> : " + action.info + "\n"
			return  info
		if self.TYPE == 'warrior':
			return str(self.__dict__)

		if self.TYPE == 'enviro_item':
			info = "item : {}\n".format(self.name)
			for action in self.interact_actions:
				info += "<Action " + str(self.interact_actions.index(action)) + "> : " + action.info + "\n"
			return info

		if self.TYPE == 'npc':
			info = "npc : {}\n".format(self.name)
			for action in self.interact_actions:
				info += "<Action " + str(self.interact_actions.index(action)) + "> : " + action.info + "\n"
			return info
	def show(self):
		print(self.__dict__)


class World:

	warrior = None

	def __init__(self):
		self.items = []


	def add(self,item : Object,floor : int):
		'add a object to the world at the floor'
		item.floor = floor
		self.items.append(item)

	@property
	def state(self):
		'''当前'''
		return

	def reward(self,action):
		''''''
		return
	def run_warrior(self,strategy_func = None):
		if World.warrior == None:
			raise value_error("Please Try to run <World.warrior = > to specific a warrior to the World.")
		if strategy_func == None:
			raise value_error("Please add a strategy to the warrior to let the warrior know when he faces the state how he act to")

		while True:
			action = strategy_func(self.state)
 			reward = self.reward(action)

	@staticmethod
	def object_added(__init__):
		def inner(*args):
			__init__(*args)
			instance = args[0]
			instance.code = Object.count[instance.TYPE]
			Object.count[instance.TYPE] += 1
			instance.name = instance.name + "(" + str(instance.code) + ")"
			if instance.TYPE == 'bonus':
				instance.interact_actions = [PickBonus(instance.bonus_name,instance.bonus_value,instance.name)]
		return inner



class Action:
	@property
	def interactor(self):
		try:
			return Action.actor
		except:
			raise value_error("You haven't specific a warrior to interact.Try: Action.interactor = ")
	@interactor.setter
	def interactor(self,value):
		if not isinstance(value,Warrior):
			raise type_error("The interactor must be the instance of Warrior!")
		Action.actor = value
	def act(self,callback = None,callback_args = None):
		self.interact()
		if callback != None:
			if callback_args != None:
				callback(callback_args)
			else:
				callback()
	def __str__(self):
		return self.name
class NullObject(Object):
	def __init__(self):
		self.name = "Void object"
		self.info = "Void Object"
class Warrior(Object):

	def __init__(self,name,health,defense,gold,attack,start_floor = 1,yellow_key = 0,blue_key = 0,red_key = 0,strategy_f = None):
		self.name = name
		self.strategy = strategy_f
		self.type = 5
		self.health = health
		self.defense = defense
		self.attack = attack
		self.gold = gold
		self.yellow_key = yellow_key
		self.blue_key = blue_key
		self.red_key = red_key
		self.facing_object = []  #the object that you can immediately to interact with
	@property
	def status(self):
		keys = ['name','health','attack','defense','gold','yellow_key','blue_key','red_key']
		_status = {}
		for key in keys:
			_status[key] = self[key]
		return _status
class Store(Object):

	@World.object_added
	def __init__(self,Buyactions,interact_prerequiresite = NullObject()):
		self.name = "Store"
		self.type = 2
		self.interact_prerequiresite = interact_prerequiresite
		self.interact_actions = Buyactions

class Monster(Object):

	def init(self):
		pass

	@World.object_added
	def __init__(self):
		self.type = 0
		self.init() #在这里自定义
		self.interact_actions = [Fight(self)]
	def fight(self):
		self.interact_actions[0].interact()

class Enviro_item(Object):


	@World.object_added
	def __init__(self):
		self.type = 4
		self.init()
		self.status = 0 #status = 0 表明还未进行互动 status = 1 表明已经互动过

	def act(self):
		self.interact_actions[0].interact()

class Npc(Object):

	@staticmethod
	def baseinit(__init__):
		def inner(*args,**kwarg):
			__init__(*args)
			instance = args[0]
			instance.type = 1
			instance.staus = 0
		return inner
	def act(self):
		self.interact_actions[0].interact()

class 骷髅人(Monster):
	def init(self):
		self.name = "骷髅人"
		self.attack = 42
		self.defense = 6
		self.gold = 6
		self.health = 50
class 骷髅士兵(Monster):
	def init(self):
		self.name = "骷髅士兵"
		self.attack = 52
		self.defense = 12
		self.gold = 8
		self.health = 55
class 小蝙蝠(Monster):
	def init(self):
		self.name = "小蝙蝠"
		self.attack = 38
		self.defense = 3
		self.gold = 3
		self.health = 35
class 初级法师(Monster):
	def init(self):
		self.name = "初级法师"
		self.attack = 32
		self.defense = 8
		self.gold = 5
		self.health = 60
class 绿色史莱姆(Monster):
	def init(self):
		self.name = "绿色史莱姆"
		self.attack = 18
		self.defense = 1
		self.gold = 1
		self.health = 35
class 红色史莱姆(Monster):
	def init(self):
		self.name = "红色史莱姆"
		self.attack = 20
		self.defense = 2
		self.gold = 2
		self.health = 45
class 初级士兵(Monster):
	def init(self):
		self.name = "初级士兵"
		self.attack = 48
		self.defense = 22
		self.health = 50

class Bonus_Item(Object):
	@World.object_added
	def __init__(self):
		'''
		bonus_name:收益加成的属性名成
		value : 加成
		'''
		self.type = 3
		self.init()
	def pick(self):
		self.interact_actions[0].interact()

class yellow_key(Bonus_Item):
	def init(self):
		self.bonus_name = 'yellow_key'
		self.name = self.bonus_name
		self.bonus_value = 1
class blue_key(Bonus_Item):
	def init(self):
		self.bonus_name = 'blue_key'
		self.name = self.bonus_name
		self.bonus_value = 1
class red_key(Bonus_Item):
	def init(self):
		self.bonus_name = 'red_key'
		self.name = self.bonus_name
		self.bonus_value = 1
class Health50(Bonus_Item):
	def init(self):
		self.name = "Health50up"
		self.bonus_name = 'health'
		self.bonus_value = 50
class Health100(Bonus_Item):
	def init(self):
		self.name = "Health100up"
		self.bonus_name = 'health'
		self.bonus_value = 100
class Health200(Bonus_Item):
	def init(self):
		self.name = "Health200up"
		self.bonus_name = 'health'
		self.bonus_value = 200
class Health400(Bonus_Item):
	def init(self):
		self.name = "Health400up"
		self.bonus_name = 'health'
		self.bonus_value = 400

class yellow_door(Enviro_item):
	def init(self):
		self.color = 'yellow'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_key"
		self.interact_actions = [Open(self)]
class blue_door(Enviro_item):
	def init(self):
		self.color = 'blue'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_key"
		self.interact_actions = [Open(self)]
class red_door(Enviro_item):
	def init(self):
		self.color = 'red'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_key"
		self.interact_actions = [Open(self)]

class merchant(Npc):

	@World.object_added
	@Npc.baseinit
	def __init__(self,BuyAction):
		if isinstance(BuyAction,list) == False:
			raise  type_error("merchant only have one buy action")
		self.name = "merchant"
		self.interact_actions = [BuyAction]

class talker(Npc):

	@World.object_added
	@Npc.baseinit
	def __init__(self,UnlockHiddenEvent):
		self.name = "A talker"
		self.interact_actions = [UnlockHiddenAction(UnlockHiddenEvent['TargetObject'],UnlockHiddenEvent['TargetAction'])]

class Bonus(Action):
	'''
	带有奖励效益类的action
	'''
	def __init__(self,bonus,bonus_value,itemname = None):
		#code 是 物品的 id
		self.bonus = bonus
		self.bonus_value = bonus_value
		self.itemname = itemname
		try:
			self.init()
		except:
			pass
	@property
	def bonus(self):
		return self._bonus
	@bonus.setter
	def bonus(self,value):
		if value not in ['health','attack','defense','yellow_key','blue_key','red_key']:
			raise value_error("Invalid Bonus")
		self._bonus = value
	@property
	def bonus_value(self):
		return self._bonus_value
	@bonus_value.setter
	def bonus_value(self,value):
		if not isinstance(value,int):
			raise type_error("The type of expense must be int!")
		self._bonus_value = value
class Buy(Bonus):
	@property
	def expense(self):
		return self._expense
	@expense.setter
	def expense(self,value):
		if not isinstance(value,int):
			raise type_error("The type of expense must be int!")
		self._expense = value
	def interact(self):
		self.interactor[self.bonus] += self.bonus_value
		self.interactor.gold  -= self.expense
class PickBonus(Bonus):
	def init(self):
		self.name = 'Pick ' + " {} ".format(self.itemname)
		self.info = 'Pick ' + str(self.bonus_value)+" "+self.bonus
	def interact(self):
		self.interactor[self.bonus] += self.bonus_value
class BuyHealth(Buy):
	def __init__(self,bonus_value,expense):
		self.name = "BuyHealth"
		self.bonus_value = bonus_value
		self.bonus = "health"
		self.expense = expense
		self.info = "Buy {} Health  at the expense of {} gold".format(self.bonus_value,self.expense)
class BuyAttack(Buy):
	def __init__(self,bonus_value,expense):
		self.name = "BuyAttack"
		self.bonus = "attack"
		self.bonus_value = bonus_value
		self.expense = expense
		self.info = "Buy {} Attack  at the expense of {} gold".format(self.bonus_value,self.expense)
class BuyDefense(Buy):
	def __init__(self,bonus_value,expense):
		self.name = "BuyDefense"
		self.bonus = "defense"
		self.bonus_value = bonus_value
		self.expense = expense
		self.info = "Buy {} Defense at the expense of {} gold".format(self.bonus_value,self.expense)
class Fight(Action):
	'''fight类'''
	def __init__(self,fight_with : Object):
		self.fight_with = fight_with
		self.name = 'fight vs '+ self.fight_with.name
	def update_fight_value(self):

		self.attack_time = int(self.fight_with.health / (Action.interactor.attack - self.fight_with.defense))
		self.loss_life = self.attack_time * (self.fight_with.attack - self.interactor.defense)
		self.margin_attack_of_life =  [int(self.fight_with.health / (self.interactor.attack + i - self.fight_with.defense))  * (self.fight_with.attack - self.interactor.defense) - self.loss_life for i in range(1,6)]
		self.margin_defense_of_life = [int(self.fight_with.health / (self.interactor.attack - self.fight_with.defense)) * (self.fight_with.attack - self.interactor.defense - i) - self.loss_life for i in range(1,6)]
	def fightavalibe(self):
		'''判断勇士与这个怪物是否能打架'''
		self.update_fight_value()
		if self.loss_life >= Action.interactor.health:
			return False
		else:
			return True
	def interact(self):
		self.update_fight_value()
		self.interactor.gold += self.fight_with.gold
		self.interactor.health -= self.loss_life
	@property
	def info(self):
		self.update_fight_value()
		return 'Fight with the monster( {} HP↓, {} GOLD ↑)'.format(self.loss_life,self.fight_with.gold)
class Open(Action):
	def __init__(self,door:Object):
		self.door = door
		self.key_need = door.key_need
		self.info = "Open the door (need : {})".format(self.key_need)
	def open_avaliable(self):
		if self.interactor[self.key_need] > 0:
			return True
		else:
			return False
	def interact(self):
		self.interactor[self.key_need] -= 1
class UnlockHiddenAction(Action):
	def __init__(self,TargetObject:Object,TargetAction :Action):
		self.TargetObject = TargetObject
		self.TargetAction = TargetAction
		self.info = TargetObject.name + " now can : " + TargetAction.info

	def interact(self):
		self.TargetObject.add_action(self.TargetAction)

#b = Warrior(name='skydownacai',health=100,attack=10,defense=10,gold=6)

b = talker({"TargetObject":yellow_key(),'TargetAction':BuyAttack(100,100)})
c = merchant([BuyAttack(100,100)])

print(b)