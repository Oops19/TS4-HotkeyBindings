#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'HotkeyBindings'

    @property
    def _author(self) -> str:
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        return 'hotkey_bindings'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '0.1.1'


'''
v0.1.1
    Code cleanup
v0.1.0
    Split from Hotkeys
v0.0.26
    Add Ctrl+S to save the game.
v0.0.25
    Set height (Y) to the proper height when routing a sim.
v0.0.24
    Add hotkeys to modify the game speed
v0.0.23
    Add pose swap options
v0.0.22
    Bugfix
v0.0.21
    Add Controller / Gamepad support
    Refactoring
    Move ctypes to TS4Library
v0.0.20
    Add resend_location()
v0.0.19
    Add o19.sim.p + o19.sim.up
v0.0.18
    Added Debug 'Move' menu.
    Click on a sim/object and select 'Move'. It will be stored forever.
    Select the floor to unselect the stored sim/object. Then the active sim will be moved.
v0.0.17
    Improve rotation support
v0.0.16
    Depends again on TS4-Library
    Inverted L/R rotation angle to rotate properly
    Support 3D rotation
    Switching move mode (Camera | Zone axis) changes the mode from rotation to move. 
    Default move mode is now 'Camera'
v0.0.15
    Added 'synchronized' parameter to config. Set to False to execute immediately.
    While the game is paused everything is executed immediately.
    Added code to move sims around while they are posing / animation is played.
    Allocated keys 'IJKL TG BM' for this.
    Show notification for 'B' (move/rotate) / 'M' (move mode)
v0.0.14
    'Standalone' build:
    Included Singleton
    Replaced config loader with static code
v0.0.13
    Added 'o19.hk.toggle.log' to enable logging of all keys
    Fixed parsing of LWin and RWin keys, removed Apps key
    Hints will be disabled after a while
v0.0.12
    Thread-Fix
v0.0.11
    Refactoring
v0.0.10
    Add 'o19.hk.log 50' cheat
v0.0.9
    Reset key state
v0.0.8
    More logging
v0.0.7
    sys.setswitchinterval(0.001) from 0.005
v0.0.6
    Fixing some bugs
v0.0.5
    Fixing some bugs
v0.0.4
    Non-blocking GetMessage() & hook only while active
v0.0.3
    Cleanup of sources
v0.0.2
    Fixed undressing
    Removed Shift+P partially
    Modified Hotkey definitions
v0.0.1
    Initial version
'''
