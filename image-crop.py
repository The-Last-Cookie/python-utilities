import os
import re
from PIL import Image

PATH = './original'
X = 100
Y = 200
W = 400
H = 300

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
            if file.endswith(allowed_format) and re.match('[a-z]+', file) is not None:
                crop_image(file, X, Y, W, H)

if __name__ == "__main__":
    main()
