# context: as interaction, at player.
# Verify the interaction belongs to the bone-mealing player, then run plant_check
# at the interaction's position (which is at/near the targeted block).

scoreboard players set #match guris.botani 0
execute on target store result score #match guris.botani if entity @s[tag=botani.actor]
execute if score #match guris.botani matches 1 at @s as @p[tag=botani.actor] run function botaniclone:plant_check
execute if score #match guris.botani matches 1 run data remove entity @s interaction
