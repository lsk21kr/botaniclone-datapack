# context: as player, at player's interaction.
# Delete the interaction when the player has stopped pointing at a supported plant.

execute as @e[type=minecraft:interaction,sort=nearest,limit=1] run kill @s
