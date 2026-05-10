# context: as player, at player's interaction.
# Tag the existing interaction as "to be moved" so the next step relocates it.

scoreboard players set @s guris.botani 2
execute as @e[type=minecraft:interaction,sort=nearest,limit=1] run scoreboard players set @s guris.botani 2
