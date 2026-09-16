# ------------------------------------------------------------------------------
# strategy_maze.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import drone_control
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
	# Keep one mapped maze active until another resource needs the field.
	if state["solver"]["size"] != get_world_size():
		state["solver"] = maze_solver.new_state()

	if not maze.inside_maze():
		if not _can_spend_substance() or not maze.create_maze():
			return False

		state["solver"] = maze_solver.new_state()

	solver = state["solver"]

	if not solver["mapped"] and not maze_solver.map_maze(solver):
		return False

	if not _run_station_swarm(solver):
		solver["mapped"] = False
		return False

	state["solver"] = maze_solver.new_state()
	return True


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


def _run_station_swarm(solver):
	count = min(max_drones(), solver["size"] * solver["size"])
	plan = maze_solver.create_station_plan(solver, count)
	jobs = []

	for index in range(len(plan["stations"])):
		jobs.append((solver, plan, index))

	results = drone_control.run_jobs(_farm_station, jobs)

	for result in results:
		if not result:
			return False

	return True


def _farm_station(job):
	solver, home_plan, index = job
	station_x, station_y = home_plan["stations"][index]

	if not maze_solver.move_to_position(solver, station_x, station_y):
		return False

	while maze.inside_maze():
		target = measure()

		if target == None:
			return True

		target_x, target_y = target
		# Immutable home sectors keep copied workers in election agreement.
		owner = maze_solver.closest_station(
			home_plan,
			target_x,
			target_y,
		)
		spread_plan = maze_solver.spread_station_plan(
			solver,
			len(home_plan["stations"]),
			target_x,
			target_y,
			owner,
		)

		if spread_plan == None:
			return False

		station_x, station_y = spread_plan["stations"][index]

		if not maze_solver.move_to_position(solver, station_x, station_y):
			return False

		if owner != index:
			continue

		if get_entity_type() != Entities.Treasure:
			continue

		if _should_reuse_treasure() and maze.reuse_treasure():
			continue

		return harvest()

	return True


def _should_reuse_treasure():
	if not inventory.below_target(Items.Gold):
		return False

	for item in inventory.FARM_TARGET:
		if item == Items.Gold:
			continue

		if inventory.needs_refill(item):
			return False

	return _can_spend_substance()


def _can_spend_substance():
	cost = maze.substance_cost()

	if cost == 0:
		return False

	reserve = inventory.target_amount(Items.Weird_Substance)
	return num_items(Items.Weird_Substance) >= reserve + cost


# endregion
