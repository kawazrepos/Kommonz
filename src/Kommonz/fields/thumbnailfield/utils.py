# -*- coding: utf-8 -*-
#
# src/Kommonz/fields/thumbnailfield/utils.py
# created by giginet on 2011/11/12
#
import os
import shutil
def get_thumbnail_filename(filename, pattern_name):
    '''
    Returns the thumbnail name associated to the standard image filename
        * Example: /var/www/myproject/media/img/picture_1.jpeg
            will return /var/www/myproject/media/img/picture_1.thumbnail.jpeg
    '''
    splitted_filename = list(os.path.splitext(filename))
    splitted_filename.insert(1, '.%s' % pattern_name)
    return ''.join(splitted_filename)

def resize_image(filename, size):
    '''
    Resizes the image to specified width, height and force option
        - filename: full path of image to resize
        - size: dictionary containing:
            - width: new width
            - height: new height
            - force: if True, image will be cropped to fit the exact size,
                if False, it will have the bigger size that fits the specified
                size, but without cropping, so it could be smaller on width or height
    '''
    WIDTH, HEIGHT = 0, 1
    try:
        from PIL import Image, ImageOps
    except ImportError:
        import Image
        import ImageOps

    img = Image.open(filename)
    if img.size[WIDTH] > size['width'] or img.size[HEIGHT] > size['height']:
        if size['force']:
            img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS)
        else:
            img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
        try:
            img.save(filename, optimize=1)
        except IOError:
            img.save(filename)

