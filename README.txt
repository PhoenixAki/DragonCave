Joe Matta
Sean Stanley
Sethia Lochard

2D Game Design Project
“Dragoncave”
				
**Objective of the game**:
Dragoncave is a single-player 2D RPG. The objective of the game is to defeat the Golem Boss and obtain the Sacred
Crystal. This is done by first entering the cave dungeon and defeating goblins and Wyverns, and proceeding to the
Golem's room. The goblins and wyverns drop coins and rubies that you can sell to the shop owner to obtain key items
that you need to defeat the Golem. After defeating the Golem, return the crystal to the quest giver.

**Instructions**:
The player starts in the Forest area. There are two NPCs here. The NPC on the left between two trees will tell you your
quest, and the NPC on the right in front of the house is a shop owner. To talk to the “Quest” NPC, face him and
press <Enter>.

After hearing your quest, enter the cave to the north. Make sure to buy some arrows first! The cave entrance leads to
the first cave room. Goblin and Wyvern enemies are in this room. They will chase you down if you get too close.
Defeat these enemies to obtain coins and rubies which can be used to buy items from the shop. Occasionally, Wyverns
may drop potions which will heal you for +1. When the enemies in this room are defeated, the east wall will open. The
opening leads to the Golem boss room. The Golem will quickly chase you and destroy you if you do not have the
Boots (sold at the shop). Also, you need to buy the Magic Book to upgrade your arrows to fire magic in order to
damage the Golem. The golem is immune to regular arrows, so make sure to have the magic book first. If you run out
of arrows, you can buy more at the shop.

After defeating the Golem, a key will appear. Take the key and use it to open the chest in the north-east corner of
the Golem room. Face the chest from the bottom and press <Enter>; if you have the key, the chest will open, and the
Sacred Crystal will appear from the chest. Take the crystal back to the Quest NPC to finish the game.

**Controls**:
Up arrow key / W	Walk up
Left arrow key / A	Walk left
Right arrow key / D	Walk right
Down arrow key / S	Walk down
Space key		Attack (shoot arrows)
Enter key		Interact with NPC/Buy Items/Open Chest
Tab key	Display 	Toggle display of stats and items
Escape key		Close game and exit

**Health**:
The player has three hit points (HP). Contact with enemies reduce the player’s HP by one. There is a brief invincibility
 period after getting hit. Wyverns in the first cave will occasionally drop potions that will heal the player by +1 health.
 The player can have up to 5 health.

**Money**:
The player starts with 50 money and 0 arrows. Use the 50 money to buy some arrows before going into the cave! Coins are
worth 50 and rubies are worth 75.

**Movement**:
Holding the up arrow moves your player up. Down moves down. Left and right arrow moves the player left and right
respectively. The player is restricted to the map areas and cannot move off the edge unless moving to another map.
Once the Boots are purchased the players movement speed is increased.

**Combat**:
Pressing the space bar will cause the player to shoot an arrow. When close to the player, enemies will stop moving and
attack the player. NOTE: attack animations are not working due to unresolved errors, but they still damage the player.
The player can hold up to 45 arrows at a time.

**Inventory**:
The player can hold up to 600 worth of coins and rubies. He can also hold the magic book (upgrades arrows to magic fire
 arrows), boots (increases speed), the boss key, and the crystal.

+++ NOTES +++:
Enemies have two modes - "Attack" and "Roaming".
In "Attack" mode, the enemies will find the shortest path to the player using Breadth First Search and attack when close.
If the player is hurt, he enters an "invincibility" mode for a short time. During player invincibility, the enemies
will go back to "Roaming". When the invincibility period ends, all enemies in range will return to "Attack" mode and resume
finding the shortest path and attacking.
+++++++++++++

========================================================
- Obtaining the game source code from GitHub:

    from the command prompt, navigate to the desired destination folder,
    and enter the following line:

    $ git clone https://github.com/jmatta697/2D_RPG

- Running the game:

    navigate to the clone destination folder targeted in the previous step,
    and change current directory to '2D_RPG':

    $ cd 2D_RPG

    then ensure that arcade is installed via:

    $ pip3 install arcade

    then run the program by entering the following line:

    $ python Main.py

    The game will launch. A 960 x 960 window will appear with the Forest opening scene.
========================================================
SYSTEM REQUIREMENTS:
	- “Arcade” game graphics library version 2.1.7
	- Python 3.7

