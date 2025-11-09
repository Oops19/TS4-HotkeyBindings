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


# 📝 Addendum

## 🔄 Game compatibility
This mod has been tested with `The Sims 4` 1.119.109, S4CL 3.15, TS4Lib 0.3.42.
It is expected to remain compatible with future releases of TS4, S4CL, and TS4Lib.

## 📦 Dependencies
Download the ZIP file - not the source code.
Required components:
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not already installed, download and install TS4 and the listed mods. All are available for free.

## 📥 Installation
* Locate the localized `The Sims 4` folder (it contains the `Mods` folder).
* Extract the ZIP file directly into this folder.

This will create:
* `Mods/_o19_/$mod_name.ts4script`
* `Mods/_o19_/$mod_name.package`
* `mod_data/$mod_name/*`
* `mod_documentation/$mod_name/*` (optional)
* `mod_sources/$mod_name/*` (optional)

Additional notes:
* CAS and Build/Buy UGC without scripts will create `Mods/o19/$mod_name.package`.
* A log file `mod_logs/$mod_name.txt` will be created once data is logged.
* You may safely delete `mod_documentation/` and `mod_sources/` folders if not needed.

### 📂 Manual Installation
If you prefer not to extract directly into `The Sims 4`, you can extract to a temporary location and copy files manually:
* Copy `mod_data/` contents to `The Sims 4/mod_data/` (usually required).
* `mod_documentation/` is for reference only — not required.
* `mod_sources/` is not needed to run the mod.
* `.ts4script` files can be placed in a folder inside `Mods/`, but storing them in `_o19_` is recommended for clarity.
* `.package` files can be placed in a anywhere inside `Mods/`.

## 🛠️ Troubleshooting
If installed correctly, no troubleshooting should be necessary.
For manual installs, verify the following:
* Does your localized `The Sims 4` folder exist? (e.g. localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...)
  * Does it contain a `Mods/` folder?
    * Does Mods/_o19_/ contain:
      * `ts4lib.ts4script` and `ts4lib.package`?
      * `{mod_name}.ts4script` and/or `{mod_name}.package`
* Does `mod_data/` contain `{mod_name}/` with files?
* Does `mod_logs/` contain:
  * `Sims4CommunityLib_*_Messages.txt`?
  * `TS4-Library_*_Messages.txt`?
  * `{mod_name}_*_Messages.txt`?
* Are there any `last_exception.txt` or `last_exception*.txt` files in `The Sims 4`?


* When installed properly this is not necessary at all.
For manual installations check these things and make sure each question can be answered with 'yes'.
* Does 'The Sims 4' (localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...) exist?
  * Does `The Sims 4` contain the folder `Mods`?
    * Does `Mods` contain the folder `_o19_`? 
      * Does `_19_` contain `ts4lib.ts4script` and `ts4lib.package` files?
      * Does `_19_` contain `{mod_name}.ts4script` and/or `{mod_name}.package` files?
  * Does `The Sims 4` contain the folder `mod_data`?
    * Does `mod_data` contain the folder `{mod_name}`?
      * Does `{mod_name}` contain files or folders?
  * Does `The Sims 4` contain the `mod_logs` ?
    * Does `mod_logs` contain the file `Sims4CommunityLib_*_Messages.txt`?
    * Does `mod_logs` contain the file `TS4-Library_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
    * Does `mod_logs` contain the file `{mod_name}_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
  * Doesn't `The Sims 4` contain the file(s) `last_exception.txt`  and/or `last_exception*.txt` ?
* Share the `The Sims 4/mod_logs/Sims4CommunityLib_*_Messages.txt` and `The Sims 4/mod_logs/{mod_name}_*_Messages.txt`  file.

If issues persist, share:
`mod_logs/Sims4CommunityLib_*_Messages.txt`
`mod_logs/{mod_name}_*_Messages.txt`

## 🕵️ Usage Tracking / Privacy
This mod does not send any data to external servers.
The code is open source, unobfuscated, and fully reviewable.

Note: Some log entries (especially warnings or errors) may include your local username if file paths are involved.
Share such logs with care.

## 🔗 External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## ⚖️ Copyright and License
* © 2020-2025 [Oops19](https://github.com/Oops19)
* `.package` files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* All other content (unless otherwise noted): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 

You may use and adapt this mod and its code — even without owning The Sims 4.
Have fun extending or integrating it into your own mods!

Oops19 / o19 is not affiliated with or endorsed by Electronic Arts or its licensors.
Game content and materials © Electronic Arts Inc. and its licensors.
All trademarks are the property of their respective owners.

## 🧾 Terms of Service
* Do not place this mod behind a paywall.
* Avoid creating mods that break with every TS4 update.
* For simple tuning mods, consider using:
  * [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
  * [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To verify custom tuning structures, use:
  * [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).

## 🗑️ Removing the Mod
Installing this mod creates files in several directories. To fully remove it, delete:
* `The Sims 4/Mods/_o19_/$mod_name.*`
* `The Sims 4/mod_data/_o19_/$mod_name/`
* `The Sims 4/mod_documentation/_o19_/$mod_name/`
* `The Sims 4/mod_sources/_o19_/$mod_name/`

To remove all of my mods, delete the following folders:
* `The Sims 4/Mods/_o19_/`
* `The Sims 4/mod_data/_o19_/`
* `The Sims 4/mod_documentation/_o19_/`
* `The Sims 4/mod_sources/_o19_/`
