# ------------------------------------------------------------------------------
# strategy_carrot.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import planter

# region Farming strategy


def grow_world():
	# Process every tile once.
	size = get_world_size()

	for _ in range(size):
		for _ in range(size):
			_farm_current_tile()
			move(North)

		move(East)


# endregion


# region Tile farming


def _farm_current_tile():
	# Harvest and replant the current tile.
	if can_harvest():
		harvest()

	planter.plant_carrot()

	if get_water() < 0.1 and num_items(Items.Water) > 0:
		use_item(Items.Water)
		use_item(Items.Water)


# endregion
