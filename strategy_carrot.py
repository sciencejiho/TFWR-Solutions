# ------------------------------------------------------------------------------
# strategy_carrot.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
import drone_control
import movement
import planter

# region Farming strategy


def grow_world():
	# Process every column across the available drones.
	size = get_world_size()
	jobs = range(size)
	starts = []

	for x in jobs:
		starts.append((x, 0))

	drone_control.run_jobs(_farm_column, jobs, starts)


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
	crop_care.care_after_planting()


# endregion
