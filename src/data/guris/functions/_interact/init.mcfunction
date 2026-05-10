# context: as new interaction entity, at ray edge.
# Set hitbox, position, and bind to the player's pid.

data modify entity @s width set value 0.5f
data modify entity @s height set value 0.5f
tp @s ~ ~-0.25 ~
scoreboard players set @s guris.botani 1
scoreboard players set @s guris.pid 0
