from world import *
from strategy import *
from visulization import *
import threading
world = World()
world.log.info("生成世界中...")
world.log.debug("生成第一层...")
Object.add_object_to_world = world
Action.interactor = Warrior(name='skydownacai',health=1000,attack=10,defense=10,gold=6)
monster1 = 绿色史莱姆().place(1,0,4)
monster2 = 红色史莱姆(monster1).place(1,0,3)
monster3 = 绿色史莱姆(monster2).place(1,0,2)
monster4 = 小蝙蝠().place(1,9,9)
monster5 = 绿色史莱姆().place(1,10,8)
monster6 = 绿色史莱姆().place(1,10,10)
h0 = health200([monster6,monster5,monster4]).place(1,10,9)
monster7 = 骷髅士兵().place(1,2,1)
monster8 = 骷髅士兵().place(1,3,0)
sword = sword(monster8).place(1,2,0)


rule = QLearning()
learning_thread = threading.Thread(target=world.run_warrior,kwargs={"strategy":rule})
learning_thread.start()

visual = GUI(world)
visual.run()