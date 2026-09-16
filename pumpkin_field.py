# ------------------------------------------------------------------------------
# pumpkin_field.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import drone_control
import movement
import pumpkin_tile

# region Field scanning


def scan_world():
	# Scan every tile and return its readiness state and pending coordinates.
	size = get_world_size()
	state = _new_state(size)
	pending = []
	jobs = range(size)
	starts = []

	for x in jobs:
		starts.append((x, 0))

	results = drone_control.run_jobs(_scan_column, jobs, starts)

	for x, column, column_pending in results:
		for y in range(size):
			state[x][y] = column[y]

		for index in range(len(column_pending)):
			pending.append(column_pending[index])

	return state, pending


def _scan_column(x):
	column = []
	pending = []
	movement.move_to(x, 0)

	for y in range(get_world_size()):
		ready = pumpkin_tile.resolve_current()
		column.append(ready)

		if not ready:
			pending.append((x, y))

		move(North)

	return x, column, pending


def revisit_pending(state, pending):
	# Revisit unresolved coordinates and return those still unresolved.
	next_pending = []
	jobs = _group_by_column(pending)
	starts = []

	for coordinates in jobs:
		starts.append(coordinates[0])

	results = drone_control.run_jobs(_revisit_coordinates, jobs, starts)

	for resolved, unresolved in results:
		for x, y in resolved:
			state[x][y] = True

		for index in range(len(unresolved)):
			next_pending.append(unresolved[index])

	return next_pending


def _revisit_coordinates(coordinates):
	resolved = []
	unresolved = []

	for x, y in coordinates:
		movement.move_to(x, y)

		if pumpkin_tile.resolve_current():
			resolved.append((x, y))
		else:
			unresolved.append((x, y))

	return resolved, unresolved


def _group_by_column(coordinates):
	size = get_world_size()
	columns = []
	jobs = []

	for _ in range(size):
		columns.append([])

	for x, y in coordinates:
		columns[x].append((x, y))

	for column in columns:
		if len(column) > 0:
			jobs.append(column)

	return jobs


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
