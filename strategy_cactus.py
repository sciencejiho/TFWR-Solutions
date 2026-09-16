# ------------------------------------------------------------------------------
# strategy_cactus.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import cactus_field
import inventory
import strategy_pumpkin

# region Farming strategy


def new_state():
	# Create state for the pumpkin strategy that supplies cactus planting.
	return {"pumpkin": strategy_pumpkin.new_state()}


def grow_world(state):
	# Grow, sort, and harvest one world of cacti while below target.
	if not inventory.below_target(Items.Cactus):
		return False

	if inventory.below_target(Items.Pumpkin):
		strategy_pumpkin.grow_world(state["pumpkin"])
		return True

	strategy_pumpkin.finish(state["pumpkin"])
	cactus_state, pending = cactus_field.scan_world()
	max_revisits = get_world_size() * get_world_size()

	for _ in range(max_revisits):
		if len(pending) == 0:
			break

		pending = cactus_field.revisit_pending(cactus_state, pending)

	if len(pending) > 0:
		return True

	if not cactus_field.sort_world():
		return False

	return harvest()


def finish(state):
	# Drain any nested pumpkin or polyculture supply drones.
	return strategy_pumpkin.finish(state["pumpkin"])


# endregion
