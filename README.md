# The Farmer Was Replaced — Solutions

A collection of my automation scripts and solutions for
[*The Farmer Was Replaced*](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/).

The code is written for the game's Python-like programming environment and is
organized into small modules for farming, planting, movement, and inventory
management.

> [!WARNING]
> These scripts contain puzzle and progression spoilers. Experimenting and
> discovering your own solutions is a big part of the game—browse accordingly.

## Current solution

The repository currently focuses on growing giant pumpkins across the entire
field. The automation:

- Plants and waters pumpkins on every tile
- Detects and replaces dead pumpkins
- Revisits only tiles that are not ready
- Harvests once the whole field has matured
- Uses wraparound-aware movement to take the shortest route to a tile

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Entry point that repeatedly runs the active farming strategy |
| `giant_pumpkin.py` | Coordinates planting, recovery, and harvesting for a field-sized pumpkin |
| `planter.py` | Provides reusable planting and ground-preparation helpers |
| `movement.py` | Moves the drone to coordinates using the shortest wraparound path |
| `inventory.py` | Defines inventory targets and helper queries for resource balancing |

## Usage

1. Create matching code files in *The Farmer Was Replaced*.
2. Copy each script from this repository into its corresponding in-game file.
3. Open `main.py` and select the farming behavior you want to run.
4. Start the program in the game.

The scripts rely on in-game names such as `Items`, `Entities`, `Grounds`, and
`Hats`; they are not intended to run with a standard Python interpreter.

## Customization

Resource goals live in the `TARGET` mapping in `inventory.py`. Adjust those
values to suit your progression and preferred stockpile sizes. You can also
switch the strategy called from `main.py` as more solutions are added.

## Contributing

Suggestions, improvements, and alternative solutions are welcome. If you add a
strategy, keep it focused and reusable so it can be combined with the existing
movement, planting, and inventory helpers.

Have fun automating the farm!
