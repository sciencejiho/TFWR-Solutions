# ------------------------------------------------------------------------------
# cactus_field.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import cactus_tile
import drone_control
import movement

# region Field scanning


def scan_world():
	# Scan every tile and return readiness state and pending coordinates.
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
		ready = cactus_tile.resolve_current()
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

		if cactus_tile.resolve_current():
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


# region Sorting


def sort_world():
	# Sort rows eastward, then columns northward.
	size = get_world_size()
	row_starts = []
	column_starts = []

	for index in range(size):
		row_starts.append((0, index))
		column_starts.append((index, 0))

	if not _all_succeeded(
		drone_control.run_jobs(_sort_row, range(size), row_starts)
	):
		return False

	return _all_succeeded(
		drone_control.run_jobs(_sort_column, range(size), column_starts)
	)


def _sort_row(y):
	return _sort_line(0, y, East, get_world_size())


def _sort_column(x):
	return _sort_line(x, 0, North, get_world_size())


def _all_succeeded(results):
	for result in results:
		if not result:
			return False

	return True


def _sort_line(start_x, start_y, direction, size):
	for pass_index in range(size - 1):
		is_sorted = True
		movement.move_to(start_x, start_y)

		for _ in range(size - pass_index - 1):
			swapped = _swap_if_needed(direction)

			if swapped == None:
				return False

			if swapped:
				is_sorted = False

			if not move(direction):
				return False

		if is_sorted:
			return True

	return True


def _swap_if_needed(direction):
	current_size = measure()
	next_size = measure(direction)

	if current_size == None or next_size == None:
		return None

	if current_size <= next_size:
		return False

	if not swap(direction):
		return None

	return True


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
