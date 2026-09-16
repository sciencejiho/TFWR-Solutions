# ------------------------------------------------------------------------------
# strategy_polyculture.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import drone_control
import inventory
import movement
import polyculture_field
import polyculture_tile

# region Crop selection

CROP_BY_ITEM = {
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Tree,
	Items.Carrot: Entities.Carrot,
	Items.Power: Entities.Sunflower,
}


def _select_primary(x, y):
	selected_item = None
	selected_ratio = None

	for item in CROP_BY_ITEM:
		ratio = inventory.target_ratio(item)

		if selected_ratio == None or ratio < selected_ratio:
			selected_item = item
			selected_ratio = ratio

	entity = CROP_BY_ITEM[selected_item]

	if entity == Entities.Tree and (x + y) % 2 != 0:
		return Entities.Bush

	return entity


# endregion


# region Strategy lifecycle


def new_state():
	# Create asynchronous lane state owned by this strategy.
	state = {}
	_reset_state(state, get_world_size())
	return state


def grow_world(state):
	# Advance child lanes and one controller lane without a global barrier.
	size = get_world_size()
	lane_count = min(max_drones(), size)

	if state["size"] != size or state["lane_count"] != lane_count:
		finish(state)
		_reset_state(state, size)

	_collect_finished(state)
	_process_requests(state)
	_launch_workers(state)
	_run_controller_lane(state)


def finish(state):
	# Drain active children without launching another column.
	for worker in state["workers"]:
		if worker["handle"] == None:
			continue

		results = wait_for(worker["handle"])
		_merge_column_results(state["field"], results)
		_complete_worker(state, worker)

	return True


def _reset_state(state, size):
	lane_count = min(max_drones(), size)
	workers = []

	for lane in range(lane_count - 1):
		workers.append(
			{
				"handle": None,
				"lane": lane,
				"next_x": lane,
				"x": None,
			}
		)

	state["controller_lane"] = lane_count - 1
	state["controller_x"] = lane_count - 1
	state["field"] = polyculture_field.new_field(size, lane_count)
	state["lane_count"] = lane_count
	state["size"] = size
	state["workers"] = workers


# endregion


# region Asynchronous lanes


def _collect_finished(state):
	for worker in state["workers"]:
		handle = worker["handle"]

		if handle == None or not has_finished(handle):
			continue

		results = wait_for(handle)
		_merge_column_results(state["field"], results)
		_complete_worker(state, worker)


def _complete_worker(state, worker):
	worker["next_x"] = _next_x(
		worker["x"],
		worker["lane"],
		state["lane_count"],
		state["size"],
	)
	worker["handle"] = None
	worker["x"] = None


def _launch_workers(state):
	for worker in state["workers"]:
		if worker["handle"] != None:
			continue

		x = worker["next_x"]
		job = _column_job(state["field"], x, state["size"])
		handle = drone_control.spawn_at(
			_maintain_column,
			job,
			(x, 0),
		)

		if handle != None:
			worker["handle"] = handle
			worker["x"] = x


def _run_controller_lane(state):
	x = state["controller_x"]
	job = _column_job(state["field"], x, state["size"])
	movement.move_to(x, 0)
	results = _maintain_column(job)
	_merge_column_results(state["field"], results)
	state["controller_x"] = _next_x(
		x,
		state["controller_lane"],
		state["lane_count"],
		state["size"],
	)


def _next_x(x, lane, lane_count, size):
	next_x = x + lane_count

	if next_x >= size:
		return lane

	return next_x


# endregion


# region Column work


def _column_job(field, x, size):
	job = []

	for y in range(size):
		expected = polyculture_field.get_crop(field, x, y)
		waiting = polyculture_field.has_request(field, x, y)
		primary = _select_primary(x, y)
		job.append((x, y, expected, waiting, primary))

	return job


def _maintain_column(job):
	results = []

	for tile_job in job:
		results.append(polyculture_tile.maintain_at(tile_job))

	return results


def _merge_column_results(field, results):
	for result in results:
		if result == None:
			continue

		x, y, entity, companion = result
		polyculture_field.set_crop(field, x, y, entity)
		_record_companion(field, x, y, companion)


# endregion


# region Companion requests


def _process_requests(state):
	field = state["field"]
	targets = polyculture_field.begin_request_pass(field)
	active_columns = _active_columns(state)
	processed = 0

	for target_x, target_y in targets:
		request = polyculture_field.peek_request(
			field,
			target_x,
			target_y,
		)

		if request == None:
			continue

		source_x, source_y = request["source"]

		if processed >= state["size"]:
			polyculture_field.wait_request(field, target_x, target_y)
			continue

		if source_x in active_columns or target_x in active_columns:
			polyculture_field.wait_request(field, target_x, target_y)
			continue

		if polyculture_field.has_request(field, target_x, target_y):
			polyculture_field.defer_request(field, target_x, target_y)
			continue

		job = {
			"entity": request["entity"],
			"source": (source_x, source_y),
			"source_entity": request["source_entity"],
			"target": (target_x, target_y),
		}
		result = polyculture_tile.resolve_request_at(job)
		processed += 1

		if result == None:
			polyculture_field.wait_request(field, target_x, target_y)
			continue

		_merge_request_result(field, result)


def _active_columns(state):
	columns = set()

	for worker in state["workers"]:
		if worker["handle"] != None:
			columns.add(worker["x"])

	return columns


def _merge_request_result(field, result):
	source_x, source_y = result["source"]
	target_x, target_y = result["target"]
	status = result["status"]

	if result["target_cleared"]:
		polyculture_field.set_crop(field, target_x, target_y, None)

	if status == polyculture_tile.REQUEST_SOURCE_MISSING:
		polyculture_field.set_crop(field, source_x, source_y, None)
		polyculture_field.complete_request(field, target_x, target_y)
		return

	if status == polyculture_tile.REQUEST_WAITING:
		polyculture_field.wait_request(field, target_x, target_y)
		return

	if status == polyculture_tile.REQUEST_BLOCKED:
		polyculture_field.defer_request(field, target_x, target_y)
		return

	polyculture_field.complete_request(field, target_x, target_y)

	if result["source_harvested"]:
		polyculture_field.set_crop(field, source_x, source_y, None)

	polyculture_field.set_crop(
		field,
		target_x,
		target_y,
		result["entity"],
	)
	_record_companion(
		field,
		target_x,
		target_y,
		result["companion"],
	)


def _record_companion(field, x, y, companion):
	if companion == None:
		return

	companion_entity, target = companion
	target_x, target_y = target
	polyculture_field.add_request(
		field,
		x,
		y,
		target_x,
		target_y,
		companion_entity,
	)


# endregion
