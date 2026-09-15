from __builtins__ import *

import movement
import planter

# region Farming


def grow_world():
    # Grow and harvest one world-sized giant pumpkin.
    size = get_world_size()
    state = _new_state(size)

    pending = _scan_world(state, size)

    while pending:
        pending = _check_pending(state, pending)

    harvest()


# endregion


# region Field state


def _new_state(size):
    # state[x][y] is True once that tile is confirmed ready.
    state = []

    for x in range(size):
        column = []

        for y in range(size):
            column.append(False)

        state.append(column)

    return state


def _scan_world(state, size):
    # Perform the initial full-field pass.
    pending = []

    for _ in range(size):
        for _ in range(size):
            x = get_pos_x()
            y = get_pos_y()

            if _tend_tile():
                state[x][y] = True
            else:
                pending.append((x, y))

            move(North)

        move(East)

    return pending


def _check_pending(state, pending):
    # Revisit only unresolved coordinates.
    next_pending = []

    for x, y in pending:
        movement.move_to(x, y)

        if _tend_tile():
            state[x][y] = True
        else:
            next_pending.append((x, y))

    return next_pending


# endregion


# region Tile handling


def _tend_tile():
    # True means this tile has a mature living pumpkin.
    entity = get_entity_type()

    if entity == Entities.Dead_Pumpkin:
        planter.plant_pumpkin()
        _water()
        return False

    if entity != Entities.Pumpkin:
        if can_harvest():
            harvest()

        planter.plant_pumpkin()
        _water()
        return False

    if can_harvest():
        return True

    _water()
    return False


def _water():
    if get_water() < 0.1 and num_items(Items.Water) > 0:
        use_item(Items.Water)


# endregion
