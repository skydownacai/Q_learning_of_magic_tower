import colorlog
import logging
import threading
from  strategy import *
import time
from copy import copy,deepcopy
class Log:
	def __init__(self):
		log_colors_config = {
			'DEBUG': 'bg_yellow',
			'INFO': 'bg_green',
			'WARNING': 'bg_red',
			'ERROR': 'bg_red',
			'CRITICAL': 'bg_red',
		}
		RESET_SEQ = "\033[0m"
		COLOR_SEQ = "\033[1;%dm"
		BOLD_SEQ = "\033[1m"

		'''
		self.filename = fileName
		self.logger = logging.getLogger("VeChain LJC")
		self.logger.setLevel(logging.DEBUG)
		'''
		self.logger = logging.getLogger("VeChain LJC")
		self.logger.setLevel(logging.DEBUG)
		self.consleformatter = colorlog.ColoredFormatter(
			   BOLD_SEQ+'\033[0m%(fg_black)s%(log_color)s%(levelname)-7s\033[0m'+'%(fg_cyan)s%(message)s',
			log_colors=log_colors_config)  # 日志输出格式
		# 创建一个StreamHandler,用于输出到控制台
		ch = colorlog.StreamHandler()
		ch.setLevel(logging.DEBUG)
		ch.setFormatter(self.consleformatter)
		self.logger.addHandler(ch)
	@property
	def debug(self):
		return self.logger.debug
	@property
	def info(self):
		return self.logger.info
	@property
	def warning(self):
		return self.logger.warning
	@property
	def error(self):
		return self.logger.error
	@property
	def critical(self):
		return self.logger.critical
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
class End_Game(Exception):
	def __init__(self):
		pass
class Death(Exception):
	def __init__(self):
		pass
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
		'warrior':0
	}
	total_count = 0
	index = {
	}
	add_object_to_world = None
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
		if key == "interact_prerequiresite":
			if not isinstance(value, Object) and  not isinstance(value,list):
				raise type_error("Must be the (list of) instance of Warrior!")

		if key == 'as_prerequiresite_to':
			if not isinstance(value,Object) and not isinstance(value,list):
				raise type_error("Must be the instance of object!")
		self.__dict__[key] = value
	def __setitem__(self, key, value):
		self.__setattr__(key,value)
	def __getitem__(self, item):
		return self.__getattr__(item)
	@property
	def TYPE(self):
		return Object.type_of_str[self.type]

	def __str__(self):
		return str(self.__dict__)
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
	def place(self,floor,row,column):
		'''把这个物体放到 第 floor 层的 第row行 column 列'''
		self.floor = floor
		self.row = row
		self.column = column
		return self
	def items_to_render(self):
		floor = {}
		for item in self.items:
			if item.floor not in floor:
				floor[item.floor] = []
			floor[item.floor].append([item.name[:item.name.index("(")],item.row,item.column])
class Action:

	def act(self,callback = None,callback_args = None):

		Object.add_object_to_world.log.debug("<Action> : {} ".format(self.name))

		self.interact()

		if callback != None:

			if callback_args != None:

				callback(callback_args)

			else:
				callback()
	@property
	def rewards(self):
		return self._rewards
	def __str__(self):
		return self.name
