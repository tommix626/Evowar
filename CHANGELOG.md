Created on Wed Mar  3 18:02:14 2021
the evowar game end to update at version 0.92,instead i want to make this into a no network-need game with different playing rules

# this is another game project aim at create a defense-attacking war game

## log
    0.8     start of file
            basic environment
    0.9     cursor invloved
    0.91    eat dots
            player level up system
    0.92    fence block
            font tips
    0.93    change the structure of the code
            adding a framework(gameAgent)
    0.94    adding buildings and bullet
    0.95   trivial uppdates
    0.96    add troops
            inhanced speed
    0.97    troop stategy
    0.98    various troops and controls
    0.98a1  file strucutre modification & expConsumption
    0.98a2  minymap 
    0.98a3  bigmap
    0.99    new renderer
    0.99a1  added "alt" to halt the player       
            
## improvs
    -dot size smaller,circle, dot color brighter,ban red(v0.92)
    -add a fence(v0.8)
    -use cursor to move player(v0.9)
    -blocks outside fence(v0.9)
    -drawing optimise(v0.9x)
    -prob:bullet can't escape the trap of the building(solved)
    -special thanks to wyk for report lots of bugs for the program to improve
    -use a fatherclass function move to create more variable movements(as follow)
    -only at this moment have i realize that in this version of pygame pos doesn't need to be a int
    -troop strategy(v0.97)
    -setting
    -player hp system(v0.97)
    -player rebirth (v0.97)
    -troop sight(v0.97)
    -use arror keys to change kind of troops,and key(1-5) to implement
    -add enemy-type as a parameter(for hptower...)
    -use "enemy tag"/extra_draw instead of distinct color to distinguish enemies from friends
    -items can cross fence
    -draw buffs use towrs enemy to hollow circle
@author: Tom

I decided to add some consumption to exp for spawning different troops, towers or even respawning 
The current values are as follows
shooting:2 <-- in Player.shoot_line()
respawning:100 <-- this makes respawning a more of stratagy, but it is up to you, in player.rebirth()
other towers:300 <-- in GameAgent
troops:500<-- there seems to be exsisting codes, but I failed to find them
the list for storing above numbers are in global_variables.expConsumption
@Ling

Also, I find it IMPOSSIBLE to find the part I need
so I decide to put the classes into different files
hope you can understand
still, you can change the from...import to import to ease further modifications
@Ling

minymap is finished, I think I should give the special towers a special circle, so it shouldn't be written inside trooplist
I need to change the structure with gameagent.
if you feel ok just tell me :P
@Ling

The renderer is changed into a single file. There are still links to the original functions, but I still suggest a direct link to renderer class
@Ling

left ALT can be used to halt the player for better controls.
@Ling