# ------------------------------------------------------------------------------
# strategy_carrot.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import drone_control
import movement
import planter

# region Farming strategy


def grow_world():
	# Process every column across the available drones.
	size = get_world_size()
	drone_control.run_jobs(_farm_column, range(size))


def _farm_column(x):
	movement.move_to(x, 0)

	for _ in range(get_world_size()):
		_farm_current_tile()
		move(North)


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
