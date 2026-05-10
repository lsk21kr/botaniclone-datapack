# context: botaniclone:load — runs once per world load, idempotent.
# Migration shim for upgrading from v1.0 (guris:botani/* namespace).
#
# Scoreboard objectives (guris.botani, guris.pid) are unchanged across the
# upgrade, so per-world option choices and per-player pid mappings survive.
# This file cleans up state that COULD linger from a v1.0 install:
#   1. Stray botani.actor tag on a disconnected player.
#   2. Old advancement state (the new advancement has a different ID, so v1.0
#      players will need to bone-meal once to re-trigger; harmless).
#
# If new migration concerns arise in future versions, append idempotent commands
# below — never delete prior steps as they may still be needed for older worlds.

tag @a remove botani.actor
