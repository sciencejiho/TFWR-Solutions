# ------------------------------------------------------------------------------
# strategy_control.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory
import strategy_cactus
import strategy_maze
import strategy_polyculture
import strategy_pumpkin

# region Modes

CACTUS = "cactus"
MAZE = "maze"
POLYCULTURE = "polyculture"
PUMPKIN = "pumpkin"

MODE_BY_ITEM = {
	Items.Hay: POLYCULTURE,
	Items.Wood: POLYCULTURE,
	Items.Carrot: POLYCULTURE,
	Items.Power: POLYCULTURE,
	Items.Weird_Substance: POLYCULTURE,
	Items.Pumpkin: PUMPKIN,
	Items.Cactus: CACTUS,
	Items.Gold: MAZE,
}

# endregion


# region Controller state


def new_state():
	# Keep one persistent state object for every selectable strategy.
	return {
		"active": None,
		CACTUS: strategy_cactus.new_state(),
		MAZE: strategy_maze.new_state(),
		POLYCULTURE: strategy_polyculture.new_state(),
		PUMPKIN: strategy_pumpkin.new_state(),
	}


# endregion


# region Scheduling


def step(state):
	# Advance the selected strategy once without rebuilding its field.
	mode = _select_mode(state["active"])

	if mode != state["active"] and not _change_mode(state, mode):
		return True

	if mode == None:
		return False

	if _run_mode(state, mode):
		return True

	state["active"] = None
	return _has_work()


def _select_mode(active):
	if active == MAZE:
		urgent = _lowest_mode(True, MAZE)

		if urgent != None:
			return urgent

	mode = _lowest_mode(False, None)

	if mode == MAZE and not strategy_maze.can_start():
		return POLYCULTURE

	return mode


def _lowest_mode(refill_only, excluded):
	selected_mode = None
	selected_ratio = None

	for item in inventory.FARM_TARGET:
		mode = MODE_BY_ITEM[item]

		if mode == excluded or not inventory.below_target(item):
			continue

		if refill_only and not inventory.needs_refill(item):
			continue

		ratio = inventory.target_ratio(item)

		if selected_ratio == None or ratio < selected_ratio:
			selected_mode = mode
			selected_ratio = ratio

	return selected_mode


def _has_work():
	return _lowest_mode(False, None) != None


# endregion


# region Transitions


def _change_mode(state, mode):
	if not _finish_mode(state, state["active"]):
		return False

	if mode == None:
		state["active"] = None
		return True

	clear()
	state[mode] = _new_mode_state(mode)
	state["active"] = mode
	return True


def _finish_mode(state, mode):
	if mode == CACTUS:
		return strategy_cactus.finish(state[CACTUS])

	if mode == MAZE:
		return strategy_maze.finish(state[MAZE])

	if mode == POLYCULTURE:
		return strategy_polyculture.finish(state[POLYCULTURE])

	if mode == PUMPKIN:
		return strategy_pumpkin.finish(state[PUMPKIN])

	return True


def _new_mode_state(mode):
	if mode == CACTUS:
		return strategy_cactus.new_state()

	if mode == MAZE:
		return strategy_maze.new_state()

	if mode == PUMPKIN:
		return strategy_pumpkin.new_state()

	return strategy_polyculture.new_state()


def _run_mode(state, mode):
	if mode == CACTUS:
		strategy_cactus.grow_world(state[mode])
		return True

	if mode == MAZE:
		return strategy_maze.grow_gold(state[mode])

	if mode == PUMPKIN:
		strategy_pumpkin.grow_world(state[mode])
		return True

	strategy_polyculture.grow_world(state[mode])
	return True


# endregion
