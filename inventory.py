# region Targets

TARGET = {
	Items.Hay: 100000,
	Items.Wood: 100000,
	Items.Carrot: 10000,
	Items.Pumpkin: 10000,
	Items.Weird_Substance: 10000,
	Items.Water: 10000,
	Items.Fertilizer: 10000,
	Items.Power: 10000
}

# endregion


# region Queries

def target_ratio(item):
	# Return current inventory relative to target.
	return num_items(item) / TARGET[item]


def below_target(item):
	# Return whether inventory is below target.
	return num_items(item) < TARGET[item]

# endregion