class World:
	log = Log()
	def __init__(self):
		self.items = []
		self._item = []
		self.event_hisotry = []

	def get_item(self, code):
		return self._item[code]

	def place(self, item: Object, floor: int):
		'place a object to the world at the floor'
		item.floor = floor
		self.items.append(item)

	def reward_and_update_world(self, object:Object , action :Action ,get_action_reward):
		''' 环境 对 action 给出reward'''
		action.act()

		rewards = action.rewards
		END = False
		for reward in rewards:
			self.log.debug("<Reward> : {} {}".format(reward['attr'],reward['value']))
			get_action_reward(reward)

		#self.log.debug("Now status : {}\n".format(Action.interactor.status))
		''' 执行一个action之后,更新状态'''
		'''如果这个object 是怪物,奖励物品,环境物品,那么这个物品会消失,并解说与其他
			type_of_str = {
			0 : "monster",
			1 : "npc",
			2 : "store",
			4 : "enviro_item",
			3 : "bonus",
			5 : "warrior"
			}
		'''

		if object.type in [0,3,4]:
			'''将这个object 移除状态 和 世界物品'''
			self.state.remove(object)
			self.map.remove(object)
			try:
				'''可视化里去掉这个object'''
				this_position = self.gui.position_to_str(object.row,object.column)
				del self.gui.floor[self.gui.floor_index][this_position]
			except:
				pass
			#print('object', object.name)

			'''这个object 消失后解锁了其他的object 可互动'''
			for item in object.as_prerequiresite_to:
				item.interact_prerequiresite = NullObject()
				if item not in self.map or item in self.state:
					pass
				else:
					self.state.append(item)

			#捡到一把钥匙后就可以打开更多的门
			if "key" in object.name and Action.interactor[object.bonus_name] == 1:
					for item in self.door_need_key:
						if item.key_need == object.bonus_name:
								self.state.append(item)
								self.door_need_key.remove(item)
			#print([item.name for item in self.state])
			#开了一个门，如果钥匙耗光了，那么本来能互动的门就不能互动
			if "door" in object.name and Action.interactor[object.key_need] == 0:
					for item in self.state[:]:
						if "door" in item.name and item.key_need == object.key_need:
							self.door_need_key.append(item)
							self.state.remove(item)
		self.state = list(sorted(self.state,key = lambda x:x.code)) # 姜
		if self.state == []:
			raise End_Game
		if Action.interactor.health <= 0:
			raise Death
	@property

	def History(self):
		return self.event_hisotry

	@property
	def warrior(self):
		return Action.interactor

	def create_world(self):
		#生成世界函数
		pass

	def reset(self):

		''' 重新 初始化 世界'''
		World.log.info("初始化世界中...")
		self.items = []
		Object.total_count = 0
		for type in Object.count:
			Object.count[type] = 0
		self.create_world()
		self.state = []
		self.event_hisotry = []
		self.door_need_key = []
		for item in self.items:
			if isinstance(item.interact_prerequiresite,NullObject) == False:
				if isinstance(item.interact_prerequiresite,list):
					for obj in item.interact_prerequiresite:
						obj.as_prerequiresite_to.append(item)
				if isinstance(item.interact_prerequiresite,Object):
						before = item.interact_prerequiresite
						before.as_prerequiresite_to.append(item)
				'''还不能直接互动的排除掉'''
				continue

			if 'door' in item.name and Action.interactor[item.key_need] == 0:
				'''如果当前有门可以直接互动,但是没有对应的钥匙的话也要排除'''

				self.door_need_key.append(item)
				continue

			self.state.append(item)
		self.map = self.items[:]
		World.log.info("初始化世界完毕中...")
		self.gui.floor_index = 0
		for key in self.warrior_info:
			Action.interactor[key]  = self.warrior_info[key]
		self.gui.init = True
	def run_warrior(self, strategy : Strategy = None):
		self.warrior_info = deepcopy(Action.interactor.__dict__)
		self.reset()

		if World.warrior == None:
			raise value_error("Please Try to run <World.warrior = > to specific a warrior to the World.")
		if strategy == None:
			raise value_error(
				"Please add a strategy to the warrior to let the warrior know when he faces the state how he act to")
		input("press any key to start")
		while True:
			try:
				stauts_values = Action.interactor.stauts_value
				state_encoded =  '_'.join(map(lambda x:str(x),stauts_values))
				state_encoded += "/"+'_'.join(map(lambda x:str(x.name),self.state))
				World.log.debug("Now state : "+state_encoded)
				(obj,action) = strategy.choose_action(self.state,state_encoded)
				self.event_hisotry.append((obj, action))
				try:
					render_action = threading.Thread(target=self.gui.go,args=(obj,))
					render_action.start()
					render_action.join()
				except:
					pass
				self.reward_and_update_world(obj,action,strategy.actionreward)
				time.sleep(0.2)
			except End_Game:
				World.log.info("Game Over!")
				self.reset()
				exit()
			except Death:
				World.log.info("You died!")
				self.reset()

	@staticmethod
	def object_added(__init__):
		def inner(*args,**kwargs):
			__init__(*args,**kwargs)
			instance = args[0]
			instance.code = Object.total_count
			Object.total_count += 1
			Object.count[instance.TYPE] += 1
			if instance.name in ['200healthup','400healthup']:
				instance.icon = "bighealthup"
			elif instance.name in ['50healthup','100healthup']:
				instance.icon = "bighealthup"
			elif instance.name in ['attackup']:
				instance.icon = "attackup"
			elif instance.name in ['defenseup']:
				instance.icon = "defenseup"
			else:
				instance.icon = instance.name
			instance.name = instance.name + "(" + str(instance.code) + ")"
			if "door" in instance.name:
				instance.interact_actions = [Open(instance)]
			if instance.TYPE == 'bonus':
				instance.interact_actions = [PickBonus(instance.bonus_name, instance.bonus_value, instance.name)]
			if instance.TYPE == 'monster':
				instance.interact_actions = [Fight(instance)]
			if Object.add_object_to_world != None:
				Object.add_object_to_world.items.append(instance)
			if 'interact_prerequiresite' not in instance.__dict__:
				instance.interact_prerequiresite = NullObject()
			if 'as_prerequiresite_to' not in instance.__dict__:
				instance.as_prerequiresite_to = []
			World.log.debug("创建Object:" + instance.name)
			if not isinstance(instance.interact_prerequiresite, NullObject):
				if isinstance(instance.interact_prerequiresite,Object):
					World.log.debug("添加Object Action 关系: " + instance.name + " -> " + instance.interact_prerequiresite.name)
				if isinstance(instance.interact_prerequiresite, list):
					for item in instance.interact_prerequiresite:
						Object.add_object_to_world.log.debug(
							"添加Object Action 关系: " + instance.name + " -> " + item.name)
		return inner
	@staticmethod
	def add_relationship(func):
		def inner(*args):
			instance = args[0]
			object = args[1]
			func(*args)
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
		self.icon = "facedown"
	@property
	def status(self):
		keys = ['name','health','attack','defense','gold','yellow_key','blue_key','red_key']
		_status = {}
		for key in keys:
			_status[key] = self[key]
		return _status
	@property
	def stauts_value(self):
		keys = ['health','attack','defense','gold','yellow_key','blue_key','red_key']
		values = []
		for key in keys:
			values.append(self[key])
		return values
