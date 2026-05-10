# Building BotaniClone

The pack ships as two zip artifacts produced from one source tree:

| Profile | Output | MC versions | pack_format range |
|---|---|---|---|
| Legacy | `dist/botaniclone-1.20.zip` | 1.20.2 – 1.20.6 | 18 – 41 |
| Modern | `dist/botaniclone-1.21.zip` | 1.21.0 – 26.2 snap | 48 – 105 |

## Prerequisites

* [`uv`](https://github.com/astral-sh/uv) (Python package/runtime manager). Pulls in Python 3.10+.

## One-time setup

```sh
uv sync
```

That installs `beet`, `jinja2`, and `pyyaml` into a project-local `.venv`.

## Building

```sh
uv run beet -p beet-1.20.yaml build
uv run beet -p beet-1.21.yaml build
```

Both can run independently. Each writes to `dist/botaniclone-<profile>.zip`. To rebuild from scratch, delete `dist/` first.

Run a continuous rebuild during development:

```sh
uv run beet -p beet-1.21.yaml watch
```

## Source layout

```
src/
├── data/                                  # raw pack source (always plural folder names)
│   ├── botaniclone/                       # public API
│   │   ├── functions/{load,tick,_use_bonemeal,_migrate}.mcfunction
│   │   ├── tags/functions/{load,tick}.json
│   │   └── advancements/use_bonemeal.json
│   ├── guris/                             # internal helpers
│   │   ├── functions/_interact/*.mcfunction
│   │   ├── loot_tables/*.json             # 13 custom loot tables
│   │   ├── predicates/{bonemeal,is_night}.json
│   │   └── tags/blocks/*.json
│   └── minecraft/tags/functions/{load,tick}.json    # re-points to botaniclone:*
├── tables/
│   ├── blocks.yaml                        # source of truth for plant_check
│   └── options.yaml                       # source of truth for settings menu
└── (no templates needed — handler bodies live in plugins/block_table.py)
```

`plugins/` (sibling to `src/`) holds the Beet plugin code; see "Pipeline" below.

## Adding a block

Append a row to `src/tables/blocks.yaml` and rebuild. No mcfunction or loot-table edits needed for a "drops vanilla loot table" block.

```yaml
- {id: my_new_flower, behavior: spawn_loot, loot: minecraft:blocks/my_new_flower, potted_id: potted_my_new_flower, above: "~ ~1 ~"}
```

For blocks introduced in MC 1.21+ that should be filtered out of the Legacy build, add `min_pack_format: <value>`:

```yaml
- {id: my_new_flower, ..., min_pack_format: 71}   # 1.21.5+
```

If the block needs to be raytrace-discoverable (so the player can target it with bone meal), also add it to `src/data/guris/tags/blocks/non-optionals.json` (or another existing tag).

## Adding an option

Append a row to `src/tables/options.yaml`. The build emits the toggle function, hooks it into the settings menu, and adds a default initialiser automatically.

```yaml
- {key: option_my_thing, default: 0, short: my_thing, label: "My thing",
   on_text: "Enabled", off_text: "Disabled"}
```

Then reference `option_my_thing` from a `blocks.yaml` row's `option_score` field if it gates a plant.

## Pipeline

Each profile YAML lists the plugin pipeline order:

1. **`plugins.legacy_filter`** — reads `blocks.yaml`, drops rows whose `min_pack_format` exceeds the profile's `meta.max_format`. Stashes the filtered list under `ctx.meta["_filtered_blocks"]`.
2. **`plugins.block_table`** — emits `botaniclone:plant_check` (auto-generated dispatcher) plus all `guris:_handler/*` macro handlers.
3. **`plugins.options_table`** — emits `botaniclone:options/default`, `botaniclone:options/toggle/<key>`, and `botaniclone:settings` from `options.yaml`.
4. **`plugins.folder_convention`** — currently a no-op; Beet renames `functions/` ↔ `function/` automatically based on declared pack_format. Reserved for future overrides.
5. **`plugins.pack_meta`** — generates `pack.mcmeta` with primary pack_format plus `supported_formats: { min_inclusive, max_inclusive }`. Modern profile additionally emits the newer `min_format` / `max_format` fields.
6. **`plugins.validate`** — static link check across emitted mcfunctions; aborts the build on a dangling `function ns:X` or `loot ns:X` reference.
7. **`plugins.zip_artifact`** — names the pack so Beet writes `dist/botaniclone-<profile>.zip`.

## Profile config

Profile-specific values live in `meta:` under each profile YAML:

| Key | Used by | Notes |
|---|---|---|
| `meta.profile` | logging | "legacy" or "modern" |
| `meta.artifact_name` | `zip_artifact` | filename stem (sans `.zip`) |
| `meta.pack_format` | `pack_meta` | declared pack_format (primary) |
| `meta.min_format` | `pack_meta` | low end of supported_formats range |
| `meta.max_format` | `pack_meta`, `legacy_filter` | high end of supported range; also the filter threshold |
| `meta.use_min_max_fields` | `pack_meta` | also emit `min_format`/`max_format` fields (25w31a+ form) |
| `meta.blocks_table` | `legacy_filter`, `block_table` | path to blocks YAML |

## Updating pack_format ranges

When a new MC version ships (e.g. 26.2 promoted from snapshot to stable):

1. Look up the new `pack_format` on [the wiki](https://minecraft.wiki/w/Pack_format).
2. Update `meta.max_format` (and possibly `meta.pack_format` if you want the primary to bump too) in `beet-1.21.yaml`.
3. Rebuild.

For new flora introduced in that version, append rows to `blocks.yaml` with `min_pack_format` set to the new format value.
