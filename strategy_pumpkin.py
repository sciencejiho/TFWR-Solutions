# ------------------------------------------------------------------------------
# strategy_pumpkin.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory
import pumpkin_field
import strategy_carrot

# region Farming strategy


def grow_world():
	# Grow and harvest one world-sized giant pumpkin.
	if inventory.target_ratio(Items.Carrot) < 1:
		strategy_carrot.grow_world()
		return

	state, pending = pumpkin_field.scan_world()

	while pending:
		pending = pumpkin_field.revisit_pending(state, pending)

	harvest()


# endregion