class Store(Object):

	@World.object_added
	def __init__(self,Buyactions,interact_prerequiresite = NullObject()):
		self.name = "Store"
		self.type = 2
		self.interact_prerequiresite = interact_prerequiresite
		self.interact_actions = Buyactions
		for action in self.interact_actions:
			action.Store_To_Buy = self

class Monster(Object):

	def init(self):
		pass

	@World.object_added
	def __init__(self,interact_prerequiresite = NullObject()):
		self.type = 0
		self.init() #在这里自定义
		self.interact_prerequiresite = interact_prerequiresite

	def fight(self):
		self.interact_actions[0].interact()
class Enviro_item(Object):


	@World.object_added
	def __init__(self,interact_prerequiresite = NullObject()):

		self.type = 4
		self.init()
		self.status = 0 #status = 0 表明还未进行互动 status = 1 表明已经互动过
		self.interact_prerequiresite = interact_prerequiresite
	def interact(self):

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
	def interact(self):

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
	def __init__(self,interact_prerequiresite = NullObject()):
		'''
		bonus_name:收益加成的属性名成
		value : 加成
		'''
		self.type = 3
		self.init()
		self.interact_prerequiresite = interact_prerequiresite
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
class health50(Bonus_Item):
	def init(self):
		self.name = "50healthup"
		self.bonus_name = 'health'
		self.bonus_value = 50
class health100(Bonus_Item):
	def init(self):
		self.name = "100healthup"
		self.bonus_name = 'health'
		self.bonus_value = 100
class health200(Bonus_Item):
	def init(self):
		self.name = "200healthup"
		self.bonus_name = 'health'
		self.bonus_value = 200
class health400(Bonus_Item):
	def init(self):
		self.name = "400healthup"
		self.bonus_name = 'health'
		self.bonus_value = 400
class oneattackup(Bonus_Item):
	def init(self):
		self.name = "1attackup"
		self.bonus_name = 'attack'
		self.bonus_value = 1
class twoattackup(Bonus_Item):
	def init(self):
		self.name = "2attackup"
		self.bonus_name = 'attack'
		self.bonus_value = 2
class sword(Bonus_Item):
	def init(self):
		self.name = "sword"
		self.bonus_name = 'attack'
		self.bonus_value = 10
class sheld(Bonus_Item):
	def init(self):
		self.name = "sword"
		self.bonus_name = 'defense'
		self.bonus_value = 10
class onedefenseup(Bonus_Item):
	def init(self):
		self.name = "1defenseup"
		self.bonus_name = 'defense'
		self.bonus_value = 1
class twodefenseup(Bonus_Item):
	def init(self):
		self.name = "2defenseup"
		self.bonus_name = 'defense'
		self.bonus_value = 2
class yellow_door(Enviro_item):
	def init(self):
		self.color = 'yellow'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_door"
class blue_door(Enviro_item):
	def init(self):
		self.color = 'blue'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_door"

class red_door(Enviro_item):
	def init(self):
		self.color = 'red'
		self.key_need =self.color+ "_key"
		self.name = self.color + "_door"

