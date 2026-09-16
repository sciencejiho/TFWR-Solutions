# ------------------------------------------------------------------------------
# strategy_pumpkin.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory
import pumpkin_field
import strategy_polyculture

# region Farming strategy


def new_state():
	# Create state owned by the selected farming strategy.
	return {"polyculture": strategy_polyculture.new_state()}


def grow_world(state):
	# Grow and harvest one world-sized giant pumpkin.
	if inventory.target_ratio(Items.Carrot) < 1:
		strategy_polyculture.grow_world(state["polyculture"])
		return

	strategy_polyculture.finish(state["polyculture"])
	pumpkin_state, pending = pumpkin_field.scan_world()

	if len(pending) == 0:
		harvest()
		return

	max_revisits = get_world_size() * get_world_size()

	for _ in range(max_revisits):
		pending = pumpkin_field.revisit_pending(pumpkin_state, pending)

		if len(pending) == 0:
			harvest()
			return


def finish(state):
	# Drain any carrot-supply drones owned by this strategy.
	return strategy_polyculture.finish(state["polyculture"])


# endregion
