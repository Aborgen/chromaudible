from math import log10
import numpy as np
from typing import List, Union

def dBFStoGainAmps(dBs: np.ndarray) -> np.ndarray:
  return np.round(10 ** (dBs / 20), 2)

def gainAmpTodBFS(amps: np.ndarray) -> np.ndarray:
  return 20 * np.log10(amps)
  
def normalizeOne(n: Union[int, float], minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float]) -> Union[int, float]:
  n = clampOne(n, minBound, maxBound)
  return (n - minBound / maxBound - minBound) * (newMax - newMin) + newMin

def normalizeAll(arr: np.ndarray, minBound: Union[int, float], maxBound: Union[int, float], newMin: Union[int, float], newMax: Union[int, float]) -> np.ndarray:
  arr = clampAll(arr, minBound, maxBound)
  return (arr - minBound / maxBound - minBound) * (newMax - newMin) + newMin

def clampOne(n: Union[int, float], minBound: Union[int, float], maxBound: Union[int, float]) -> Union[int, float]:
  return max(minBound, min(maxBound, n))

def clampAll(arr: np.ndarray, minBound: Union[int, float], maxBound: Union[int, float]) -> np.ndarray:
  return np.clip(arr, minBound, maxBound)
