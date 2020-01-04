from world_old import *
from strategy import *

world = World()
world.log.info("生成世界中...")
world.log.debug("生成第一层...")
Object.add_object_to_world = world
start_yellow_door = yellow_door()
start_yellow_key = yellow_key()
door1 = yellow_door() #有骷髅那个黄门
door2 = yellow_door() #有加200血的那个黄门
door3 = yellow_door() #有法师那个黄门
monster1 = 绿色史莱姆()
monster2 = 红色史莱姆(monster1)
monster3 = 绿色史莱姆(monster2)# 上楼的绿色史莱姆
#右下角
monster4 = 小蝙蝠(door2)
monster5 = 绿色史莱姆(monster4)
monster6 = 绿色史莱姆(monster4)
h0 = health200([monster6,monster5])


monster7 = 骷髅人(door1)
h1 = health50(door1)
#通往骷髅士兵的门
door4 = yellow_door(monster7)
monster8 = 骷髅士兵(door4)
y_k = yellow_key(door4)
#中间的门
door5 = yellow_door(monster8)
#左下角四个道具
h2 = health50(door5)
h3 = health50(door5)
y_k2 = yellow_key(door5)
y_k3 = yellow_key(door5)

#有法师的那个门
bat2 = 小蝙蝠(door3)
fa = 初级法师(bat2)
bat3 = 小蝙蝠(fa)
inner_door = yellow_door(bat3)
#最里面的奖励道具
yellow_key(inner_door)
health50(inner_door)
oneattackup(inner_door)
onedefenseup(inner_door)

