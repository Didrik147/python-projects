# -*- coding: utf-8 -*-

import os

most_recent_file = None
most_recent_time = 0

for entry in os.scandir():
    if entry.is_file():
        # get the modification time of the file using entry.stat().st_mtime_ns
        mod_time = entry.stat().st_mtime_ns
        if mod_time > most_recent_time and "putt-maister-data-export" in entry.name:
            # update the most recent file and its modification time
            most_recent_file = entry.name
            most_recent_time = mod_time
            

print(most_recent_file)