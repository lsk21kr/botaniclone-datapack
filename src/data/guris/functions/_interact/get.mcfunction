# context: as player, at ray edge.
# Plant detected on ray. Mark player as having a pending interaction and
# either reuse an existing interaction entity for this player or summon a new one.

scoreboard players set @s guris.botani 1

# Stop the ray loop.
scoreboard players set #ray_dist guris.botani 0

# If an interaction with this player's pid already exists nearby, reuse it.
execute at @e[type=minecraft:interaction] if score @s guris.pid = @e[type=minecraft:interaction,sort=nearest,limit=1] guris.pid run function guris:_interact/found

# Already-found interaction: move it to the new position.
execute as @e[type=minecraft:interaction,scores={guris.botani=2}] run function guris:_interact/move

# No existing interaction for this player: summon a new one.
execute if score @s guris.botani matches 1 summon minecraft:interaction run function guris:_interact/init
scoreboard players operation @e[type=interaction,scores={guris.botani=1,guris.pid=..0}] guris.pid = @s guris.pid
