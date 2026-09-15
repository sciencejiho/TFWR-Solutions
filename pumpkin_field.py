# ------------------------------------------------------------------------------
# pumpkin_field.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import movement
import pumpkin_tile

# region Field scanning


def scan_world():
	# Scan every tile and return its readiness state and pending coordinates.
	size = get_world_size()
	state = _new_state(size)
	pending = []

	for _ in range(size):
		for _ in range(size):
			x = get_pos_x()
			y = get_pos_y()

			if pumpkin_tile.resolve_current():
				state[x][y] = True
			else:
				pending.append((x, y))

			move(North)

		move(East)

	return state, pending


def revisit_pending(state, pending):
	# Revisit unresolved coordinates and return those still unresolved.
	next_pending = []

	for x, y in pending:
		movement.move_to(x, y)

		if pumpkin_tile.resolve_current():
			state[x][y] = True
		else:
			next_pending.append((x, y))

	return next_pending


# endregion


# region Field state


def _new_state(size):
	# state[x][y] is True once that tile is confirmed ready.
	state = []

	for x in range(size):
		column = []

		for y in range(size):
			column.append(False)

		state.append(column)

	return state


# endregion
