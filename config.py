"""
Default system configuration.
To override settings edit config_local.py
"""
import os


# Render in pygame simulator instead of to the curtain
RENDER_PYGAME = True

# Render faulty pixels in pygame simulator
RENDER_FAULTS = True

#eastcampus tweets
ENABLE_TWITTER = False

# Listen for beats
ENABLE_BEATS = False

ENABLE_QUIET_HOURS = False
#In 24-hour time, the times of day when the curtain will be off
#you will have to rewrite this if it contains midnight
QUIET_HOURS_START = 300
QUIET_HOURS_END = 800

# create local settings file
if not os.path.exists("./config_local.py"):
    with open("./config_local.py", 'w') as f:
        f.write("# Override local settings in this file.\n\n")

# import local settings
from config_local import *
