from config import tempDir
from colorsys import hls_to_rgb
from colorsys import rgb_to_hls
from math import log10
import numpy as np
from operator import itemgetter
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

def denormalizeRgb(rgb: Tuple[float]) -> Tuple[int]:
  denorm = denormalizeAll(list(rgb), minBound=0, maxBound=255, newMin=0, newMax=1.0)
  return tuple([round(n) for n in denorm])


def melodyPartsToHexColor(melodyParts: Dict) -> Dict[int, str]:
  melody, volumeChanges, timbreTexture = itemgetter('melody', 'volumeChanges', 'timbreTexture')(melodyParts)
  h = 0.0
  l = volumeChanges[0][1]
  s = timbreTexture
  volumePtr = 0
  colorTimeMap = dict()
  for t, freq in melody:
    h = freq
    volumeT, volumeValue = volumeChanges[volumePtr]
    if t == volumeT:
      l = volumeValue
      ++volumePtr

    colorTimeMap[t] = rgbToHex(hls_to_rgb(h, l, s))
  
  return colorTimeMap

def hexColorToMelodyParts(colorTimeMap: Dict[int, str]) -> Dict:
  melody = []
  volumeChanges = []
  timbreTexture = 0.0
  lastLightness = 0.0
  for i, (t, hexColor) in enumerate(colorTimeMap.items()):
    h, l, s = rgb_to_hls(*hexToRgb(hexColor))
    if i == 0:
      timbreTexture = s

    melody.append((t, h))
    if l != lastLightness:
      volumeChanges.append((t, l))
      lastLightness = l

  return {
    'melody': melody,
    'volumeChanges': volumeChanges,
    'timbreTexture': timbreTexture
  }
    
def rgbToHex(rgb: Tuple[float]) -> str:
  r, g, b = denormalizeRgb(rgb)
  return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Based off of terrygarcia's stackexchange answer:
# https://stackoverflow.com/a/57777266
def hexToRgb(hexString: str) -> Tuple[int]:
  n = int(hexString[1:], 16)
  b = n % 256.0
  g = (n - b) / 256.0 % 256.0
  r = (n - b) / 256.0 ** 2 - (g / 256.0)
  rgb = normalizeAll([int(r), int(g), int(b)], minBound=0, maxBound=255, newMin=0, newMax=1.0)
  return tuple(rgb)
