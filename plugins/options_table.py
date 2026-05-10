"""Generates botaniclone:options/default, botaniclone:options/toggle/<key>,
and botaniclone:settings from src/tables/options.yaml.

The hand-written settings.mcfunction and options/default.mcfunction in
src/data/botaniclone/functions/* are placeholders only — this plugin
overwrites them via ctx.data["..."] = Function(...).

Pipeline order: runs after legacy_filter (so we can drop options whose
min_pack_format > target).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from beet import Context, Function


def beet_default(ctx: Context):
    target_format = int(ctx.meta.get("max_format", ctx.meta.get("pack_format", 0)))
    options_path = Path(ctx.directory) / "src/tables/options.yaml"
    if not options_path.exists():
        return

    raw = yaml.safe_load(options_path.read_text(encoding="utf-8")) or []
    options = [
        opt for opt in raw
        if int(opt.get("min_pack_format", 0)) <= target_format
    ]

    # 1. Defaults function (preserves existing scores).
    default_lines = [
        "# Auto-generated from src/tables/options.yaml — do not edit by hand.",
        "# Defaults are applied only when not yet set, so existing worlds preserve user choices.",
    ]
    for opt in options:
        key = opt["key"]
        default = int(opt["default"])
        default_lines.append(
            f"execute unless score {key} guris.botani = {key} guris.botani run scoreboard players set {key} guris.botani {default}"
        )
    ctx.data["botaniclone:options/default"] = Function(default_lines)

    # 2. Per-option toggle functions.
    for opt in options:
        key = opt["key"]
        short = opt["short"]
        toggle_lines = [
            f"# Auto-generated toggle for {key}",
            f"execute if score {key} guris.botani matches 1.. run scoreboard players set {key} guris.botani 2",
            f"execute unless score {key} guris.botani matches 1.. run scoreboard players set {key} guris.botani 1",
            f"execute if score {key} guris.botani matches 2.. run scoreboard players set {key} guris.botani 0",
            f"execute if score {key} guris.botani matches 1 run playsound minecraft:ui.button.click master @s ~ ~ ~ .2 1.9 .2",
            f"execute if score {key} guris.botani matches 0 run playsound minecraft:ui.button.click master @s ~ ~ ~ .2 1.3 .2",
            f"function botaniclone:settings",
            f"function guris:_options/_mute_set",
        ]
        ctx.data[f"botaniclone:options/toggle/{short}"] = Function(toggle_lines)

    # 3. Settings menu (chat tellraw).
    settings_lines = [
        "# Auto-generated from src/tables/options.yaml — do not edit by hand.",
        '# Padding so the menu pushes prior chat content up.',
    ]
    for _ in range(6):
        settings_lines.append('tellraw @s ["",{"text":" "}]')
    settings_lines.append('tellraw @s ["",{"text":"\\u00A7m                                                                                ","color":"dark_gray"}]')
    settings_lines.append('tellraw @s ["",{"text":"                    BotaniClone "},{"text":"/","color":"gray"},{"text":" Global Settings"}]')
    settings_lines.append('tellraw @s ["",{"text":"\\u00A7m                                                                                ","color":"dark_gray"}]')

    for opt in options:
        for state in ("on", "off"):
            settings_lines.append(_build_menu_line(opt, state))

    settings_lines.append('tellraw @s ["",{"text":"\\u00A7m                                                                                ","color":"dark_gray"}]')
    settings_lines.append("function guris:_options/_mute_set")
    ctx.data["botaniclone:settings"] = Function(settings_lines)

    # 4. Mute helpers (silence the spammy command-feedback while toggling/printing).
    ctx.data["guris:_options/_mute_set"] = Function([
        "# Auto-generated mute helper.",
        "execute store result score mute guris.botani run gamerule sendCommandFeedback",
        "execute if score mute guris.botani matches 1 run schedule function guris:_options/_mute_reset 1t",
        "gamerule sendCommandFeedback false",
    ])
    ctx.data["guris:_options/_mute_reset"] = Function([
        "gamerule sendCommandFeedback true",
    ])


# ---- helpers ------------------------------------------------------------------

def _build_menu_line(opt: dict, state: str) -> str:
    """Emit one tellraw line for either the [✔] (state='on') or [❌] (state='off') variant."""
    key = opt["key"]
    short = opt["short"]
    label = opt["label"]
    hover_underline = opt.get("hover_underline")
    hover = opt.get("hover")
    if state == "on":
        condition = f"if score {key} guris.botani matches 1.."
        bracket_text = "[ ✔ ]"
        bracket_color = "green"
        body = opt.get("on_text", "Enabled")
    else:
        condition = f"unless score {key} guris.botani matches 1.."
        bracket_text = "[ ❌ ]"
        bracket_color = "red"
        body = opt.get("off_text", "Disabled")

    components: list[dict] = [
        "",
        {
            "text": bracket_text,
            "color": bracket_color,
            "clickEvent": {
                "action": "run_command",
                "value": f"/function botaniclone:options/toggle/{short}",
            },
        },
        {"text": f" {label}", "bold": True},
        {"text": f": {body}"},
    ]
    if hover_underline:
        components.append({
            "text": hover_underline,
            "underlined": True,
            "hoverEvent": {"action": "show_text", "value": hover or hover_underline},
        })
    payload = json.dumps(components, ensure_ascii=False)
    return f"execute {condition} run tellraw @s {payload}"
