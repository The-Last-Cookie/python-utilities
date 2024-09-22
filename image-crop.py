import os
import re
from PIL import Image

PATH = './original'

def crop_image(filename, x, y, w, h) -> None:
    print('Cropping file: ', filename)
    filepath = PATH + '/' + filename
    try:
        image = Image.open(filepath)
    except FileNotFoundError:
        print('File not found!')
        return

    image = image.crop((x, y, w, h))
    image.save(PATH + '/../cut/' + filename, image.format, optimize=True, quality=95, subsampling=0)

def main() -> None:
    formats = ('.jpeg', '.jpg', '.png')

    files = os.listdir(PATH)
    for file in files:
        for allowed_format in formats:
            # Normal book pages have this format: 505, 349, 2205, 1538
            # Wallpaper: TODO

            if file.endswith(allowed_format) and re.match('[a-z]+', file) is not None:
                crop_image(file, 505, 349, 2205, 1538)

if __name__ == "__main__":
    main()
