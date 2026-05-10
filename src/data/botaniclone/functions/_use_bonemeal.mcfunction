# context: advancement reward, as player at player.
# Player just used bone meal on an interaction entity. Walk all nearby
# interactions and dispatch each one through the plant_check pipeline.
advancement revoke @s only botaniclone:use_bonemeal

tag @s add botani.actor
execute as @e[type=interaction,distance=..6] run function guris:_interact/dispatch
tag @s remove botani.actor
