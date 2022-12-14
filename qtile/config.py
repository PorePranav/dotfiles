import os
import re
import socket
import subprocess
from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder

import colors

#My programmes
mod = "mod4"
mod1 = "mod1"
myBrowser = 'firefox'
myTerminal = 'alacritty'
myTextEditor = myTerminal + ' vim'
myPrimaryFileManager = 'pcmanfm'
mySecondaryFileManager = myTerminal + ' vifm'
myRecorder = 'obs'
myDrawingApp = 'mypaint'
myVideoEditor = 'kdenlive'
myAudioEditor = 'audacity'
myPhotoEditor = 'gimp'
myVirtualbox = 'virtualbox'
myVideoPlayer = 'vlc'
myPrimaryMenu = 'rofi -show run'
myEmailCliant = 'thunderbird'

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc = "Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc = "Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc = "Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc = "Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc = "Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc = "Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc = "Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc = "Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc = "Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc = "Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc = "Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc = "Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc = "Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc = "Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(myTerminal), desc = "Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc = "Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc = "Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc = "Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc = "Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc = "Spawn a command using a prompt widget"),

    #Browser
    Key([mod, "shift"], "b", lazy.spawn(myBrowser), desc = "Launch browser"),

    #Geany
    Key([mod, "shift"], "n", lazy.spawn(myTextEditor), desc = "Launch Neovim"),

    #Email cliant
    Key([mod], "e", lazy.spawn(myEmailCliant), desc = "Launch thunderbird"),

    #Primary File manager
    Key([mod, "shift"], "f", lazy.spawn(myPrimaryFileManager), desc = "Lauch primary file manager"),

    #rofi
    Key([mod], "space", lazy.spawn(myPrimaryMenu), desc = "Launch dmenu"),


    #Sound
    Key([mod1], "v", lazy.spawn("pactl set-sink-volume 0 +5%")),
    Key([mod1, "shift"], "v", lazy.spawn("pactl set-sink-volume 0 -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),

    #Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("lux -a 10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("lux -s 10%")),
]

groups = [Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp'),
          Group("???", layout='bsp')]

dgroups_key_binder = simple_key_binder(mod)


# Append scratchpad with dropdowns to groups
groups.append(ScratchPad('scratchpad', [
    DropDown('myTerminal', myTerminal, width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown('myTextEditor', myTextEditor, width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown('mySecondaryFileManager', mySecondaryFileManager, width=0.4, height=0.5, x=0.3, y=0.2, opacity=1),
]))
# extend keys list with keybinding for scratchpad
keys.extend([
    Key(["control"], "1", lazy.group['scratchpad'].dropdown_toggle('myTerminal')),
    Key(["control"], "2", lazy.group['scratchpad'].dropdown_toggle('myTextEditor')),
    Key(["control"], "3", lazy.group['scratchpad'].dropdown_toggle('mySecondaryFileManager')),
])

colors, backgroundColor, foregroundColor, workspaceColor, foregroundColorTwo = colors.doomOne() 

layouts = [
    layout.MonadTall(border_focus = colors[0], border_normal = colors[0], border_width = 1, margin = 8),
    #layout.Bsp(border_focus = colors[4], margin = 5),
    #layout.RatioTile(border_focus = colors[4], margin = 2),
    #layout.TreeTab(border_focus = colors[4], margin = 2),
    #layout.Tile(border_focus = colors[4], margin = 2),
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadWide(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font = 'Hack',
    fontsize = 16,
    padding = 2,
    background = colors[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.GroupBox(
					margin_x = 5,
					active = colors[2],
                    inactive = colors[1],
                    highlight_color = [backgroundColor, workspaceColor],
                    highlight_method = 'line',
                    ),
               widget.Prompt(),
                widget.TextBox(
                   # text='\u25e2',
                    padding=0,
                    fontsize=12,
                    background = workspaceColor,
                foreground = backgroundColor),
            widget.WindowName(
				    foreground = colors[5]
                    ),
#                widget.CPU(
#                format = '???  {freq_current}GHz {load_percent}%',
#                background = foregroundColorTwo,
#                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerminal + ' -e htop')},
#                foreground = colors[10],
#                padding = 2
#                ),
#		widget.Memory(
#                    background = foregroundColorTwo,
#                    foreground = colors[4],
#                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerminal + ' -e htop')},
#                    fmt = '??? {}',
#                    padding = 2
#		),
               widget.Volume(
                    foreground = colors[8],
                    background = foregroundColorTwo,
                    fmt = '??? {}',
                    padding = 2
                    ),
                widget.Battery(
                    charge_char ='???',
                    discharge_char = '???',
                    format = '??? {percent:2.0%} {char}',
                    foreground = colors[6],
                    background = foregroundColorTwo,
                    padding = 8,
                    ),
                widget.Clock(format='??? %a, %d. %m. %Y. | ??? %I:%M %p',
					foreground = colors[2],
                    background = backgroundColor,
					padding = 2
					),
				widget.QuickExit(
					fmt = '??? ',
					foreground = colors[9],
					padding = 2
					),              
            ],
            20,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start = lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start = lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_focus = colors[4], float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class = 'gimp'),  # gitk
    Match(wm_class = 'mypaint'),  # gitk
    Match(wm_class = 'ssh-askpass'),  # ssh-askpass
    Match(title = 'branchdialog'),  # gitk
    Match(title = 'pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

#Programms to start on log in
@hook.subscribe.startup_once
def autostart ():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
