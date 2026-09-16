# ------------------------------------------------------------------------------
# pumpkin_tile.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import crop_care
import planter

# region Tile resolution


def resolve_current():
	# True means the current tile has a mature living pumpkin.
	entity = get_entity_type()

	if entity == Entities.Dead_Pumpkin:
		planter.plant_pumpkin()
		return crop_care.care_after_planting()

	if entity != Entities.Pumpkin:
		if can_harvest():
			harvest()

		planter.plant_pumpkin()
		return crop_care.care_after_planting()

	if can_harvest():
		return True

	return crop_care.care_on_revisit()


# endregion
