# -*- coding: utf-8 -*-
#
# ffmpeg.py
# created by giginet on 2011/12/18
#
import os
import re
import sys
import math
import commands

def get_playtime(path):
    """
    Returns play time of movie/audio file.
    """
    command = "ffmpeg -i %s" % path
    try:
        output = commands.getstatusoutput(command)[1]
    except:
        return 0
    for line in output.split('\n'):
        duration = re.findall(r"Duration: ([0-9]{2}:[0-9]{2}:[0-9\.]*)", line)
        if duration:
            times = duration[0].split(':')
            if len(times) == 3:
                return sum([float(v) * math.pow(60, 2 - i) for i, v in enumerate(times)])
    return 0

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Second argument must be filename."
    else:
        path = os.path.join(os.getcwd(), sys.argv[1])
        print get_playtime(path)
