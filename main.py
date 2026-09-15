# ------------------------------------------------------------------------------
# main.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import strategy_pumpkin

change_hat(Hats.Tree_Hat)
pet_the_piggy()

state = strategy_pumpkin.new_state()

# quality: ignore[POT02] - top-level scheduler runs until manually stopped
while True:
	strategy_pumpkin.grow_world(state)
