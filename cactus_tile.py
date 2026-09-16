# ------------------------------------------------------------------------------
# cactus_tile.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
import planter

# region Tile resolution


def resolve_current():
	# True means the current tile has a mature cactus.
	entity = get_entity_type()

	if entity == Entities.Cactus:
		return crop_care.care_on_revisit()

	if entity == Entities.Dead_Pumpkin:
		if not planter.plant_entity(Entities.Cactus):
			return False

		return crop_care.care_after_planting()

	if entity != None:
		if not can_harvest() and not crop_care.care_on_revisit():
			return False

		if not harvest():
			return False

	if not planter.plant_entity(Entities.Cactus):
		return False

	return crop_care.care_after_planting()


# endregion
