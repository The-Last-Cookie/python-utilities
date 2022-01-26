# Python utilities

This is a small folder for python scripts to make life easier :)

## Image resizer

```md
image-resizer.py
```

Resizes an image (or several) to a specific size while keeping its aspect ratio (and also reduces file size a bit).

*Notice: This requires [Pillow](https://python-pillow.org/).*

## osu! wiki search

```md
osu-wiki-search.py
```

The [osu! wiki](https://github.com/ppy/osu-wiki/) is a knowledge base for the rhythm game called *osu!*. For more information about osu!, see [here](https://osu.ppy.sh).

With this tool, you can search for file content in any wiki article.

This should be used as a cli tool for Windows via converting the script into an executable (can be done with `pyinstaller osu-wiki-search.py --onefile`). I'm not sure if it also runs on UNIX-based systems, because I haven't tried it yet.

## Wrapper for youtube-dl

```md
yt-dl.py
```

This is a python wrapper for executing a specific command via [youtube-dl](https://github.com/ytdl-org/youtube-dl).

It simplifies the workflow a bit, so that the command doesn't need to be typed in the console every time. Mainly using this for downloading music as `.mp3`.
