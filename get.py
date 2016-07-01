#!/usr/local/bin/python3

import subprocess
import os
import time
import configparser

# TODO: Implement ConfigParser bit

# TODO: Run in loop and check exit code status, run again if error
# TODO: Run periodically to check updates in the downloadfile
# TODO: Remove entries from the downloadfile as the thing completes
#   * Accomplish this by reading config chunks out of the file and writing the remainder

# TODO: Make this work on Windows?
try:
    DOWNLOADFILE = os.environ['DOWNLOADFILE']
except KeyError:
    print("You must set the environment variable DOWNLOADFILE to point to your list of URLs!")
    sys.exit(1)

try:
    DLDIR = os.environ['DLDIR']
except KeyError:
    print("You must set the environment variable DLDIR to point to your download directory!!")
    sys.exit(1)

def getArglist(url):
    """
    Returns the command line for youtube-dl with our options and URL in list format
    for subprocess.Popen()
    """
    args = []
    args.append('youtube-dl')
    args.append('-c')
    # The following two options are listed as deprecated, 
    # but there's some issue using the Outputformat that I can't determine.
    # So instead, we just set cwd in our subprocess.Popen call and it all works out.
    args.append('-t')
    args.append('-A')
    args.append(url)

    return args

def downloadPlaylist(cfgsection):
    """
    Pass in a config section and actually do the downloading.
    """
    name = cfgsection.name
    url = cfgsection.get('url')

    if name and url:
        playlistdir = os.path.join(DLDIR, name)
        if not os.path.exists(playlistdir):
            print("Creating directory %s" % playlistdir)
            os.mkdir(playlistdir)

        args = getArglist(url)
        if cfgsection.getboolean('audio'):
            args.append('--extract-audio')
            args.append('--audio-format=mp3')
            if cfgsection.getboolean('sync'):
                # If we're going to be repeatedly syncing this playlist
                # it makes sense to keep the originals around to avoid
                # re-downloading the whole thing every time.
                args.append('--keep-video')

        p = subprocess.Popen(args=args, cwd=playlistdir)
        p.wait()

if __name__ == "__main__":
    # This exterior loop should just do the config file reading and rewriting
    # While dispatching youtube-dl for the actual work
    #
    while True:
        print("Checking queuefile %s for updates..." % DOWNLOADFILE)
        config = configparser.ConfigParser()
        config.read(DOWNLOADFILE)

        for plname in config.sections():
            section = config[plname]
            downloadPlaylist(section)
            if not section.getboolean('sync'):
                pass # TODO: Delete the section from the new config

            TIMESLEEP_MINUTES = 60
            print("Reached end of loop, sleeping for %d minutes..." % TIMESLEEP_MINUTES)
            time.sleep(TIMESLEEP_MINUTES*60)
