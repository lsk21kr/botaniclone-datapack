"""Reads src/tables/blocks.yaml and generates the dispatcher + handler macros.

The 240-line plant_check.mcfunction reduces to:
- one auto-generated `botaniclone:plant_check` orchestrator
- one auto-generated handler macro per behavior under `guris:_handler/<behavior>`
- one universal drop sink `guris:_handler/_drop`
- the existing `guris:_interact/effect` (hand-written, ports interaction_effect)

Block rows live in `src/tables/blocks.yaml`. Adding a block = one new row.

Pipeline order: legacy_filter runs FIRST and stashes the filtered list under
ctx.meta["_filtered_blocks"]. If absent, this plugin re-reads the YAML directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from beet import Context, Function

# ---- handler macro bodies ----------------------------------------------------
# Macro vars used:
#   id              — block id (no namespace)
#   state           — optional blockstate suffix, e.g. "[age=4]" or ""
#   pos             — "~ ~ ~" or "~ ~1 ~" or "~ ~-1 ~" (selects which pass)
#   loot            — primary loot table id
#   loot2           — alternate loot (modeloot off, or sapling for leaves)
#   loot_tall       — tall-mode loot
#   loot_short      — short-mode loot
#   loot_day        — eye mode time-based, daytime
#   loot_night      — eye mode time-based, nighttime
#   potted          — potted variant id (without minecraft:); empty = no potted check
#
# All execute lines start with `$` (macro) so the substitutions actually expand.

HANDLER_SPAWN_LOOT = """
$execute if block $(pos) minecraft:$(id)$(state) run function guris:_handler/_drop {loot:"$(loot)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) run function guris:_handler/_drop {loot:"$(loot)"}
""".strip()

HANDLER_SPAWN_LOOT_NOPOT = """
$execute if block $(pos) minecraft:$(id)$(state) run function guris:_handler/_drop {loot:"$(loot)"}
""".strip()

HANDLER_SPAWN_LOOT_POTTED_ONLY = """
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) run function guris:_handler/_drop {loot:"$(loot)"}
""".strip()

# pitcher_plant / pitcher_crop[age=4]: drop is the result of mining the lower
# half. Block-state-aware via [half=upper]/[half=lower]; the dispatcher already
# gated on age (for pitcher_crop) or block id (for pitcher_plant), so the bare
# half= predicate is sufficient.
HANDLER_SPAWN_PITCHER = """
$execute if block $(pos) minecraft:$(id)[half=upper] positioned $(pos) run function guris:_handler/_mine_below
$execute if block $(pos) minecraft:$(id)[half=lower] positioned $(pos) run function guris:_handler/_mine_self
""".strip()

HANDLER_SPAWN_LOOT_ALT = """
$execute if block $(pos) minecraft:$(id)$(state) if score option_modeloot guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot)"}
$execute if block $(pos) minecraft:$(id)$(state) unless score option_modeloot guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot2)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) if score option_modeloot guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) unless score option_modeloot guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot2)"}
""".strip()

HANDLER_SPAWN_LOOT_MODE_TALL = """
$execute if block $(pos) minecraft:$(id) if score option_modetall guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot_tall)"}
$execute if block $(pos) minecraft:$(id) unless score option_modetall guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot_short)"}
""".strip()

HANDLER_SPAWN_LOOT_MODE_EYE = """
$execute if block $(pos) minecraft:$(id) if score option_modeeye guris.botani matches 1 if predicate guris:is_night run function guris:_handler/_drop {loot:"$(loot_night)"}
$execute if block $(pos) minecraft:$(id) if score option_modeeye guris.botani matches 1 unless predicate guris:is_night run function guris:_handler/_drop {loot:"$(loot_day)"}
$execute if block $(pos) minecraft:$(id) unless score option_modeeye guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) if score option_modeeye guris.botani matches 1 if predicate guris:is_night run function guris:_handler/_drop {loot:"$(loot_night)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) if score option_modeeye guris.botani matches 1 unless predicate guris:is_night run function guris:_handler/_drop {loot:"$(loot_day)"}
$execute if score option_potted guris.botani matches 1 if block $(pos) minecraft:$(potted) unless score option_modeeye guris.botani matches 1 run function guris:_handler/_drop {loot:"$(loot)"}
""".strip()

# chorus_deage: lower the [age=N] state by 1, for N in 1..5. Skipped when [age=0].
HANDLER_CHORUS_DEAGE = """
$execute if block $(pos) minecraft:chorus_flower[age=1] positioned $(pos) run setblock ~ ~ ~ minecraft:chorus_flower[age=0] replace
$execute if block $(pos) minecraft:chorus_flower[age=2] positioned $(pos) run setblock ~ ~ ~ minecraft:chorus_flower[age=1] replace
$execute if block $(pos) minecraft:chorus_flower[age=3] positioned $(pos) run setblock ~ ~ ~ minecraft:chorus_flower[age=2] replace
$execute if block $(pos) minecraft:chorus_flower[age=4] positioned $(pos) run setblock ~ ~ ~ minecraft:chorus_flower[age=3] replace
$execute if block $(pos) minecraft:chorus_flower[age=5] positioned $(pos) run setblock ~ ~ ~ minecraft:chorus_flower[age=4] replace
$execute if block $(pos) minecraft:chorus_flower unless block $(pos) minecraft:chorus_flower[age=0] run function guris:_interact/effect
""".strip()

DROP_SINK = """
$loot spawn ~ ~ ~ loot $(loot)
function guris:_interact/effect
""".strip()

# Pitcher plant: mine one block below current position, drop at current.
MINE_BELOW = """
loot spawn ~ ~ ~ mine ~ ~-1 ~ mainhand
function guris:_interact/effect
""".strip()

# Pitcher plant: mine current block, drop at current.
MINE_SELF = """
loot spawn ~ ~ ~ mine ~ ~ ~ mainhand
function guris:_interact/effect
""".strip()


# ---- main entry --------------------------------------------------------------

def beet_default(ctx: Context):
    target_format = int(ctx.meta.get("pack_format", 0))
    if not target_format:
        raise ValueError("meta.pack_format missing — set in profile yaml")

    # Use filtered list from legacy_filter if present; else load fresh.
    blocks = ctx.meta.get("_filtered_blocks")
    if blocks is None:
        table_path = Path(ctx.directory) / ctx.meta["blocks_table"]
        raw = yaml.safe_load(table_path.read_text(encoding="utf-8")) or []
        blocks = [b for b in raw if int(b.get("min_pack_format", 0)) <= target_format]

    # 1. Emit handlers
    ctx.data["guris:_handler/spawn_loot"] = Function(HANDLER_SPAWN_LOOT)
    ctx.data["guris:_handler/spawn_loot_nopot"] = Function(HANDLER_SPAWN_LOOT_NOPOT)
    ctx.data["guris:_handler/spawn_loot_potted_only"] = Function(HANDLER_SPAWN_LOOT_POTTED_ONLY)
    ctx.data["guris:_handler/spawn_loot_alt"] = Function(HANDLER_SPAWN_LOOT_ALT)
    ctx.data["guris:_handler/spawn_loot_mode_tall"] = Function(HANDLER_SPAWN_LOOT_MODE_TALL)
    ctx.data["guris:_handler/spawn_loot_mode_eye"] = Function(HANDLER_SPAWN_LOOT_MODE_EYE)
    ctx.data["guris:_handler/spawn_pitcher"] = Function(HANDLER_SPAWN_PITCHER)
    ctx.data["guris:_handler/chorus_deage"] = Function(HANDLER_CHORUS_DEAGE)
    ctx.data["guris:_handler/_drop"] = Function(DROP_SINK)
    ctx.data["guris:_handler/_mine_below"] = Function(MINE_BELOW)
    ctx.data["guris:_handler/_mine_self"] = Function(MINE_SELF)

    # 2. Build dispatch lines for both passes
    pass1 = ["# Auto-generated by plugins.block_table — do not edit by hand.",
             "# Pass 1: ground (~ ~ ~)"]
    pass2 = ["# Pass 2: above-offset (typically ~ ~1 ~)"]

    for row in blocks:
        line = build_dispatch_line(row, pass_=1)
        if line:
            pass1.append(line)

    for row in blocks:
        line = build_dispatch_line(row, pass_=2)
        if line:
            pass2.append(line)

    plant_check = (
        pass1
        + ["execute if score @e[type=interaction,sort=nearest,limit=1] guris.botani matches 1 run return 0"]
        + pass2
    )
    ctx.data["botaniclone:plant_check"] = Function(plant_check)


# ---- helpers -----------------------------------------------------------------

def build_dispatch_line(row: dict[str, Any], pass_: int) -> str | None:
    """Compose a single `function guris:_handler/<behavior> {args}` line for a row.

    pass_ == 1: ground level (pos="~ ~ ~"). Always emit if the row exists.
    pass_ == 2: above offset. Emit only if `above` is set.
                Wraps with `unless block ~ ~ ~ <id>` to avoid double-firing
                when the same block occupies the ground slot.
    """
    behavior = row["behavior"]
    block_id = row["id"]
    state = row.get("blockstate", "") or ""
    above = row.get("above")  # offset string or None
    option_score = row.get("option_score")  # str or None
    potted_id = row.get("potted_id", "") or ""
    potted_only = bool(row.get("potted_only", False))

    if pass_ == 1:
        pos = "~ ~ ~"
        prefix_unless = ""
    else:  # pass 2
        if not above:
            return None
        pos = above
        # Avoid double-fire when same block was already matched in pass 1.
        # potted-only rows have no ground form, so no unless-guard needed.
        if not potted_only:
            prefix_unless = f"unless block ~ ~ ~ minecraft:{block_id}{state}"
        else:
            prefix_unless = ""

    # Build macro args dict (NBT compound literal)
    args = build_macro_args(row, pos)
    args_str = "{" + ",".join(f'{k}:"{v}"' for k, v in args.items()) + "}"

    # Compose final line. Match the original dispatcher's clause order:
    # execute [if score OPT...] [unless block ...] [if block ...] run function ...
    parts = ["execute"]
    if option_score:
        parts.append(f"if score {option_score} guris.botani matches 1")
    if prefix_unless:
        parts.append(prefix_unless)

    if parts == ["execute"]:
        # No execute prefix needed; direct call.
        return f"function guris:_handler/{behavior} {args_str}"
    return f"{' '.join(parts)} run function guris:_handler/{behavior} {args_str}"


def build_macro_args(row: dict[str, Any], pos: str) -> dict[str, str]:
    """Compose the NBT-compound-literal argument map passed to the handler macro.

    All keys present even when empty so the handler template can rely on them.
    """
    args: dict[str, str] = {
        "id": str(row["id"]),
        "state": str(row.get("blockstate") or ""),
        "pos": pos,
        "loot": str(row.get("loot") or ""),
        "loot2": str(row.get("loot_alt") or ""),
        "loot_tall": str(row.get("loot_tall") or ""),
        "loot_short": str(row.get("loot_short") or ""),
        "loot_day": str(row.get("loot_day") or ""),
        "loot_night": str(row.get("loot_night") or ""),
        "potted": str(row.get("potted_id") or ""),
    }
    # Beet's Function won't escape these; we already know they're safe ID strings.
    return args
