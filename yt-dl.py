import os
import sys

def download_video():
    # first argument is the file itself
    if len(sys.argv) < 2:
        print('No YouTube link provided')
        filename = get_filename(sys.argv[0])
        print('Usage: ' + filename + ' [YouTube link]')
        return

    if (sys.argv[1] == 'help' or sys.argv[1] == '-h'):
        filename = get_filename(sys.argv[0])
        print('Usage: ' + filename + ' [YouTube link]')
        return

    link = sys.argv[1]

    command = str('youtube-dl -o "%USERPROFILE%\Downloads\%(title)s.%(ext)s" ' + link + ' --extract-audio --audio-format mp3 --audio-quality 256K')
    os.system(command)

def get_filename(path):
    if path.rfind('\\') == -1:
        filename = path
    else:
        last_occurence = path.rfind('\\')
        filename = path[last_occurence + 1:]
    
    return filename

download_video()
