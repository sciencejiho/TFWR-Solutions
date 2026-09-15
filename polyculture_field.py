# ------------------------------------------------------------------------------
# polyculture_field.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Field state


def new_field(size, max_attempts):
	# Create bounded crop and companion-request state for the world.
	return {
		"crop_count": 0,
		"crop_scheduled": _new_grid(size, False),
		"crop_targets": [],
		"crops": _new_grid(size, None),
		"max_attempts": max_attempts,
		"requests": _new_queue_grid(size),
		"scheduled": _new_grid(size, False),
		"source_targets": _new_grid(size, None),
		"size": size,
		"targets": [],
	}


def get_crop(field, x, y):
	# Return the entity tracked at a coordinate.
	return field["crops"][x][y]


def set_crop(field, x, y, entity):
	# Record the entity currently planted at a coordinate.
	previous = field["crops"][x][y]

	if previous == None and entity != None:
		field["crop_count"] += 1
	elif previous != None and entity == None:
		field["crop_count"] -= 1

	field["crops"][x][y] = entity

	if entity == None or field["crop_scheduled"][x][y]:
		return

	field["crop_targets"].append((x, y))
	field["crop_scheduled"][x][y] = True


def crop_count(field):
	# Return the number of coordinates with managed crops.
	return field["crop_count"]


def begin_crop_pass(field):
	# Return a fixed snapshot containing only currently managed crops.
	targets = field["crop_targets"]
	field["crop_targets"] = []
	active = []

	for x, y in targets:
		field["crop_scheduled"][x][y] = False

		if field["crops"][x][y] != None:
			active.append((x, y))

	return active


# endregion


# region Companion requests


def add_request(field, source_x, source_y, target_x, target_y, entity):
	# Queue one companion request for a source that has no request yet.
	if field["source_targets"][source_x][source_y] != None:
		return False

	request = {
		"attempts": 0,
		"entity": entity,
		"source": (source_x, source_y),
		"source_entity": field["crops"][source_x][source_y],
	}
	field["requests"][target_x][target_y].append(request)
	field["source_targets"][source_x][source_y] = (target_x, target_y)
	_schedule_target(field, target_x, target_y)
	return True


def has_request(field, source_x, source_y):
	# Return whether a source crop is waiting for its companion.
	return field["source_targets"][source_x][source_y] != None


def begin_request_pass(field):
	# Return a fixed work snapshot; newly queued work waits for the next pass.
	targets = field["targets"]
	field["targets"] = []

	for x, y in targets:
		field["scheduled"][x][y] = False

	return targets


def peek_request(field, target_x, target_y):
	# Return the oldest request for a target coordinate.
	queue = field["requests"][target_x][target_y]

	if len(queue) == 0:
		return None

	return queue[0]


def complete_request(field, target_x, target_y):
	# Remove and return the oldest request, preserving later FIFO work.
	queue = field["requests"][target_x][target_y]

	if len(queue) == 0:
		return None

	request = queue.pop(0)
	source_x, source_y = request["source"]
	field["source_targets"][source_x][source_y] = None

	if len(queue) > 0:
		_schedule_target(field, target_x, target_y)

	return request


def defer_request(field, target_x, target_y):
	# Reschedule a blocked request or return it when its limit expires.
	request = peek_request(field, target_x, target_y)

	if request == None:
		return None

	request["attempts"] += 1

	if request["attempts"] >= field["max_attempts"]:
		return complete_request(field, target_x, target_y)

	_schedule_target(field, target_x, target_y)
	return None


def wait_request(field, target_x, target_y):
	# Reschedule a request without consuming a collision attempt.
	if peek_request(field, target_x, target_y) == None:
		return False

	_schedule_target(field, target_x, target_y)
	return True


def _schedule_target(field, x, y):
	if field["scheduled"][x][y]:
		return

	field["targets"].append((x, y))
	field["scheduled"][x][y] = True


# endregion


# region State construction


def _new_grid(size, value):
	grid = []

	for x in range(size):
		column = []

		for y in range(size):
			column.append(value)

		grid.append(column)

	return grid


def _new_queue_grid(size):
	grid = []

	for x in range(size):
		column = []

		for y in range(size):
			column.append([])

		grid.append(column)

	return grid


# endregion
