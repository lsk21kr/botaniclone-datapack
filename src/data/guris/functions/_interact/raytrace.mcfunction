# context: as player, at ray edge.
# Walk the player's eye ray forward 0.2 blocks at a time looking for any
# pack-supported plant. When found, create or move the interaction entity.
# (Ported from plant_raytrace.mcfunction; namespaces updated; option_shroomlight
# removed — merged into option_fungus per v1.0 changelog.)

# Ray distance counter (24 steps × 0.2 ≈ 4.8 blocks reach).
execute unless score #ray_dist guris.botani matches 1.. run scoreboard players set #ray_dist guris.botani 24
scoreboard players remove #ray_dist guris.botani 1

# Default-on plants (always discoverable).
execute unless score @s guris.botani matches 1 if block ~ ~ ~ #guris:non-optionals run function guris:_interact/get

# Option-gated discoverability.
execute unless score @s guris.botani matches 1 if score option_potted guris.botani matches 1 if block ~ ~ ~ #minecraft:flower_pots unless block ~ ~ ~ minecraft:flower_pot run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_tree guris.botani matches 1 if block ~ ~ ~ #minecraft:leaves unless block ~ ~ ~ minecraft:mangrove_leaves run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_tree guris.botani matches 1 if block ~ ~ ~ minecraft:mangrove_propagule[age=4,hanging=true] run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_ancient guris.botani matches 1 if block ~ ~ ~ #guris:ancient_plants run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_ancient guris.botani matches 1 if block ~ ~ ~ minecraft:pitcher_crop[age=4] run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_chorus guris.botani matches 1 if block ~ ~ ~ minecraft:chorus_flower unless block ~ ~ ~ minecraft:chorus_flower[age=0] run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_fungus guris.botani matches 1 if block ~ ~ ~ #minecraft:wart_blocks run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_fungus guris.botani matches 1 if block ~ ~ ~ minecraft:shroomlight run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_mushroom guris.botani matches 1 if block ~ ~ ~ #guris:mushroom_blocks run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_netherwart guris.botani matches 1 if block ~ ~ ~ minecraft:nether_wart[age=3] run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_witherrose guris.botani matches 1 if block ~ ~ ~ minecraft:wither_rose run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_witherrose guris.botani matches 1 if score option_potted guris.botani matches 1 if block ~ ~ ~ minecraft:potted_wither_rose run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_golden_dandelion guris.botani matches 1 if block ~ ~ ~ minecraft:golden_dandelion run function guris:_interact/get
execute unless score @s guris.botani matches 1 if score option_golden_dandelion guris.botani matches 1 if score option_potted guris.botani matches 1 if block ~ ~ ~ minecraft:potted_golden_dandelion run function guris:_interact/get

# Continue ray casting forward unless we've already terminated on an available block.
execute if score #ray_dist guris.botani matches 1.. unless block ~ ~ ~ #guris:available positioned ^ ^ ^0.2 run function guris:_interact/raytrace
