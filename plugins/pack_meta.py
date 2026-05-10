"""Generates pack.mcmeta with profile-specific pack_format and supported_formats range.

Beet's default mcmeta only contains pack_format + description. We override the
entire mcmeta payload so we can add `supported_formats` (1.20.2+ feature) and
optionally the newer `min_format`/`max_format` (25w31a+ format).
"""

from __future__ import annotations

from beet import Context


def beet_default(ctx: Context):
    meta = ctx.meta

    pack_format = int(meta.get("pack_format", 0))
    min_format = int(meta.get("min_format", pack_format))
    max_format = int(meta.get("max_format", pack_format))
    use_min_max = bool(meta.get("use_min_max_fields", False))

    if not pack_format:
        raise ValueError("meta.pack_format missing — set in profile yaml")

    description = ctx.data.description or "BotaniClone"
    if isinstance(description, list):
        description = description[0] if description else "BotaniClone"
    description = str(description)

    pack_block: dict = {
        "pack_format": pack_format,
        "description": description,
    }
    # supported_formats was added in pack_format 16 (1.20.2 / 23w31a).
    if pack_format >= 16:
        pack_block["supported_formats"] = {
            "min_inclusive": min_format,
            "max_inclusive": max_format,
        }
    # Newer min_format/max_format style (25w31a+, format 88+). Modern profile sets both.
    if use_min_max:
        pack_block["min_format"] = min_format
        pack_block["max_format"] = max_format

    ctx.data.mcmeta.data = {"pack": pack_block}
