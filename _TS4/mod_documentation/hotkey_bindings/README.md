# TS4 Hotkey Bindings
The bindings mod defines method and hotkeys to be used with the 'TS4 Hotkeys & Gamepad' mod.

## Functionality
### Move and Rotate
Instead of 'WASD'/'QE' the 'IJKL'/'TG' keys will be used to move or rotate a sim.

One tile matches around 1 meter and there are modifier keys to use various steps.
* Shift+Alt+_ .... 1 m / 1 tile | 90°
* Alt+_ .......... 25 cm | 22.5°
* Shift+_ ........ 5 cm  | 4.5°
* Ctrl+_ ......... 1 cm | 0.9°
* Shift+Ctrl+_ ... 2 mm | 0.18°
* For '_' use one of the 'IJKL'/'TG' keys.

#### Modes
* Shift+M - Toggle Movement Mode: Absolute (world axis) or Camera (I=away, K=closer, J=left, L=right); T/G (up/down) always use the world axis. 
* Shift+B - Toggle Usage: Move or Rotate

#### Save
* Shift+Ctrl+S - Call the pose/animation player to save the current sim position.  

Please note: For poses/animations sims are usually teleported to the object center.
This is their location in-game, no matter where they are displayed while the pose is playing.
Thus, the center of the object it used to determine the camera axis and not the visible sim position on the screen. 

### Speed / Experimental / Useless
The game speed can be set, no matter whether TS4 wants to block it. Results may vary.
* Shift+Ctrl+Alt+P - Pause the game
* Shift+Ctrl+Alt+1 - Set the game speed to 1
* Shift+Ctrl+Alt+2 - Set the game speed to 2
* Shift+Ctrl+Alt+3 - Set the game speed to 3

### Saving
* Ctrl+S - Save the game in a timely manner.
This save method is many times faster than the UI save button. Saving takes a few seconds and runs in background. Wait 5 seconds before exiting the game, after the 'save' notification has been displayed.
In case the game has issues with loading 'Alpha-CC' and the rending of thumbnails of sims/hair/outfits takes ages it helps a lot to use this method.
The ID is incremented every 4 hours. This will increase the needed disc space and/or allow to load also really old save files.

### Exiting
* Shift+Ctrl+Alt+X - Exit the game in a timely manner. Nothing will be saved. A currently running save will be interrupted, so use it with care.

### Outfit options
Outfit options are fully supported using 3rd party mods which support outfit modifiers. For vanilla TS4 some options are not available and dressing the sim is usually not possible. One CAS part after the other is either hidden or replaced by the bathing outfit. The order is pre-defined and can not be modified.
* H - Toggle heels / shoes. ('H' as 'S' is already used by TS4)
* Q - Undress the active sim.
* Shift+Q - Dress the active sim (Undo Q).
* Ctrl+Q - Undress all other sims in the social group.
* Shift+Ctrl+Q - Undress all sims in the social group, including the active sim.
* Shift+U - Undress all members during club gathering.

### Debug
* Shift+Ctrl+Alt+C - Create a thread dump of all running TS4 threads.

## Pose and Animation interactions
There is support for some special interactions, this might or might not be supported by the used pose/animation player.

* Shift+N - Play next pose/animation
* Shift+O - Active sim gets very happy (within the currently played pose/animation).
* Ctrl+O - All other 1-n sims  gets very happy (within the currently played pose/animation).
* Shift+Ctrl+O - Make all sims in currently played pose/animation happy.
* Shift+H - Active sim swaps its spot randomly in current pose/animation.
* Ctrl+H - A random sim swaps its spot randomly in current pose/animation. Best to be used with 3+ sim poses.
* ~~Win+Shift+H - Experimental²: Active sim swaps its spot randomly with a sim playing a different pose/animation.~~
* ~~Win+Ctrl+H - Experimental²: A random sim swaps its spot randomly with a sim playing a different pose/animation.~~
* Shift+Ctrl+S - Call the pose/animation player to save the current sim position.  This makes only sense if the sim has been moved before using the 'Move' options.

Experimental² means experimental. Don't enable or use these hotkeys.
If errors are thrown after using it simply ignore them.
Do not report them.


# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.111.102, S4CL 3.9, TS4Lib 0.3.33.
It is expected to be compatible with many upcoming releases of TS4, S4CL and TS4Lib.

## Dependencies
Download the ZIP file, not the sources.
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not installed download and install TS4 and these mods.
All are available for free.

## Installation
* Locate the localized `The Sims 4` folder which contains the `Mods` folder.
* Extract the ZIP file into this `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/$mod_name.ts4script`, `Mods/_o19_/$mod_name.package`, `mod_data/$mod_name/*` and/or `mod_documentation/$mod_name/*`
* `mod_logs/$mod_name.txt` will be created as soon as data is logged.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this. 
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## Copyright and License
* © 2024 [Oops19](https://github.com/Oops19)
* License for '.package' files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* License for other media unless specified differently: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 / o19 is not endorsed by or affiliated with Electronic Arts or its licensors.
Game content and materials copyright Electronic Arts Inc. and its licensors. 
Trademarks are the property of their respective owners.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
* or [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To check the XML structure of custom tunings use [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).
