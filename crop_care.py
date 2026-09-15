from __builtins__ import *

# region Water


def water_if_needed():
	# Water the current tile when it is dry and water is available.
	if get_water() < 0.1 and num_items(Items.Water) > 0:
		use_item(Items.Water)


# endregion