class merchant(Npc):

	@World.object_added

	@Npc.baseinit

	def __init__(self,BuyAction,interact_prerequiresite = NullObject()):
		if isinstance(BuyAction,list) == False:
			raise  type_error("BuyAction must be type of list")
		self.name = "merchant"
		self.interact_actions = BuyAction
		self.interact_prerequiresite = interact_prerequiresite

class talker(Npc):

	@World.object_added
	@Npc.baseinit
	def __init__(self,UnlockHiddenEvent,interact_prerequiresite = NullObject()):
		self.name = "talker"
		self.interact_actions = [UnlockHiddenAction(UnlockHiddenEvent['TargetObject'],UnlockHiddenEvent['TargetAction'])]
		self.interact_prerequiresite = interact_prerequiresite

class Bonus(Action):
	'''
	带有奖励效益类的action
	'''
	def __init__(self,bonus,bonus_value,itemname = None):
		#code 是 物品的 id
		self.bonus = bonus
		self.bonus_value = bonus_value
		self.itemname = itemname
		self.init()
	def init(self):
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

	def avaliable(self):
		if self.interactor.gold < self.expense:
			return False
		return True

	@property
	def Store_To_Buy(self):
		return self._Store_To_Buy

	@Store_To_Buy.setter
	def Store_To_Buy(self,store:Store):
		if isinstance(store,Store) == False:
			raise TypeError("The Store To Buy must be the instance of Store")
		self._Store_To_Buy = store

	@property
	def name(self):
		return 'Buy {} {} of {} gold At {}'.format(self.bonus_value,self.bonus,self.expense,self.Store_To_Buy.name)

	@property
	def rewards(self):
		return [
			{'attr':self.bonus,'value':self.bonus_value},
			{'attr':'gold','value': -1 * self.expense}
		]
class PickBonus(Bonus):

	def init(self):
		self.name = 'Pick ' + " {} ".format(self.itemname)
		self.info = 'Pick ' + str(self.bonus_value)+" "+self.bonus
	def interact(self):
		self.interactor[self.bonus] += self.bonus_value
	@property
	def rewards(self):
		return [
			{'attr':self.bonus,'value':self.bonus_value}
		]
class BuyHealth(Buy):
	def __init__(self,bonus_value,expense):
		self.bonus_value = bonus_value
		self.bonus = "health"
		self.expense = expense
		self.info = "Buy {} Health  at the expense of {} gold".format(self.bonus_value,self.expense)
class BuyAttack(Buy):
	def __init__(self,bonus_value,expense):
		self.bonus = "attack"
		self.bonus_value = bonus_value
		self.expense = expense
		self.info = "Buy {} Attack  at the expense of {} gold".format(self.bonus_value,self.expense)
class BuyDefense(Buy):
	def __init__(self,bonus_value,expense):
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

		if Action.interactor.attack > self.fight_with.defense:

			self.attack_time = int(self.fight_with.health / (Action.interactor.attack - self.fight_with.defense))

			self.loss_life = self.attack_time * (self.fight_with.attack - self.interactor.defense)

		else:

			self.loss_life = \
				100000000
		#self.margin_attack_of_life =  [int(self.fight_with.health / (self.interactor.attack + i - self.fight_with.defense))  * (self.fight_with.attack - self.interactor.defense) - self.loss_life for i in range(1,6)]
		#self.margin_defense_of_life = [int(self.fight_with.health / (self.interactor.attack - self.fight_with.defense)) * (self.fight_with.attack - self.interactor.defense - i) - self.loss_life for i in range(1,6)]
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

	@property
	def rewards(self):
		self.update_fight_value()
		return [
			{'attr':'health', 'value': -1 * self.loss_life},
			{'attr':'gold'  , 'value': self.fight_with.gold}
		]
class Open(Action):
	def __init__(self,door:Object):
		self.name = "Open door {}".format(door.name)
		self.door = door
		self.key_need = door.key_need
		self.info = "Open door (item : {})".format(self.door)
	def avaliable(self):
		if self.interactor[self.key_need] > 0:
			return True
		else:
			return False
	def interact(self):
		self.interactor[self.key_need] -= 1

	@property
	def rewards(self):
		return [
			{'attr':self.key_need, 'value': -1},
		]

class UnlockHiddenAction(Action):
	def __init__(self,TargetObject:Object,TargetAction :Action):
		self.TargetObject = TargetObject
		self.TargetAction = TargetAction
		self.info = TargetObject.name + " now can : " + TargetAction.info

	def interact(self):
		self.TargetObject.add_action(self.TargetAction)
