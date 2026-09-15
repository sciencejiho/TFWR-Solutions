# ------------------------------------------------------------------------------
# strategy_polyculture.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
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

CROP_MISSING = 0
CROP_KEPT = 1
CROP_HARVESTED = 2


def _select_primary():
	selected_item = None
	selected_ratio = None

	for item in CROP_BY_ITEM:
		ratio = inventory.target_ratio(item)

		if selected_ratio == None or ratio < selected_ratio:
			selected_item = item
			selected_ratio = ratio

	return CROP_BY_ITEM[selected_item]


# endregion


# region Farming strategy


def new_state():
	# Create explicitly owned persistent state for this strategy.
	size = get_world_size()
	return {"field": polyculture_field.new_field(size, size)}


def grow_world(state):
	# Advance one bounded pass of a persistent compact polyculture field.
	size = get_world_size()
	limit = _crop_limit(size)
	field = state["field"]

	if field["size"] != size:
		field = polyculture_field.new_field(size, size)
		state["field"] = field

	_process_crops(field, limit)
	_process_requests(field, limit)
	_seed_field(field, limit)


def _crop_limit(size):
	limit = size * 2
	area = size * size

	if limit > area:
		return area

	return limit


def _process_crops(field, limit):
	coordinates = polyculture_field.begin_crop_pass(field)
	jobs = []

	for x, y in coordinates:
		expected = polyculture_field.get_crop(field, x, y)
		waiting = polyculture_field.has_request(field, x, y)
		jobs.append((x, y, expected, waiting))

	results = drone_control.run_jobs(_process_crop, jobs)

	for x, y, expected, result in results:
		if result == CROP_MISSING:
			polyculture_field.set_crop(field, x, y, None)
		elif result == CROP_HARVESTED:
			polyculture_field.set_crop(field, x, y, None)
			movement.move_to(x, y)
			_plant_if_below_limit(field, limit)
		else:
			polyculture_field.set_crop(field, x, y, expected)


def _process_crop(job):
	x, y, expected, waiting = job
	movement.move_to(x, y)

	if get_entity_type() != expected:
		return x, y, expected, CROP_MISSING

	if waiting:
		return x, y, expected, CROP_KEPT

	if not can_harvest() and not crop_care.care_until_mature():
		return x, y, expected, CROP_KEPT

	if can_harvest() and harvest():
		return x, y, expected, CROP_HARVESTED

	return x, y, expected, CROP_KEPT


def _process_requests(field, limit):
	targets = polyculture_field.begin_request_pass(field)

	for x, y in targets:
		opened = polyculture_tile.resolve_request(field, x, y)

		if opened != None:
			movement.move_to(opened[0], opened[1])
			_plant_if_below_limit(field, limit)


def _seed_field(field, limit):
	for _ in range(limit):
		if polyculture_field.crop_count(field) >= limit:
			return

		_seed_current(field)
		move(North)

		if get_pos_y() == 0:
			move(East)


def _seed_current(field):
	x = get_pos_x()
	y = get_pos_y()

	if polyculture_field.get_crop(field, x, y) != None:
		return

	entity = get_entity_type()

	if entity != None and (not can_harvest() or not harvest()):
		return

	polyculture_field.set_crop(field, x, y, None)
	_plant_primary(field)


def _plant_if_below_limit(field, limit):
	if polyculture_field.crop_count(field) < limit:
		_plant_primary(field)


def _plant_primary(field):
	entity = _select_primary()

	if polyculture_tile.plant_current(field, entity):
		return True

	if entity != Entities.Grass:
		return polyculture_tile.plant_current(field, Entities.Grass)

	return False


# endregion
