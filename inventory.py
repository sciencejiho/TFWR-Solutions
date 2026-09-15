# ------------------------------------------------------------------------------
# inventory.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Targets

TARGET = {
	Items.Hay: 500000,
	Items.Wood: 500000,
	Items.Carrot: 100000,
	Items.Pumpkin: 100000,
	Items.Weird_Substance: 10000,
	Items.Water: 5000,
	Items.Fertilizer: 500,
	Items.Power: 500,
}

# endregion


# ------------------------------------------------------------------------------
# region Queries
# ------------------------------------------------------------------------------
def target_ratio(item):
	# Return current inventory relative to target.
	return num_items(item) / TARGET[item]


def below_target(item):
	# Return whether inventory is below target.
	return num_items(item) < TARGET[item]


# endregion
