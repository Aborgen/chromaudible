import math
from PIL import Image
from PIL import PyAccess
from typing import List, Tuple
from .utils import reversed_index_of_first_not
from .utils import index_of_first_not
from werkzeug.datastructures import FileStorage

def extractImage(f: FileStorage):
  image = Image.open(f).convert('RGB')
  # In the case that the image is not square
  n = min(image.width, image.height)
  if n % 2 != 0:
    n -= 1

  pixelMatrix = image.load()
  return _extractSpiral(pixelMatrix, n)

def _extractSpiral(pixelMatrix: PyAccess, n: int):
  # These parameters must be the same as defined in front/. . ./AudioUpload.vue
  distanceBetweenPoints = 1
  separationBetweenRings = 20
  numberOfArms = 5
  origin = ([n // 2] * 2)
  generator = _spiralPointGenerator(distanceBetweenPoints, separationBetweenRings)

  intRgbGroupList = []
  while True:
    point = next(generator)
    x = origin[0] + point[0]
    # Subtract, as [0, 0] in pixelMatrix is the upper left corner.
    y = origin[1] - point[1]
    rgbGroup = _extractPoints(pixelMatrix, x, y, origin, numberOfArms)
    if not rgbGroup:
      break

    intRgbGroupList.append(rgbGroup)

  foo = _cleanup(intRgbGroupList)
  return foo

def _anyPureBlack(rgbGroup: List[Tuple[int, int, int]]) -> bool:
  return any(rgb == (0, 0, 0) for rgb in rgbGroup)

# Remove excess pure black from end of list
def _cleanup(rgbGroupList: List[List[Tuple[int, int, int]]]):
  beginning = index_of_first_not(rgbGroupList, predicate=_anyPureBlack)
  end = reversed_index_of_first_not(rgbGroupList, predicate=_anyPureBlack)
  return rgbGroupList[beginning:end]

# Implementation is the same as front/utils/Spiral.js
def _spiralPointGenerator(distanceBetweenPoints: int, separationBetweenRings: int):
  b = separationBetweenRings / (2 * math.pi);
  radius = distanceBetweenPoints;
  theta = radius / b;
  x = 0;
  y = 0;
  while True:
    yield (x, y)
    x = math.floor(radius * math.cos(theta));
    y = math.floor(radius * math.sin(theta));
    theta += (distanceBetweenPoints / radius);
    radius = b * theta;

def _extractPoints(pixelMatrix: PyAccess, x: int, y: int, origin: Tuple[int, int], numberOfArms: int):
  xOffset = x - origin[0]
  yOffset = y - origin[1]
  phi = math.radians(round(360 / numberOfArms))
  intRgbGroup = []
  # In the event that accessing pixelMatrix with out of bounds indices, return
  # None. This is how the loop in _extractSpiral terminates.
  try:
    for i in range(numberOfArms):
      if i == 0:
        intRgbGroup.append(pixelMatrix[x, y])
        continue

      x1 = origin[0] + math.floor(xOffset * math.cos(phi * i) - yOffset * math.sin(phi * i))
      y1 = origin[1] + math.floor(yOffset * math.cos(phi * i) + xOffset * math.sin(phi * i))
      intRgbGroup.append(pixelMatrix[x1, y1])
  except:
    return None

  return intRgbGroup
