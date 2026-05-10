"""Skeleton: handles plural ↔ singular folder convention for the output pack.

In recent Beet versions, the singular folder names (function/, loot_table/,
predicate/, advancement/, tags/block/, tags/function/) are emitted automatically
based on the declared pack_format. So this plugin is a no-op for now.

If a future Beet version stops auto-handling the rename, this plugin will
intercept ctx.data and rewrite the in-memory paths before the pack is written.
"""

from __future__ import annotations

from beet import Context


def beet_default(ctx: Context):
    # Currently a no-op — Beet handles folder convention automatically based on
    # ctx.data.pack_format. Re-evaluate during Step 4 once the pipeline is
    # exercising both targets end-to-end.
    _ = ctx
