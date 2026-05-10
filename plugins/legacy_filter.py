"""Reads blocks.yaml and stashes a filtered list (drops rows whose
min_pack_format is greater than the profile's target). The block_table plugin
then consumes ctx.meta["_filtered_blocks"] instead of re-reading the YAML.

This must run BEFORE block_table in the pipeline.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from beet import Context


def beet_default(ctx: Context):
    # The filter threshold is the MAX pack_format the profile's range covers,
    # not the primary pack_format declaration. Modern's primary is 80 (1.21.6)
    # but its supported_formats spans up to 105 (26.2 snap), so we keep blocks
    # that became available anywhere in the range.
    target_format = int(ctx.meta.get("max_format", ctx.meta.get("pack_format", 0)))
    if not target_format:
        raise ValueError("meta.max_format / meta.pack_format missing — set in profile yaml")

    table_path = Path(ctx.directory) / ctx.meta["blocks_table"]
    if not table_path.exists():
        # blocks.yaml may not exist yet during the very first scaffold run;
        # block_table will handle empty-or-missing gracefully.
        ctx.meta["_filtered_blocks"] = []
        return

    raw = yaml.safe_load(table_path.read_text(encoding="utf-8")) or []
    if not isinstance(raw, list):
        raise ValueError(f"{table_path} must contain a list at top level")

    filtered: list[dict] = []
    dropped: list[str] = []
    for row in raw:
        min_fmt = int(row.get("min_pack_format", 0))
        if min_fmt <= target_format:
            filtered.append(row)
        else:
            dropped.append(str(row.get("id", "<no-id>")))

    ctx.meta["_filtered_blocks"] = filtered
    if dropped:
        profile = ctx.meta.get("profile", "?")
        print(f"  legacy_filter[{profile}]: dropped {len(dropped)} row(s) above format {target_format}: {', '.join(dropped)}")
