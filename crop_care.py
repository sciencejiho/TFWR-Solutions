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

	if num_items(Items.Water) <= inventory.TARGET[Items.Water]:
		return False

	return use_item(Items.Water)


# endregion


# region Fertilizer

MAX_FERTILIZER_USES = 3


def fertilize_until_mature():
	# Spend bounded fertilizer surplus until the current crop is mature.
	if can_harvest():
		return True

	for _ in range(MAX_FERTILIZER_USES):
		if num_items(Items.Fertilizer) <= inventory.TARGET[Items.Fertilizer]:
			return False

		if not use_item(Items.Fertilizer):
			return False

		if can_harvest():
			return True

	return False


# endregion


# region Combined care


def care_until_mature():
	# Apply available growth aids and report whether the crop is mature.
	if can_harvest():
		return True

	water_if_needed()

	if can_harvest():
		return True

	return fertilize_until_mature()


# endregion
