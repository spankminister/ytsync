#!/usr/local/bin/python3

import subprocess
import os
import time

# TODO: Run in loop and check exit code status, run again if error
# TODO: Run periodically to check updates in the downloadfile
# TODO: Remove entries from the downloadfile as the thing completes

# TODO: Make this work on Windows?
#DOWNLOADFILE = os.path.join(os.environ.get('HOME'), 'Dropbox','youtubedl.txt')
DOWNLOADFILE = os.path.join("c:\\Users\\spanky\\Dropbox\\youtubedl.txt")
#MOVIEDIR = '/Users/spanky/Movies'
MOVIEDIR = 'm:\\Youtube'

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

if __name__ == "__main__":
    print("Checking queuefile %s for updates..." % DOWNLOADFILE)
    with open(DOWNLOADFILE,'r') as f:
        while True:
            print("Reading from file...")
            name = f.readline().rstrip()
            url = f.readline().rstrip()
            print("Name is: %s" % name)
            print("URL is: %s" % url)
            #queuefile = f.read()

            if name and url:
                playlistdir = os.path.join(MOVIEDIR, name)
                if not os.path.exists(playlistdir):
                    print("Creating directory %s" % playlistdir)
                    os.mkdir(playlistdir)

                args = getArglist(url)

                p = subprocess.Popen(args=args, cwd=playlistdir)
                p.wait()

                """
                if p.returncode == 0:
                    print("Successfully downloaded %s, removing from queuefile..." % name)
                    with open(DOWNLOADFILE,'w') as f:
                        f.write(queuefile)
                """
            print("Reached end of loop, sleeping for 10 secs...")
            time.sleep(10)
