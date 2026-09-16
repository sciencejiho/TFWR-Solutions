# ------------------------------------------------------------------------------
# crop_care.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory

# region Water


def water_if_needed():
	# Water a dry tile only when inventory is above its reserve.
	if get_water() >= 0.1:
		return False

	if not _has_drone_margin(Items.Water):
		return False

	return use_item(Items.Water)


# endregion


# region Fertilizer

SLOW_GROWERS = {
	Entities.Bush,
	Entities.Carrot,
	Entities.Sunflower,
	Entities.Tree,
}


def fertilize_if_useful(for_substance=False):
	# Use one dose only for a slow crop or needed Weird Substance.
	if can_harvest() or not _has_drone_margin(Items.Fertilizer):
		return False

	if not for_substance and get_entity_type() not in SLOW_GROWERS:
		return False

	return use_item(Items.Fertilizer)


# endregion


# region Care policies


def care_after_planting():
	# Water new plants and infect them only while substance is needed.
	water_if_needed()

	if inventory.below_target(Items.Weird_Substance):
		fertilize_if_useful(True)

	return can_harvest()


def care_on_revisit():
	# Help a slow plant only after a traversal found it still growing.
	if can_harvest():
		return True

	water_if_needed()

	if can_harvest():
		return True

	fertilize_if_useful()
	return can_harvest()


# endregion


# region Spending


def _has_drone_margin(item):
	reserve = inventory.target_amount(item)
	return num_items(item) >= reserve + max_drones()


# endregion
