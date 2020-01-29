from .config import denormalizeRgbPasses
from .config import loudnessBounds
from .config import melodyBounds
from .config import tempDir
from .config import timbreBounds
from colorsys import hls_to_rgb
from colorsys import rgb_to_hls
from math import log10
from math import modf
import numpy as np
from typing import Dict, List, Tuple, Union

def dBFStoGainAmps(dBs: np.ndarray) -> np.ndarray:
  return np.round(10 ** (dBs / 20), 2)

def gainAmpTodBFS(amps: np.ndarray) -> np.ndarray:
  return 20 * np.log10(amps)
  
def normalizeOne(n: Union[int, float], minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float], clamped: bool = True) -> Union[int, float]:
  if clamped:
    n = clampOne(n, minBound, maxBound)

  return ((n - minBound) / (maxBound - minBound)) * (newMax - newMin) + newMin

def denormalizeOne(normalizedN: float, minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float]) -> Union[int, float]:
  return ((normalizedN - newMin) / (newMax - newMin)) * (maxBound - minBound) + minBound

def normalizeAll(arr: np.ndarray, minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float], clamped: bool = True) -> np.ndarray:
  if clamped:
    arr = clampAll(arr, minBound, maxBound)

  return ((arr - minBound) / (maxBound - minBound)) * (newMax - newMin) + newMin

def denormalizeAll(normalizedArr: List[float], minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float]) -> List[Union[int, float]]:
  return [denormalizeOne(normN, minBound, maxBound, newMin, newMax) for normN in normalizedArr]

def clampOne(n: Union[int, float], minBound: Union[int, float], maxBound: Union[int, float]) -> Union[int, float]:
  return max(minBound, min(maxBound, n))

def clampAll(arr: np.ndarray, minBound: Union[int, float], maxBound: Union[int, float]) -> np.ndarray:
  return np.clip(arr, minBound, maxBound)
 
def normalizeRgb(rgb: Tuple[int]) -> Tuple[float]:
  return tuple(normalizeAll(list(rgb), minBound=0, maxBound=255, newMin=0, newMax=1.0))

# The purpose of this function is to scale from rgb[0.0-1.0] to rgb[0, 255].
# This process would normally result in the loss of data, since the common ways
# of accomplishing this goal involves either rounding or flooring each component
# into ints.
#
# Therefore, the solution I came up with is to perform multiple passes over the
# original rgb tuple, storing the information to the right of the decimal in
# additional integer rgb tuples. The larger the number of passes, the more
# accurate the data being preserved. The tradeoff is, of course, more colors
# being sent to the client. This process is reversed in reconstructRgb.
def denormalizeRgb(rgb: Tuple[float, float, float]) -> List[Tuple[int, int, int]]:
  l = []
  currentRgb = list(rgb)
  for _ in range(denormalizeRgbPasses):
    denorm = denormalizeAll(currentRgb, minBound=0, maxBound=255, newMin=0, newMax=1.0)
    decimalRgb, integerRgb = zip(*[modf(n) for n in denorm])
    integerRgb = tuple(int(n) for n in integerRgb)
    l.append(integerRgb)
    currentRgb = list(decimalRgb)

  return l

def normalizeMelody(melody: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
  return [(t, normalizeOne(f, **melodyBounds, clamped=False)) if f > 0 else (t, 0) for t, f in melody]

def denormalizeMelody(normalizedMelody: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
  return [(t, denormalizeOne(fPrime, **melodyBounds)) if fPrime > 0 else (t, 0) for t, fPrime in normalizedMelody]

def normalizeVolume(volumeChanges: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
  return [(t, normalizeOne(A, **loudnessBounds)) for t, A in volumeChanges]

def denormalizeVolume(normalizedVolumeChanges: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
  return [(t, denormalizeOne(APrime, **loudnessBounds)) for t, APrime in normalizedVolumeChanges]

def normalizeTimbre(timbreTexture: float) -> float:
  return normalizeOne(timbreTexture, **timbreBounds);

def denormalizeTimbre(normalizedTimbreTexture: float) -> float:
  return denormalizeOne(normalizedTimbreTexture, **timbreBounds);

def hlsToRgb(hls: Tuple[float, float, float]) -> Tuple[float, float, float]:
  return hls_to_rgb(*hls)

def rgbToHls(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
  return rgb_to_hls(*rgb)

# Given an rgb[0.0-1.0] tuple, return a list of hex color strings
def rgbToHex(rgb: Tuple[float, float, float]) -> List[str]:
  # denormalizeRgb returns a list of rgb[0-255] tuples
  return [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in denormalizeRgb(rgb)]

def hlsToHex(hls: Tuple[float, float, float]) -> List[str]:
  return rgbToHex(hlsToRgb(hls))

def hexToHls(hexStringGroup: List[str]) -> Tuple[float, float, float]:
  return rgbToHls(reconstructRgb(hexStringGroup))

def melodyPartsToHexColor(melodyParts: Dict) -> Dict[int, str]:
  melody = normalizeMelody(melodyParts['melody'])
  volumeChanges = normalizeVolume(melodyParts['volumeChanges'])
  timbreTexture = normalizeTimbre(melodyParts['timbreTexture'])

  h = 0.0
  l = 0.0
  s = timbreTexture
  volumePtr = 0
  colorTimeMap = dict()
  for t, freq in melody:
    h = freq
    volumeT, volumeValue = volumeChanges[volumePtr]
    if t == volumeT:
      l = volumeValue
      volumePtr += 1

    colorTimeMap[t] = hlsToHex((h, l, s))
  
  return colorTimeMap

def hexColorToMelodyParts(colorTimeMap: Dict[int, List[str]]) -> Dict:
  melody = []
  volumeChanges = []
  timbreTexture = 0.0
  lastLightness = 0.0
  for i, (t, hexStringGroup) in enumerate(colorTimeMap.items()):
    h, l, s = hexToHls(hexStringGroup)
    if i == 0:
      timbreTexture = s

    melody.append((t, h))
    if l != lastLightness:
      volumeChanges.append((t, l))
      lastLightness = l

  return {
    'melody': denormalizeMelody(melody),
    'volumeChanges': denormalizeVolume(volumeChanges),
    'timbreTexture': denormalizeTimbre(timbreTexture)
  }

# Based off of terrygarcia's stackexchange answer:
# https://stackoverflow.com/a/57777266
def hexToRgb(hexString: str) -> Tuple[float, float, float]:
  n = int(hexString[1:], 16)
  b = n % 256.0
  g = (n - b) / 256.0 % 256.0
  r = (n - b) / 256.0 ** 2 - (g / 256.0)
  return (int(r), int(g), int(b))

# The original rgb[0.0-1.0] data has been converted into a group of hex color
# strings. This function performs the reverse of that operation.
def reconstructRgb(hexStringGroup: List[str]) -> Tuple[float, float, float]:
  rgbList = [hexToRgb(hexString) for hexString in hexStringGroup]
  # The rgb[0-255] tuples have been stored in order of information contained,
  # with the rgbList[0] containing the greatest amount. The last one added
  # will be scaled to [0.0-1.0] and be added to the rgbList[n-1]th integer rgb
  # tuple, and so on.
  integerRgbList = rgbList[:-1]
  decimalRgb = normalizeRgb(rgbList[-1])
  for integerRgb in reversed(integerRgbList):
    # Add itemwise, integer + decimal: r + r, g + g, b + b
    decimalRgb = normalizeRgb(tuple(a + b for a, b in zip(integerRgb, decimalRgb)))

  # decimalRgb is now in the form that it was originally before having
  # denormalizeRgb applied to it.
  return decimalRgb

