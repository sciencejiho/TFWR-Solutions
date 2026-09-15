from __builtins__ import *

import planter


def farm_tile():
	# Harvest and replant the current tile.

	if can_harvest():
		harvest()

	planter.plant_carrot()

	# planter.plant_pumpkin()

	if get_water() < 0.1 and num_items(Items.Water) > 0:
		use_item(Items.Water)
		use_item(Items.Water)


def farm_world():
	# Process every tile once.
	size = get_world_size()

	for _ in range(size):
		for _ in range(size):
			farm_tile()
			move(North)

		move(East)


change_hat(Hats.Tree_Hat)
pet_the_piggy()

while True:
	# giant_pumpkin.grow_world()
	farm_world()
