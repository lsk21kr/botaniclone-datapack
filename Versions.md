# Version History

## v2.0.0-wip (2026-05-10, in progress)

### Added
* Multi-MC-version build pipeline. Single source tree under `src/` produces two release zips:
  * `dist/botaniclone-1.20.zip` — Legacy build (pack_format 18–41, MC 1.20.2 – 1.20.6)
  * `dist/botaniclone-1.21.zip` — Modern build (pack_format 48–105, MC 1.21.0 – 26.2 snapshot)
* New flora support (Modern build only — auto-filtered out of Legacy):
  * **1.21.4** — pale oak leaves → pale oak sapling (incl. potted), pale moss carpet, pale hanging moss, closed/open eyeblossom (incl. potted)
  * **1.21.5** — leaf litter, cactus flower, short dry grass, tall dry grass
  * **26.1** — golden dandelion (incl. potted; default off, craft-only)
* New `Eyeblossom mode` drop-mode option (default on, 1.21.4+ only) — when on, bone mealing eyeblossoms drops the variant matching the current time of day (night → open, day → closed). When off, drops match the source block.
* New `Golden dandelion` plant-gate option (default off, 26.1+ only).
* `is_night` predicate (used by eyeblossom drop-mode) — `minecraft:time_check`.
* Build-time validator plugin — fails the build on dangling function or loot-table references.

### Changed
* Source tree restructured. Source under `src/data/<namespace>/...`; build artifacts under `dist/`. The repo-root README/Versions/License files are unchanged in location.
* Public API moved to a new `botaniclone:` namespace (`/function botaniclone:settings`, `botaniclone:plant_check`, `botaniclone:options/toggle/<key>`, etc.). Internal helpers — interaction logic, raytrace, handler macros — remain under `guris:` (now flat: `guris:_interact/*`, `guris:_handler/*`, `guris:_options/*`).
* The 240-line `plant_check.mcfunction` is now auto-generated from `src/tables/blocks.yaml` (one row per trigger block) into a thin orchestrator that delegates to per-behavior macro handlers.
* Settings menu and option toggle commands are auto-generated from `src/tables/options.yaml`.
* Modern build uses singular folder names (`function/`, `loot_table/`, `predicate/`, `tags/block/`, `tags/function/`, `advancement/`) per the 1.21+ pack-format convention. Legacy build keeps the plural form. Beet handles the rename automatically based on declared pack_format.
* `pack.mcmeta` now carries a `supported_formats` range (since pack_format 16) so a single zip loads cleanly across its target range. The Modern build also emits `min_format` / `max_format` (the 25w31a+ form recommended for pack_format 88+).

### Migration notes (upgrading from v1.0)
* Per-world option choices are preserved across the upgrade. The scoreboard objectives (`guris.botani`, `guris.pid`) and option score names (`option_ancient`, `option_witherrose`, `option_modeloot`, etc.) are unchanged.
* The advancement ID changed from `guris:botani/use_bonemeal` to `botaniclone:use_bonemeal`. Players will need to bone-meal once after the upgrade to re-trigger; harmless.
* `option_shroomlight` was removed in v1.0 (merged into `option_fungus`); this release additionally removes its leftover read in `plant_raytrace`.

## v1.0 (2023-07-05)
* Added
  * Hanging root replication
* Changed
  * Options command is relocated to `guris:botani/settings`
  * Slightly increased size of interaction so that users can interact easily
* Removed
  * Option for nether roots (purely decorational, no balance impact)
  * Option for shroomlight is merged into option for fungi
* Others
  * Code cleanup

## v0.1 (2023-07-03)
* Added
  * Plant replication for small flowers, pitcher plant, torchflower, cactus, dead bush, lily pad, moss carpet, crimson roots, warped roots, nether sprouts, nether wart, shroomlight, spore blossom, sugar cane, tall grass, tall seagrass, large fern, and vine
  * Potted plant replication for small flowers, saplings, bushes, propagule, bamboo, cactus, dead bush, fern, crimson fungus, warped fungus, brown mushroom, red mushroom, crimson roots, and warped roots
  * Tree-like plant replication for oak, spruce, birch, jungle, acacia, dark oak, cherry leaves for saplings, azalea / flowering azalea leaves for bushes, mangrove propagule for mangrove propagule, nether wart block for crimson fungus, warped wart block for warped fungus, and brown / red mushroom block for mushrooms
  * Chorus flower de-aging
  * Options for balancing: ancient plants, nether roots, nether wart, shroomlight, wither rose, trees, fungi, mushroom, chorus de-aging, potted plants, loot mode, tall grass mode
