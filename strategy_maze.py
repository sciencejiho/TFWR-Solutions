# ------------------------------------------------------------------------------
# strategy_maze.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import inventory
import maze
import maze_solver

# region Farming strategy


def new_state():
	# Create persistent passage data for the active maze.
	return {"solver": maze_solver.new_state()}


def can_start():
	# Return whether a maze can be created without spending its reserve.
	return _can_spend_substance()


def grow_gold(state):
	# Collect or relocate one treasure while preserving substance reserves.
	if state["solver"]["size"] != get_world_size():
		state["solver"] = maze_solver.new_state()

	if not maze.inside_maze():
		if not _can_spend_substance() or not maze.create_maze():
			return False

		state["solver"] = maze_solver.new_state()

	solver = state["solver"]

	if not solver["mapped"] and not maze_solver.map_maze(solver):
		return False

	if not maze_solver.move_to_treasure(solver):
		return False

	if not _can_spend_substance():
		return _harvest_and_reset(state)

	if maze.reuse_treasure():
		return True

	return _harvest_and_reset(state)


def finish(state):
	# Collect the active treasure before another strategy clears the field.
	if not maze.inside_maze():
		state["solver"] = maze_solver.new_state()
		return True

	if state["solver"]["size"] != get_world_size():
		state["solver"] = maze_solver.new_state()

	solver = state["solver"]

	if not solver["mapped"] and not maze_solver.map_maze(solver):
		return False

	if not maze_solver.move_to_treasure(solver):
		return False

	return _harvest_and_reset(state)


def _harvest_and_reset(state):
	if not harvest():
		return False

	state["solver"] = maze_solver.new_state()
	return True


def _can_spend_substance():
	cost = maze.substance_cost()

	if cost == 0:
		return False

	reserve = inventory.target_amount(Items.Weird_Substance)
	return num_items(Items.Weird_Substance) >= reserve + cost


# endregion
