from world import *
from strategy import *

world = World()
world.log.info("生成世界中...")
world.log.debug("生成第一层...")
Object.add_object_to_world = world
monster1 = 绿色史莱姆()
monster2 = 红色史莱姆()
monster3 = 绿色史莱姆()# 上楼的绿色史莱姆
monster4 = 小蝙蝠()
monster5 = 绿色史莱姆()
monster6 = 绿色史莱姆()
h0 = health200([monster6,monster5])
monster7 = 骷髅士兵()
monster8 = 骷髅士兵()
sword = sword(monster8)
world.run_warrior(QLearning())

