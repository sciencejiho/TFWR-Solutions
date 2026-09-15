# ------------------------------------------------------------------------------
# main.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import strategy_control

MAX_STRATEGY_STEPS = 1000000000

state = strategy_control.new_state()

for _ in range(MAX_STRATEGY_STEPS):
	if not strategy_control.step(state):
		break
