# ------------------------------------------------------------------------------
# polyculture_tile.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
import movement
import planter

# region Planting


def maintain_at(job):
	# Complete one crop visit before the lane moves to the next tile.
	x, y, expected, waiting, primary = job
	movement.move_to(x, y)
	current = get_entity_type()

	if expected != None and current == expected:
		if waiting:
			return x, y, expected, None

		if not can_harvest() and not crop_care.care_on_revisit():
			return x, y, expected, None

		if not harvest():
			return x, y, expected, None

	result = plant_at((x, y, primary))

	if result == None:
		return x, y, None, None

	return result


def plant_at(job):
	# Plant one coordinate and return the observation for controller state.
	x, y, entity = job
	movement.move_to(x, y)
	current = get_entity_type()

	if current != None and current != Entities.Dead_Pumpkin:
		if not can_harvest() and not crop_care.care_on_revisit():
			return None

		if not harvest():
			return None

	planted = _plant_with_fallback(entity)

	if planted == None:
		return None

	planted_entity, companion = planted
	crop_care.care_after_planting()
	return x, y, planted_entity, companion


def _plant_with_fallback(entity):
	if planter.plant_entity(entity):
		return entity, get_companion()

	if entity == Entities.Grass:
		return None

	if not planter.plant_entity(Entities.Grass):
		return None

	return Entities.Grass, get_companion()


# endregion


# region Companion resolution

REQUEST_SOURCE_MISSING = 0
REQUEST_WAITING = 1
REQUEST_BLOCKED = 2
REQUEST_COMPLETED = 3


def resolve_request_at(job):
	# Resolve one physical source-target transaction without shared state.
	source_x, source_y = job["source"]
	target_x, target_y = job["target"]
	movement.move_to(source_x, source_y)

	if get_entity_type() != job["source_entity"]:
		return _request_result(job, REQUEST_SOURCE_MISSING)

	if not can_harvest() and not crop_care.care_on_revisit():
		return _request_result(job, REQUEST_WAITING)

	movement.move_to(target_x, target_y)
	target_cleared = _clear_current()

	if not target_cleared:
		return _request_result(job, REQUEST_BLOCKED)

	if not planter.plant_entity(job["entity"]):
		result = _request_result(job, REQUEST_BLOCKED)
		result["target_cleared"] = True
		return result

	crop_care.care_after_planting()
	companion = get_companion()
	movement.move_to(source_x, source_y)
	source_harvested = False

	if get_entity_type() == job["source_entity"] and can_harvest():
		source_harvested = harvest()

	result = _request_result(job, REQUEST_COMPLETED)
	result["companion"] = companion
	result["entity"] = job["entity"]
	result["source_harvested"] = source_harvested
	result["target_cleared"] = True
	return result


def _request_result(job, status):
	return {
		"companion": None,
		"entity": None,
		"source": job["source"],
		"source_harvested": False,
		"status": status,
		"target": job["target"],
		"target_cleared": False,
	}


def _clear_current():
	entity = get_entity_type()

	if entity == None or entity == Entities.Dead_Pumpkin:
		return True

	if not can_harvest() and not crop_care.care_on_revisit():
		return False

	return harvest()


# endregion
