"""Sets the output artifact name based on profile, so Beet writes the zip with the
right filename. This plugin only needs to set ctx.data.name; Beet's `output` config
plus `data_pack.zipped: true` does the actual zipping.
"""

from __future__ import annotations

from beet import Context


def beet_default(ctx: Context):
    artifact = ctx.meta.get("artifact_name")
    if not artifact:
        raise ValueError("meta.artifact_name missing — set in profile yaml")
    ctx.data.name = artifact
