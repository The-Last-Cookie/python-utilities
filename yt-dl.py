import os
import sys

if len(sys.argv) < 2:
    print('No YouTube link provided')
    exit(0)

# first argument is the file itself
link = sys.argv[1]

command = str('youtube-dl -o "%USERPROFILE%\Downloads\%(title)s.%(ext)s" ' + link + ' --extract-audio --audio-format mp3 --audio-quality 256K')

os.system(command)
