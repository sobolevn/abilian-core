"""
Provides tools (currently: only functions, not a real service) for image
processing.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from cStringIO import StringIO
import hashlib

from PIL import Image

__all__ = ['resize', 'RESIZE_MODES', 'SCALE', 'FIT', 'CROP']

# resize modes

#: resize without retaining original proportions
SCALE = 'scale'

#: resize image and retain original proportions. Image width and height will be
#: at most specified width and height, respectively; At least width or height
#: will be equal to specified width and height, respectively.
FIT = 'fit'

#: crop image and resize so that it matches specified width and height.
CROP= 'crop'

RESIZE_MODES = frozenset({SCALE, FIT, CROP})


# TODO: cache to file
cache = {}

def open(img):
  if isinstance(img, basestring):
    img = StringIO(img)

  pos = img.tell()
  image = Image.open(img)
  img.seek(pos)
  return image


def get_format(img):
  image = open(img)
  return image.format

def get_size(img):
  image = open(img)
  return image.size

def get_save_format(fmt):
  if format in ('GIF', 'PNG'):
    return 'PNG'
  return 'JPEG'


def resize(orig, width, height, mode=FIT):
  cache_key = (hashlib.md5(orig).digest(), mode, width, height)
  if cache_key in cache:
    return cache[cache_key]

  if isinstance(orig, basestring):
    orig = StringIO(orig)

  image = open(orig)
  format = image.format
  x, y = image.size

  if (x, y) == (width, height):
    return orig.read()

  if mode is SCALE:
    image = image.resize((width, height), Image.LANCZOS)
  elif mode is FIT:
    image.thumbnail((width, height), Image.LANCZOS)
  elif mode is CROP:
    image = _crop_and_resize(image, width, height)

  output = StringIO()
  image.save(output, get_save_format(format))
  converted = output.getvalue()
  cache[cache_key] = converted
  return converted


def _crop_and_resize(image, width, height=0):
  if not height:
    height = width

  # Compute cropping coordinates
  x1 = y1 = 0
  x2, y2 = image.size
  w_ratio = 1.0 * x2 // width
  h_ratio = 1.0 * y2 // height

  if h_ratio > w_ratio:
    y1 = int(y2 // 2 - width * w_ratio // 2)
    y2 = int(y2 // 2 + height * w_ratio // 2)
  else:
    x1 = int(x2 // 2 - width * h_ratio // 2)
    x2 = int(x2 // 2 + height * h_ratio // 2)

  image = image.crop((x1, y1, x2, y2))
  image.thumbnail((width, height), Image.LANCZOS)
  return image
