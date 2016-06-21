#!/usr/local/bin/python3

import subprocess
import os
import time

# TODO: Run in loop and check exit code status, run again if error
# TODO: Run periodically to check updates in the downloadfile
# TODO: Remove entries from the downloadfile as the thing completes
#   * Accomplish this by reading config chunks out of the file and writing the remainder

# TODO: Change config file format to something like
"""
[Playlist Title]
url=http://youtube.com/some_video_url
sync=True (defaults to False)
audio=False (defaults to False)
"""
# Where sync will keep it in the queue file to be re-downloaded periodically
# And audio will only retain the audio file

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

def getPlaylistData(fp):
    # Returns a name the the player and the URL, given a file pointer to a playlist list.
    print("Reading from file...")
    name = f.readline().rstrip()
    url = f.readline().rstrip()
    print("Name is: %s" % name)
    print("URL is: %s" % url)
    return name, url


if __name__ == "__main__":
    print("Checking queuefile %s for updates..." % DOWNLOADFILE)
    with open(DOWNLOADFILE,'r') as f:
        while True:
            name, url = getPlaylistData(f)
            #print("Reading from file...")
            #name = f.readline().rstrip()
            #url = f.readline().rstrip()
            #print("Name is: %s" % name)
            #print("URL is: %s" % url)

            if name and url:
                playlistdir = os.path.join(DLDIR, name)
                if not os.path.exists(playlistdir):
                    print("Creating directory %s" % playlistdir)
                    os.mkdir(playlistdir)

                args = getArglist(url)

                p = subprocess.Popen(args=args, cwd=playlistdir)
                p.wait()

            print("Reached end of loop, sleeping for 11 secs...")
            time.sleep(10)
