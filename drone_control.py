# ------------------------------------------------------------------------------
# drone_control.py
# ------------------------------------------------------------------------------

from __builtins__ import *

# region Job control


def run_jobs(worker, jobs):
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

			drone = spawn_drone(worker, jobs[next_job])

			if drone == None:
				break

			handles.append((next_job, drone))
			next_job += 1

		if next_job < len(jobs):
			results[next_job] = worker(jobs[next_job])
			next_job += 1

		for index, drone in handles:
			results[index] = wait_for(drone)

	return results


# endregion
