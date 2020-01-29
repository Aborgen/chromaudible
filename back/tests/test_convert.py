import numpy as np
from src.convert import denormalizeMelody
from src.convert import denormalizeTimbre
from src.convert import denormalizeVolume
from src.convert import hexColorToMelodyParts
from src.convert import hexToHls
from src.convert import hexToRgb
from src.convert import hlsToHex
from src.convert import hlsToRgb
from src.convert import melodyPartsToHexColor
from src.convert import normalizeMelody
from src.convert import normalizeTimbre
from src.convert import normalizeVolume
from src.convert import reconstructRgb
from src.convert import rgbToHex
from src.convert import rgbToHls
from .__config import hexGroupList
from .__config import hlsList
from .__config import melodyParts
from .__config import normMelodyParts
from .__config import rgbList



import json

decimal = 8
def test_normalize_melodyParts():
  result = {
    'melody': normalizeMelody(melodyParts['melody']),
    'volumeChanges': normalizeVolume(melodyParts['volumeChanges']),
    'timbreTexture': normalizeTimbre(melodyParts['timbreTexture'])
  }

  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], normMelodyParts[key], decimal=decimal)

def test_assure_normMelodyParts_values_within_range():
  result = {
    'melody': normalizeMelody(melodyParts['melody']),
    'volumeChanges': normalizeVolume(melodyParts['volumeChanges']),
    'timbreTexture': normalizeTimbre(melodyParts['timbreTexture'])
  }

  minValue = 0.0
  maxValue = 1.0
  for key in list(result.keys()):
    if key == 'timbreTexture':
      assert minValue <= result[key] <= maxValue
      continue

    for t, n in result[key]:
      assert minValue <= n <= maxValue

def test_revert_normalize_melodyParts():
  result = {
    'melody': denormalizeMelody(normMelodyParts['melody']),
    'volumeChanges': denormalizeVolume(normMelodyParts['volumeChanges']),
    'timbreTexture': denormalizeTimbre(normMelodyParts['timbreTexture'])
  }

  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)
# ----
def test_hls_to_rgb():
  result = [hlsToRgb(hls) for hls in hlsList]
  np.testing.assert_almost_equal(result, rgbList, decimal=decimal)

def test_rgb_to_hls():
  result = [rgbToHls(rgb) for rgb in rgbList]
  np.testing.assert_almost_equal(result, hlsList, decimal=decimal)
# ----
# ----
def test_hls_to_hex():
  result = [hlsToHex(hls) for hls in hlsList]
  assert result == hexGroupList

def test_hex_to_hls():
  result = [hexToHls(hexGroup) for hexGroup in hexGroupList]
  np.testing.assert_almost_equal(result, hlsList, decimal=decimal)
# ----
# ----
def test_rgb_to_hex():
  result = [rgbToHex(rgb) for rgb in rgbList]
  assert result == hexGroupList

def test_hex_to_rgb():
  result = [reconstructRgb(hexGroup) for hexGroup in hexGroupList]
  np.testing.assert_almost_equal(result, rgbList, decimal=decimal)
# ----
# ----
def test_melodyParts_to_hex():
  result = melodyPartsToHexColor(melodyParts)
  for i, (_, obtainedGroup) in enumerate(result.items()):
    assert obtainedGroup == hexGroupList[i]

def test_hex_to_melodyParts():
  timeHex = {i[0]: h for i, h in zip(melodyParts['melody'], hexGroupList)}
  result = hexColorToMelodyParts(timeHex)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)
# ----
# Used to create hlsList in __config.py
def __construct_hlsList__():
  melody = normMelodyParts['melody']
  volumeChanges = normMelodyParts['volumeChanges']
  timbreTexture = normMelodyParts['timbreTexture']

  h = 0.0
  l = 0.0
  s = timbreTexture
  volumePtr = 0
  hlsList = []
  for t, freq in melody:
    h = freq
    volumeT, volumeValue = volumeChanges[volumePtr]
    if t == volumeT:
      l = volumeValue
      volumePtr += 1

    hlsList.append((h, l, s))

  return hlsList
