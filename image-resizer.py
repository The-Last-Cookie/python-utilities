import os
from PIL import Image

PATH = r''
MAX_SIZE = 800

def resize_image(filename):
    filepath = PATH + '/' + filename
    image = Image.open(filepath)

    image.thumbnail(size=(MAX_SIZE, MAX_SIZE))
    print('Compressing file: ', filename)
    image.save(PATH + '/'+ 'Compressed_' + filename, image.format, optimize=True, quality=95, subsampling=0)

def main():
    formats = ('.jpeg', '.jpg', '.png')

    for file in os.listdir(PATH):
        for format in formats:
            if file.endswith(format):
                resize_image(file)

if __name__ == "__main__":
    main()
