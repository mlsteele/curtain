# Iron Curtain

## Setup

### Installation
Install (some subset) of the prereqs from requirements.txt

Pygame is required for the simulator, the rest are only required for hype
features.

### Configuration
Look at but try not to change `config.py`.

Override settings in `config_local.py`. You may have to create `config_local.py`.

Enable the pygame simulator in `config_local.py`.

Edit `runner.py` to show the plugins you want to display.

# Writing A Plugin
A plugin is a visualization that appears on the curtain.

To write a plugin, copy an example from `plugins/` (`plugins/fancyrainbow.py`
is a pretty simple example). Then add it to the list of background plugins in
`runner.py`.
