# The Farmer Was Replaced — Solutions

<p align="center">
  <a href="https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/">
    <img
      src="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2060160/a93cdbf3f795ca7736dca7fde208c5cd5fcf2a9e/header.jpg"
      alt="The Farmer Was Replaced"
      width="460"
    >
  </a>
</p>

Inventory-driven farming automation for
[*The Farmer Was Replaced*](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/),
written for the game's Python-like programming environment.

> [!WARNING]
> This repository contains progression and puzzle spoilers. Discovering your
> own solutions is a large part of the game, so browse accordingly.

<table align="center">
  <thead>
    <tr>
      <th align="left">Repository progression</th>
      <th align="left">In-game progression</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">
  <a href="movement.py"><img src="https://img.shields.io/badge/Movement-ready-2ea44f?style=flat" alt="Movement: ready" height="24"></a><br>
  <a href="inventory.py"><img src="https://img.shields.io/badge/Inventory-ready-2ea44f?style=flat" alt="Inventory: ready" height="24"></a><br>
  <a href="strategy_carrot.py"><img src="https://img.shields.io/badge/Carrots-ready-2ea44f?style=flat" alt="Carrots: ready" height="24"></a><br>
  <a href="strategy_pumpkin.py"><img src="https://img.shields.io/badge/Pumpkins-active-0969da?style=flat" alt="Pumpkins: active" height="24"></a><br>
  <a href="crop_care.py"><img src="https://img.shields.io/badge/Crop%20care-ready-2ea44f?style=flat" alt="Crop care: ready" height="24"></a><br>
  <a href="strategy_polyculture.py"><img src="https://img.shields.io/badge/Polyculture-experimental-d97706?style=flat" alt="Polyculture: experimental" height="24"></a>
      </td>
      <td valign="top">
  <img src="https://img.shields.io/badge/Grass-Lv%206-0969da?style=flat" alt="Grass level 6" height="24"><br>
  <img src="https://img.shields.io/badge/Speed-Lv%205-0969da?style=flat" alt="Speed level 5" height="24"><br>
  <img src="https://img.shields.io/badge/Farm%20size-Lv%207-0969da?style=flat" alt="Farm size level 7" height="24"><br>
  <img src="https://img.shields.io/badge/Carrots-Lv%205-0969da?style=flat" alt="Carrots level 5" height="24"><br>
  <img src="https://img.shields.io/badge/Trees-Lv%206-0969da?style=flat" alt="Trees level 6" height="24"><br>
  <img src="https://img.shields.io/badge/Watering-Lv%205-0969da?style=flat" alt="Watering level 5" height="24"><br>
  <img src="https://img.shields.io/badge/Pumpkins-Lv%205-0969da?style=flat" alt="Pumpkins level 5" height="24"><br>
  <img src="https://img.shields.io/badge/Fertilizer-Lv%204-0969da?style=flat" alt="Fertilizer level 4" height="24"><br>
  <img src="https://img.shields.io/badge/Cactus-Lv%202-0969da?style=flat" alt="Cactus level 2" height="24"><br>
  <img src="https://img.shields.io/badge/Polyculture-unlocked-2ea44f?style=flat" alt="Polyculture unlocked" height="24"><br>
  <img src="https://img.shields.io/badge/Sunflowers-unlocked-2ea44f?style=flat" alt="Sunflowers unlocked" height="24"><br>
  <img src="https://img.shields.io/badge/Mazes-locked-6e7781?style=flat" alt="Mazes locked" height="24"><br>
  <img src="https://img.shields.io/badge/Dinosaurs-locked-6e7781?style=flat" alt="Dinosaurs locked" height="24"><br>
  <img src="https://img.shields.io/badge/Megafarm-locked-6e7781?style=flat" alt="Megafarm locked" height="24"><br>
  <img src="https://img.shields.io/badge/Simulation-locked-6e7781?style=flat" alt="Simulation locked" height="24"><br>
  <img src="https://img.shields.io/badge/Leaderboards-locked-6e7781?style=flat" alt="Leaderboards locked" height="24">
      </td>
    </tr>
  </tbody>
</table>

The in-game badges reflect the unlock data in the current save. Repository
badges describe automation maturity instead, so an unlocked crop may still
need a complete farming strategy.

## Current automation

