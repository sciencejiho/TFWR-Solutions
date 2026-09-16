# ------------------------------------------------------------------------------
# drone_control.py
# ------------------------------------------------------------------------------

from __builtins__ import *

import movement

# region Job control


def run_jobs(worker, jobs, starts=None):
	# Run copied jobs across available drones and preserve result order.
	results = []

	for _ in jobs:
		results.append(None)

	next_job = 0

	for _ in range(len(jobs)):
		if next_job >= len(jobs):
			return results

		handles = []
		available = max_drones() - num_drones()

		for _ in range(available):
			if next_job >= len(jobs):
				break

			start = None

			if starts != None:
				start = starts[next_job]

			drone = spawn_at(worker, jobs[next_job], start)

			if drone == None:
				break

			handles.append((next_job, drone))
			next_job += 1

		if next_job < len(jobs):
			_move_to_start(starts, next_job)
			results[next_job] = worker(jobs[next_job])
			next_job += 1

		for index, drone in handles:
			results[index] = wait_for(drone)

	return results


def spawn_at(worker, job, start=None):
	# Spawn one copied job after positioning the controller if requested.
	if start != None:
		x, y = start
		movement.move_to(x, y)

	return spawn_drone(worker, job)


def _move_to_start(starts, index):
	if starts == None:
		return

	x, y = starts[index]
	movement.move_to(x, y)


# endregion
