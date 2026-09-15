# ------------------------------------------------------------------------------
# movement.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Positioning


def move_to(x, y):
	# Move the drone to a world coordinate.
	size = get_world_size()

	_move_x(x, size)
	_move_y(y, size)


def _move_x(target, size):
	current = get_pos_x()

	east = (target - current) % size
	west = (current - target) % size

	if east <= west:
		for _ in range(east):
			move(East)
	else:
		for _ in range(west):
			move(West)


def _move_y(target, size):
	current = get_pos_y()

	north = (target - current) % size
	south = (current - target) % size

	if north <= south:
		for _ in range(north):
			move(North)
	else:
		for _ in range(south):
			move(South)


# endregion
