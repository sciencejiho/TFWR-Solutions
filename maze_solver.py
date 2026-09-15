# ------------------------------------------------------------------------------
# maze_solver.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import drone_control

# region Directions

DIRECTIONS = [North, East, South, West]
OPPOSITE = [2, 3, 0, 1]
X_CHANGE = [0, 1, 0, -1]
Y_CHANGE = [1, 0, -1, 0]

# endregion


# region Solver state


def new_state():
	# Create a persistent map of passages that are known to stay open.
	size = get_world_size()
	return {
		"connections": _new_connections(size),
		"mapped": False,
		"size": size,
	}


def _reset(state, size):
	state["connections"] = _new_connections(size)
	state["mapped"] = False
	state["size"] = size


# endregion


# region Mapping


def map_maze(state):
	# Explore entrance branches in parallel and merge their passage maps.
	size = get_world_size()

	if state["size"] != size:
		_reset(state, size)

	start_x = get_pos_x()
	start_y = get_pos_y()
	jobs = []

	for direction_index in range(len(DIRECTIONS)):
		if can_move(DIRECTIONS[direction_index]):
			jobs.append((start_x, start_y, direction_index, size))

	results = drone_control.run_jobs(_map_branch, jobs)

	for connections in results:
		if connections == None:
			return False

		_merge_connections(state["connections"], connections, size)

	state["mapped"] = True
	return True


def _map_branch(job):
	start_x, start_y, direction_index, size = job
	connections = _new_connections(size)
	visited = _new_grid(size, False)
	visited[start_x][start_y] = True

	if get_pos_x() != start_x or get_pos_y() != start_y:
		return None

	direction = DIRECTIONS[direction_index]

	if not can_move(direction) or not move(direction):
		return None

	x, y = _neighbor(start_x, start_y, direction_index, size)
	connections[start_x][start_y][direction_index] = True
	connections[x][y][OPPOSITE[direction_index]] = True
	visited[x][y] = True
	stack = [[x, y, 0, OPPOSITE[direction_index]]]
	max_steps = size * size * (len(DIRECTIONS) + 1) + 1

	for _ in range(max_steps):
		if len(stack) == 0:
			return connections

		frame = stack[len(stack) - 1]

		if frame[2] >= len(DIRECTIONS):
			back_direction = frame[3]
			stack.pop()

			if not move(DIRECTIONS[back_direction]):
				return None

			continue

		next_direction = frame[2]
		frame[2] += 1

		if not _visit_direction(
			connections,
			visited,
			stack,
			frame,
			next_direction,
		):
			return None

	return None


def _visit_direction(
	connections,
	visited,
	stack,
	frame,
	direction_index,
):
	size = len(connections)
	x = frame[0]
	y = frame[1]
	direction = DIRECTIONS[direction_index]

	if not can_move(direction):
		return True

	neighbor_x, neighbor_y = _neighbor(x, y, direction_index, size)
	connections[x][y][direction_index] = True
	connections[neighbor_x][neighbor_y][OPPOSITE[direction_index]] = True

	if visited[neighbor_x][neighbor_y]:
		return True

	if not move(direction):
		return False

	visited[neighbor_x][neighbor_y] = True
	stack.append(
		[
			neighbor_x,
			neighbor_y,
			0,
			OPPOSITE[direction_index],
		]
	)
	return True


def _merge_connections(target, source, size):
	for x in range(size):
		for y in range(size):
			_merge_tile(target[x][y], source[x][y])


def _merge_tile(target, source):
	for direction_index in range(len(DIRECTIONS)):
		if source[direction_index]:
			target[direction_index] = True


# endregion


# region Routing


def move_to_treasure(state):
	# Follow mapped passages to the treasure reported by measure().
	if not state["mapped"]:
		return False

	target = measure()

	if target == None:
		return False

	target_x, target_y = target
	path = _find_path(state, target_x, target_y)

	if path == None:
		return False

	for direction_index in path:
		if not move(DIRECTIONS[direction_index]):
			state["mapped"] = False
			return False

	return get_entity_type() == Entities.Treasure


def _find_path(state, target_x, target_y):
	size = state["size"]
	start_x = get_pos_x()
	start_y = get_pos_y()
	visited = _new_grid(size, False)
	parents = _new_grid(size, None)
	queue = [(start_x, start_y)]
	queue_index = 0
	visited[start_x][start_y] = True
	max_cells = size * size

	for _ in range(max_cells):
		if queue_index >= len(queue):
			return None

		x, y = queue[queue_index]
		queue_index += 1

		if x == target_x and y == target_y:
			return _build_path(parents, start_x, start_y, x, y)

		for direction_index in range(len(DIRECTIONS)):
			if not state["connections"][x][y][direction_index]:
				continue

			neighbor_x, neighbor_y = _neighbor(
				x,
				y,
				direction_index,
				size,
			)

			if visited[neighbor_x][neighbor_y]:
				continue

			visited[neighbor_x][neighbor_y] = True
			parents[neighbor_x][neighbor_y] = (x, y, direction_index)
			queue.append((neighbor_x, neighbor_y))

	return None


def _build_path(parents, start_x, start_y, target_x, target_y):
	path = []
	x = target_x
	y = target_y
	max_cells = len(parents) * len(parents)

	for _ in range(max_cells):
		if x == start_x and y == start_y:
			return path

		parent = parents[x][y]

		if parent == None:
			return None

		parent_x, parent_y, direction_index = parent
		path.insert(0, direction_index)
		x = parent_x
		y = parent_y

	return None


# endregion


# region State construction


def _neighbor(x, y, direction_index, size):
	neighbor_x = (x + X_CHANGE[direction_index]) % size
	neighbor_y = (y + Y_CHANGE[direction_index]) % size
	return neighbor_x, neighbor_y


def _new_grid(size, value):
	grid = []

	for x in range(size):
		column = []

		for y in range(size):
			column.append(value)

		grid.append(column)

	return grid


def _new_connections(size):
	connections = []

	for x in range(size):
		column = []

		for y in range(size):
			column.append([False, False, False, False])

		connections.append(column)

	return connections


# endregion
