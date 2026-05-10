# context: #minecraft:tick

# Set per-player pid for multiplayer-friendly interaction matching.
execute as @a[gamemode=!spectator] unless score @s guris.pid matches 1.. store result score @s guris.pid run scoreboard players add #last guris.pid 1

# Find a plant when the player is holding bone meal in main hand.
execute as @a[predicate=guris:bonemeal,gamemode=!spectator] at @s anchored eyes positioned ^ ^ ^ run function guris:_interact/raytrace

# Remove a player's interaction when not currently bone-mealing an enabled plant.
execute as @a unless score @s guris.botani matches 1.. at @e[type=minecraft:interaction] if score @s guris.pid = @e[type=minecraft:interaction,sort=nearest,limit=1] guris.pid run function guris:_interact/remove

scoreboard players reset @a guris.botani
