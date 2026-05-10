# BotaniClone

Bone meal any plants and replicate them. You can bone meal small flowers, potted flowers, cactus, chorus flower, sugar cane, vine, even dead bush, and more.

## Dev Status
* 🟦 **Active**: Actively developing. Working properly.
* **Version**: v2.0.0-wip

## Compatibility

Two builds are produced from a single source tree. Each ships as its own zip in `dist/`:

| Build | Minecraft versions | pack_format range | Filename |
|---|---|---|---|
| Legacy | 1.20.2 — 1.20.6 | 18 — 41 | `dist/botaniclone-1.20.zip` |
| Modern | 1.21.0 — 26.2 (snapshot) | 48 — 105 | `dist/botaniclone-1.21.zip` |

Multiplayer-friendly. Per-player interaction matching is preserved.

## Features
### Plant replication
Use bone meal on various non-bone-meal-able plants to replicate them. (\* Options are provided for balancing purposes.)
* Small flowers: dandelion, poppy, blue orchid, allium, azure bluet, red tulip, orange tulip, white tulip, pink tulip, oxeye daisy, cornflower, lily of the valley, and wither rose\*
* Ancient plants\*: pitcher plant, torchflower
* Cactus
* Dead bush (how?)
* Lily pad
* Hanging roots
* Moss carpet
* Nether roots: crimson roots, warped roots, and nether sprouts
* Nether wart\*
* Spore blossom
* Sugar cane
* Tall grasses: tall grass, tall seagrass, and large fern
* Vine

#### New in v2.0 (Modern build only)
* **1.21.4** — pale oak leaves → pale oak sapling, pale moss carpet, pale hanging moss, closed/open eyeblossom (with new drop-mode option)
* **1.21.5** — leaf litter, cactus flower, short dry grass, tall dry grass
* **26.1** — golden dandelion\* (default off; craft-only flower)

Use bone meal on potted plants\* to replicate them.
* Potted flowers: dandelion, poppy, blue orchid, allium, azure bluet, red tulip, orange tulip, white tulip, pink tulip, oxeye daisy, cornflower, lily of the valley, wither rose, golden dandelion (Modern, 26.1+)
* Potted saplings, bushes, propagule: oak sapling, spruce sapling, birch sapling, jungle sapling, acacia sapling, dark oak sapling, cherry sapling, azalea bush, flowering azalea bush, mangrove propagule, pale oak sapling (Modern, 1.21.4+)
* Potted bamboo
* Potted cactus
* Potted dead bush
* Potted fern
* Potted fungi: crimson fungus, warped fungus
* Potted mushrooms: brown mushroom, red mushroom
* Potted nether roots: crimson roots, warped roots
* Potted eyeblossom: closed/open (Modern, 1.21.4+)

Use bone meal on various leaves to get saplings. (Wart blocks for fungi, mushroom blocks for mushrooms, and mangrove propagule for mangrove propagule)
* Leaves and propagule\*: oak, spruce, birch, jungle, acacia, dark oak, cherry, azalea, flowering azalea leaves, mangrove propagule, **pale oak leaves (Modern, 1.21.4+)**
* Fungi\*: nether wart block, warped wart block, and shroomlight
* Mushrooms\*: brown mushroom block, red mushroom block

### Chorus flower de-aging
Use bone meal on a chorus flower to lower the age value.\*

### Balancing Options
Use commands or click menu on chat to toggle the options. Defaults in parentheses. Run `/function botaniclone:settings` to evoke the menu.

* Replication of certain plants
  * Ancient plants (off)
  * Nether wart (off)
  * Wither rose (off)
  * **Golden dandelion (off)** — Modern only
* Replication of tree-like plants
  * Leaves/saplings/bushes/propagule (on)
  * Wart blocks/fungi/shroomlight (on)
  * Mushroom blocks/mushrooms (on)
* Chorus flower de-aging (on)
* Replication of potted plants (on)
* Drop modes
  * **Loot mode (on)**: When on, bone mealing drops items based on the block loot table. For example, bone mealing oak leaves drops a sapling at low chance plus sticks and apples. When off, always drop items of the same kind.
  * **Tall grass mode (on)**: When on, bone mealing on tall grasses drops items of the same tall grasses. When off, normal grasses are dropped as tall grass, and large fern are not normally obtainable in survival mode.
  * **Eyeblossom mode (on)** — Modern only: When on, bone mealing eyeblossoms drops the variant matching the current time of day (open at night, closed at day). When off, drops match the source block.

## Planned Features (Soon™)
* Bone mealing using dispensers
* Inventory mode option for dropping loot straight to inventory
* Make only natural alive leaves bone-meal-able (and option)

## Building from source

The pack is generated from `src/` by a Beet build pipeline. See [BUILD.md](BUILD.md) for full instructions. The short version:

```sh
uv sync
uv run beet -p beet-1.20.yaml build   # produces dist/botaniclone-1.20.zip
uv run beet -p beet-1.21.yaml build   # produces dist/botaniclone-1.21.zip
```

## References
* [PuckiSilver's Multitool](https://www.planetminecraft.com/data-pack/multitool-every-tool-in-one-item/) data pack for targeted block ray tracing
* [Moggla's Timber](https://www.planetminecraft.com/data-pack/timber-datapack/) data pack for settings menu design
* [How to use Interaction Entities in Minecraft](https://youtu.be/06L_PgABKnU) for interaction usage

## Version history
* v0.1: initial release
* v1.0: Hanging root replication added, some options are removed
* v2.0.0-wip: Heavy refactor — data-driven block + option tables, multi-MC-version build pipeline (Legacy 1.20.2–1.20.6, Modern 1.21.0–26.2 snap), new flora coverage (pale oak/eyeblossom/leaf litter/cactus flower/dry grasses/golden dandelion), new eyeblossom drop-mode option
