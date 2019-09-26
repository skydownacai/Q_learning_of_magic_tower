floor1 = []
for i in range(10):
	floor1.append(("wood_wall",1,i))
for i in range(8):
	floor1.append(("wood_wall",i + 3,3))
for i in [4,7]:
	floor1.append(("wood_wall",i,0))
	floor1.append(("wood_wall",i,2))
for i in [4,7]:
	floor1.append(("wood_wall",i,0))
	floor1.append(("wood_wall",i,2))
walls = [
	("wood_wall",2,5),("wood_wall",2,9),
	("wood_wall", 3, 5), ("wood_wall", 3, 9),
	("wood_wall", 4, 5), ("wood_wall", 4, 6),("wood_wall", 4, 7),("wood_wall", 4, 9),
	("wood_wall", 4, 5), ("wood_wall", 4, 6), ("wood_wall", 4, 7), ("wood_wall", 4, 9),
	("wood_wall",8,4),
	("wood_wall",8,6),
	("wood_wall",8,7),
	("wood_wall",8,7),
	("wood_wall",9,7),
	("wood_wall",10,7),
	("wood_wall",8,8),
	("wood_wall",8,10),
	("wood_wall",5,9),
	("wood_wall",6,9),
	("wood_wall",6,8),
	("wood_wall",6,7),
	("wood_wall",6,6),
	("wood_wall",6,5),

]
floor1.append(("stair_up",0,0))
floor1 += walls
