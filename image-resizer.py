import os
from PIL import Image

PATH = r''
MAX_SIZE = 200
FILES = []

def resize_image(filename) -> None:
    filepath = PATH + '/' + filename
    try:
        image = Image.open(filepath)
    except FileNotFoundError:
        print('File not found!')
        return

    image.thumbnail(size=(MAX_SIZE, MAX_SIZE))
    print('Compressing file: ', filename)
    image.save(PATH + '/'+ 'Compressed_' + filename, image.format, optimize=True, quality=95, subsampling=0)

def main() -> None:
    formats = ('.jpeg', '.jpg', '.png')

    if FILES:
        for file in FILES:
            resize_image(file)
        return

    for file in os.listdir(PATH):
        for format in formats:
            if file.endswith(format):
                resize_image(file)

if __name__ == "__main__":
    main()
