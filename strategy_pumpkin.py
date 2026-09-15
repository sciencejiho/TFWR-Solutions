from __builtins__ import *

import pumpkin_field

# region Farming strategy


def grow_world():
	# Grow and harvest one world-sized giant pumpkin.
	state, pending = pumpkin_field.scan_world()

	while pending:
		pending = pumpkin_field.revisit_pending(state, pending)

	harvest()


# endregion
