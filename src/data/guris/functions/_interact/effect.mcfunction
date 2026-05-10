# context: as player, at interaction.
# Visual + audio feedback after a successful drop, and consume one bone meal.

particle minecraft:happy_villager ~ ~ ~ 0.3 0.3 0.3 0 16
playsound minecraft:item.bone_meal.use block @s ~ ~ ~

execute as @s[gamemode=!creative] run clear @s minecraft:bone_meal 1

# Mark the interaction as consumed so plant_check's pass-2 guards behave correctly.
execute as @e[type=interaction,sort=nearest,limit=1] run scoreboard players set @s guris.botani 2
