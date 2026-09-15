from __builtins__ import *

import crop_care
import planter

# region Tile resolution


def resolve_current():
	# True means the current tile has a mature living pumpkin.
	entity = get_entity_type()

	if entity == Entities.Dead_Pumpkin:
		planter.plant_pumpkin()
		crop_care.water_if_needed()
		return False

	if entity != Entities.Pumpkin:
		if can_harvest():
			harvest()

		planter.plant_pumpkin()
		crop_care.water_if_needed()
		return False

	if can_harvest():
		return True

	crop_care.water_if_needed()
	return False


# endregion
