# Python utilities

This is a small folder for python scripts to make life easier :)

## Image resizer

```md
image-resizer.py
```

Scales down an image (or several) to a specific size while keeping its aspect ratio (and also reduces file size a bit).

*Notice: This requires [Pillow](https://python-pillow.org/).*

## Image cropper

```md
image-crop.py
```

Crop an image on specific coordinates

*Notice: This requires [Pillow](https://python-pillow.org/).*

## webp

webp to jpg or gif converter

*Notice: This requires [Pillow](https://python-pillow.org/).*

- [ ] TODO: as UI with tkinter?

## wiki-search

```md
wiki-search.sh
```

The [osu! wiki](https://github.com/ppy/osu-wiki/) is a knowledge base for the rhythm game called *osu!*. For more information about osu!, see [here](https://osu.ppy.sh).

With this tool, you can search for file content in any wiki article.

## Wrapper for youtube-dl

```md
yt-dl.py
```

This is a Windows python wrapper for executing a specific command via [youtube-dl](https://github.com/ytdl-org/youtube-dl).

It simplifies the workflow a bit, so that the command doesn't need to be typed in the console every time. Mainly using this for downloading music as `.mp3`.

The script can be converted into an executable via `pyinstaller yt-dl.py --onefile` if required. The actual youtube-dl application needs to be downloaded as well.
