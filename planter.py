# ------------------------------------------------------------------------------
# planter.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory

# region Planting


def plant_entity(entity):
	# Plant an exact polyculture entity without applying strategy policy.
	if entity == Entities.Grass:
		_set_grassland()
		return True

	if entity == Entities.Bush or entity == Entities.Tree:
		return plant(entity)

	if entity == Entities.Cactus or entity == Entities.Carrot:
		_set_soil()
		return plant(entity)

	if entity == Entities.Pumpkin or entity == Entities.Sunflower:
		_set_soil()
		return plant(entity)

	return False


def plant_grass():
	# Prepare the tile for grass.
	_set_grassland()


def plant_bush():
	# Plant a bush.
	plant(Entities.Bush)


def plant_tree():
	# Plant trees in a checkerboard pattern.
	x = get_pos_x()
	y = get_pos_y()

	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	else:
		plant_bush()


def plant_carrot():
	# Plant a carrot while preserving inventory targets.
	hay = num_items(Items.Hay)
	wood = num_items(Items.Wood)

	hay_target = inventory.target_amount(Items.Hay)
	wood_target = inventory.target_amount(Items.Wood)

	if hay > hay_target and wood > wood_target:
		_set_soil()
		plant(Entities.Carrot)
	else:
		hay_ratio = inventory.target_ratio(Items.Hay)
		wood_ratio = inventory.target_ratio(Items.Wood)

		if hay_ratio < wood_ratio:
			plant_grass()
		else:
			plant_tree()


def plant_pumpkin():
	# Plant a pumpkin on soil.
	_set_soil()
	plant(Entities.Pumpkin)


# endregion


# region Ground setting


def _set_grassland():
	if get_ground_type() == Grounds.Soil:
		till()


def _set_soil():
	if get_ground_type() == Grounds.Grassland:
		till()


# endregion
