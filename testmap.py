from world_old import *
from strategy import *
from visulization import *
import threading
world = World()
world.log.info("生成世界中...")
world.log.debug("生成第一层...")
Object.add_object_to_world = world
Action.interactor = Warrior(name='skydownacai',health=300,attack=10,defense=10,gold=6).place(1,9,5) #指定warrior
def create_world():
	open_yellow_door = yellow_door().place(1,8,5)

	yellow_key().place(1,9,4)#

	yellow_key().place(1,10,4)#开局送两把钥匙

	a = yellow_door(open_yellow_door).place(1,8,9) #进右下角的

	b = yellow_door(open_yellow_door).place(1,5,5) #进中间的

	c = yellow_door(open_yellow_door).place(1,2,3) # 进骷髅的

	monster1 = 骷髅人(open_yellow_door).place(1,0,4)

	monster2 = 红色史莱姆(monster1).place(1,0,3)

	monster3 = 绿色史莱姆(monster2).place(1,0,2) #上楼梯口那个

	monster4 = 小蝙蝠(a).place(1,9,9)

	monster5 = 绿色史莱姆(monster4).place(1,10,8)

	monster6 = 绿色史莱姆(monster4).place(1,10,10)

	h0 = health200([monster6,monster5,monster4]).place(1,10,9)

	monster7 = 绿色史莱姆(b).place(1,2,1)

	monster8 = 绿色史莱姆(b).place(1,3,0)

	mysword = sword(monster8).place(1,2,0)

	world.log.debug("生成第一层...")

	start = 绿色史莱姆(monster3).place(2,10,4)

	monster3 = 绿色史莱姆(start).place(2,0,2)

world.create_world =create_world
rule = QLearning()
visual = GUI(world)
learning_thread = threading.Thread(target=world.run_warrior,kwargs={"strategy":rule})
learning_thread.start()
visual_thread = threading.Thread(target=visual.run)
visual_thread.start()