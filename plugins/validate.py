"""Lightweight static validator: scans every emitted mcfunction for `function`
and `loot` references and asserts each target exists in the pack.

Catches:
- typos in generated dispatcher (e.g. handler renamed but caller not updated)
- forgotten loot table copies
- broken namespace migration

Runs late in the pipeline (after all generators) so it sees the final pack.
Errors abort the build with a clear message.
"""

from __future__ import annotations

import re
from beet import Context

# `$function ns:path/to/fn {...}` (macro form) or `function ns:path/to/fn`.
FUNCTION_REF = re.compile(r"^\s*\$?execute\s+.*\brun\s+function\s+([a-z0-9_./:-]+)|^\s*\$?function\s+([a-z0-9_./:-]+)", re.MULTILINE)
LOOT_REF = re.compile(r"\bloot\s+spawn\s+\S+\s+\S+\s+\S+\s+loot\s+([a-z0-9_./:-]+)|\bloot\s+spawn\s+\S+\s+\S+\s+\S+\s+loot\s+([a-z0-9_./:-]+)\b", re.MULTILINE)


def beet_default(ctx: Context):
    fn_keys = set(ctx.data.functions.keys())
    loot_keys = set(ctx.data.loot_tables.keys()) if hasattr(ctx.data, "loot_tables") else set()

    errors: list[str] = []

    for fn_id, fn in ctx.data.functions.items():
        body = "\n".join(fn.lines) if hasattr(fn, "lines") else str(fn)
        for m in re.finditer(r"\bfunction\s+([a-z0-9_./:-]+)", body):
            target = m.group(1).strip()
            # Skip macro-substituted refs like `guris:_handler/$(behavior)` —
            # we can't statically know the value.
            if "$(" in target or "$" in target:
                continue
            # Skip references to vanilla namespaces or function tags (#tag).
            if target.startswith("#"):
                continue
            ns, _, path = target.partition(":")
            if ns in ("minecraft",):
                continue
            if target not in fn_keys:
                errors.append(f"function reference {target!r} (in {fn_id}) does not resolve")

        for m in re.finditer(r"\bloot\s+\S+\s+loot\s+([a-z0-9_./:-]+)", body):
            target = m.group(1).strip()
            if "$(" in target:
                continue
            ns, _, _path = target.partition(":")
            if ns in ("minecraft",):
                continue
            if target not in loot_keys:
                errors.append(f"loot table {target!r} (in {fn_id}) does not resolve")

    if errors:
        # De-duplicate while preserving order.
        seen, unique = set(), []
        for e in errors:
            if e not in seen:
                seen.add(e)
                unique.append(e)
        msg = "validate plugin found unresolved references:\n  - " + "\n  - ".join(unique)
        raise RuntimeError(msg)

    profile = ctx.meta.get("profile", "?")
    fn_count = len(fn_keys)
    loot_count = len(loot_keys)
    print(f"  validate[{profile}]: OK ({fn_count} function(s), {loot_count} loot table(s))")
