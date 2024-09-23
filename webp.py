import os
from PIL import Image

# taken from https://stackoverflow.com/a/61242086
def isAnimated(file_path: str) -> bool:
    with open(file_path, mode='rb') as file_handler:
        file_handler.seek(12)
        if file_handler.read(4) == b'VP8X':
            file_handler.seek(20)
            is_animated_byte = file_handler.read(1)
            return (ord(is_animated_byte) >> 1) & 1
        return False

def isTransparent(img: Image) -> bool:
    return img.mode == "RGBA" or "transparency" in img.info

def convert(file_path: str, format = 'jpeg', overwrite = False, **params) -> None:
    new_file_path = file_path[:-4] + format
    img = Image.open(file_path)

    # JPEG does not support alpha channel
    if isTransparent(img) and format == 'jpeg':
        img = img.convert('RGB')

    img.save(new_file_path, format, **params)

    if overwrite:
        os.remove(file_path)

file_path = ''
if isAnimated(file_path):
    convert(file_path, 'gif', quality=95, optimize=True, save_all=True)
else:
    convert(file_path, 'jpeg', quality=95, optimize=True, subsampling=0)
