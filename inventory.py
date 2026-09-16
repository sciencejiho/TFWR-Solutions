# ------------------------------------------------------------------------------
# inventory.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Farm targets

FARM_TARGET = {
	Items.Hay: 10000000,
	Items.Wood: 10000000,
	Items.Carrot: 10000000,
	Items.Pumpkin: 500000,
	Items.Weird_Substance: 25000,
	Items.Power: 25000,
	Items.Cactus: 1000000,
	Items.Gold: 1000000,
}

# endregion


# region Passive targets

PASSIVE_TARGET = {
	Items.Water: 50000,
	Items.Fertilizer: 5000,
}

REFILL_RATIO = 0.8

# endregion


# ------------------------------------------------------------------------------
# region Queries
# ------------------------------------------------------------------------------
def target_amount(item):
	# Return the configured farm target or passive reserve.
	if item in FARM_TARGET:
		return FARM_TARGET[item]

	return PASSIVE_TARGET[item]


def target_ratio(item):
	# Return current inventory relative to target.
	return num_items(item) / target_amount(item)


def below_target(item):
	# Return whether inventory is below target.
	return num_items(item) < target_amount(item)


def needs_refill(item):
	# Return whether a farmed item is low enough to preempt a maze.
	return target_ratio(item) < REFILL_RATIO


# endregion
