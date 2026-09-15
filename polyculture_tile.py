# ------------------------------------------------------------------------------
# polyculture_tile.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
import movement
import planter
import polyculture_field

# region Planting


def plant_current(field, entity):
	# Plant one exact crop and record its companion preference.
	if not planter.plant_entity(entity):
		return False

	x = get_pos_x()
	y = get_pos_y()
	polyculture_field.set_crop(field, x, y, entity)
	companion = get_companion()

	if companion == None:
		return True

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
	return True


# endregion


# region Companion resolution


def resolve_request(field, target_x, target_y):
	# Resolve the oldest companion request for one target coordinate.
	request = polyculture_field.peek_request(field, target_x, target_y)

	if request == None:
		return

	source_x, source_y = request["source"]
	movement.move_to(source_x, source_y)

	if get_entity_type() != request["source_entity"]:
		polyculture_field.set_crop(field, source_x, source_y, None)
		polyculture_field.complete_request(field, target_x, target_y)
		return

	if not can_harvest() and not crop_care.care_until_mature():
		polyculture_field.wait_request(field, target_x, target_y)
		return None

	movement.move_to(target_x, target_y)

	if not _clear_target(field, target_x, target_y):
		return _expire_or_defer(field, target_x, target_y, request)

	if not plant_current(field, request["entity"]):
		return _expire_or_defer(field, target_x, target_y, request)

	polyculture_field.complete_request(field, target_x, target_y)
	return _harvest_source(field, request)


def _clear_target(field, x, y):
	entity = get_entity_type()

	if entity == None or entity == Entities.Dead_Pumpkin:
		polyculture_field.set_crop(field, x, y, None)
		return True

	if not can_harvest() and not crop_care.care_until_mature():
		return False

	if not harvest():
		return False

	polyculture_field.set_crop(field, x, y, None)
	return True


def _expire_or_defer(field, target_x, target_y, request):
	expired = polyculture_field.defer_request(field, target_x, target_y)

	if expired != None:
		return _harvest_source(field, request)

	return None


def _harvest_source(field, request):
	source_x, source_y = request["source"]
	movement.move_to(source_x, source_y)

	if get_entity_type() != request["source_entity"]:
		polyculture_field.set_crop(field, source_x, source_y, None)
		return

	if can_harvest() and harvest():
		polyculture_field.set_crop(field, source_x, source_y, None)
		return source_x, source_y

	return None


# endregion
