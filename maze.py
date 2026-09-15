# ------------------------------------------------------------------------------
# maze.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Creation


def substance_cost():
	# Return the cost of the largest maze available at this unlock level.
	level = num_unlocked(Unlocks.Mazes)

	if level == 0:
		return 0

	return get_world_size() * 2 ** (level - 1)


def inside_maze():
	# Return whether the drone is currently standing inside a maze.
	entity = get_entity_type()
	return entity == Entities.Hedge or entity == Entities.Treasure


def create_maze():
	# Create the largest maze available at the current unlock level.
	cost = substance_cost()

	if cost == 0:
		quick_print("Mazes are locked.")
		return False

	if get_entity_type() != Entities.Bush and not plant(Entities.Bush):
		quick_print("Stand on an empty tile or bush.")
		return False

	if not use_item(Items.Weird_Substance, cost):
		quick_print("Maze creation failed.")
		return False

	quick_print("Maze created.")
	return True


def reuse_treasure():
	# Collect and relocate the treasure while the maze can still be reused.
	if get_entity_type() != Entities.Treasure:
		return False

	cost = substance_cost()

	if cost == 0:
		return False

	return use_item(Items.Weird_Substance, cost)


# endregion