The active program grows giant pumpkins when the carrot reserve is healthy.
When carrots fall below their configured target, it delegates to the compact
polyculture strategy to rebuild supporting inventory first.

```text
main.py
└── strategy_pumpkin.py
    ├── strategy_polyculture.py  when carrots are below target
    └── pumpkin_field.py         when pumpkin farming can proceed
```

The current system includes:

- Inventory-relative crop selection for hay, wood, carrots, and power
- A compact active field that avoids traversing every tile unnecessarily
- Companion-crop requests with bounded queues, FIFO ordering, and collision
  fallbacks
- Water and fertilizer care that preserves configured inventory reserves
- Exact crop planting separated from strategy-level crop selection
- Full-field pumpkin initialization followed by sparse pending-tile revisits
- Dead-pumpkin replacement without harvesting individually mature pumpkins
- Wraparound-aware coordinate movement using the shorter route

Polyculture is intentionally marked experimental. Its state and retry rules
are implemented, but crop density, care economics, and long-running recovery
still need observation and tuning in the game.

## Architecture

The project stays flat because the game save editor exposes files directly.
Filename prefixes and focused responsibilities provide the structure that
packages normally would.

| File | Responsibility |
| --- | --- |
| `main.py` | Selects and repeatedly runs the active top-level strategy |
| `strategy_pumpkin.py` | Coordinates giant-pumpkin farming and carrot recovery |
| `strategy_polyculture.py` | Selects inventory needs and advances one bounded polyculture pass |
| `strategy_carrot.py` | Provides the standalone full-field carrot strategy |
| `pumpkin_field.py` | Scans the world and revisits unresolved pumpkin coordinates |
| `pumpkin_tile.py` | Resolves planting, death, maturity, and care for one pumpkin tile |
| `polyculture_field.py` | Owns crop memory, worksets, queues, and companion requests |
| `polyculture_tile.py` | Plants companions and resolves source/target tile interactions |
| `crop_care.py` | Applies water and bounded fertilizer while preserving reserves |
| `planter.py` | Performs exact planting and required ground preparation |
| `movement.py` | Moves to coordinates using wraparound-aware shortest paths |
| `inventory.py` | Defines stock targets and inventory-relative queries |

The boundaries follow a simple rule: strategies decide *what is worthwhile*,
field modules remember *what needs work*, tile modules decide *what the current
tile requires*, and shared services perform primitive actions.

## State model

Pumpkin and polyculture farming deliberately use different memories:

- Pumpkin state records whether each coordinate has been confirmed as a
  living, mature pumpkin during the current giant-pumpkin cycle.
- Polyculture state records managed crops, scheduled crop work, companion
  targets, per-target FIFO queues, and each source crop's outstanding request.

Both models use `state[x][y]` orientation. Work added during a pass waits for
the next pass, keeping each scheduler iteration bounded and inspectable.

## Inventory policy

Desired stock levels live in `inventory.TARGET`. Strategies compare current
inventory against those targets instead of relying on fixed crop rotations.
The polyculture strategy selects the supported resource with the lowest target
ratio, while water and fertilizer are consumed only above their own reserves.

Adjust the values in `inventory.py` to match the scale of your farm and the
resources you want to protect.

## Usage

1. Place or clone the repository files in a game save folder.
2. Open the whole save folder in VS Code rather than opening one file alone.
3. Set the desired stock levels in `inventory.py`.
4. Select the top-level strategy imported by `main.py`.
5. Load the save after externally creating or deleting game files, then run
   `main.py` in the game.

The scripts target the game's Python-like language and built-in farming API;
they are not intended to run as ordinary standalone Python programs.

## Conventions

- Keep the project flat and use descriptive filename prefixes such as
  `strategy_`.
- Use ordinary `#` comments instead of triple-quoted docstrings.
- Keep code close to 80 characters wide and use tabs for indentation.
- Prefer explicit loops and `state[x][y]` for nested world state.
- Add abstractions only when they own real policy or reusable behavior.

## Roadmap

- Add concise CLI visualizations for pumpkin and polyculture memory
- Tune the compact polyculture field through longer in-game runs
- Verify whether mature surviving pumpkins can die later in the same cycle
- Refine fertilizer use according to its strategic inventory value
- Optimize pending-coordinate routing only after behavior is reliable

Suggestions and alternative strategies are welcome. Keep additions focused so
they can compose with the existing movement, planting, care, and inventory
modules.
