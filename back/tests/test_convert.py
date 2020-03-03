import numpy as np
from src.convert import colorToMelodyParts
from src.convert import denormalizeMelody
from src.convert import denormalizeTimbre
from src.convert import denormalizeVolume
from src.convert import hexColorToMelodyParts
from src.convert import hexToHls
from src.convert import hexToRgb
from src.convert import hlsToHex
from src.convert import hlsToIntRgb
from src.convert import hlsToRgb
from src.convert import intRgbToHls
from src.convert import melodyPartsToHexColor
from src.convert import melodyPartsToColor
from src.convert import normalizeMelody
from src.convert import normalizeTimbre
from src.convert import normalizeVolume
from src.convert import reconstructRgb
from src.convert import reconstructRgb_hexVariant
from src.convert import rgbToHex
from src.convert import rgbToHls
from src.convert import rgbToIntRgb
from .__melody import melodyParts
from .__melody import normMelodyParts
from .__data import rgbList
from .__data import hexGroupList
from .__data import hlsList
from .__data import intRgbGroupList

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
def test_hls_to_intRgb():
  result = [hlsToIntRgb(hls) for hls in hlsList]
  assert result == intRgbGroupList

def test_intRgb_to_hls():
  result = [intRgbToHls(intRgbGroup) for intRgbGroup in intRgbGroupList]
  np.testing.assert_almost_equal(result, hlsList, decimal=decimal)
# ----
# ----
def test_rgb_to_hex():
  result = [rgbToHex(rgb) for rgb in rgbList]
  assert result == hexGroupList

def test_hex_to_rgb():
  result = [reconstructRgb_hexVariant(hexGroup) for hexGroup in hexGroupList]
  np.testing.assert_almost_equal(result, rgbList, decimal=decimal)
# ----
# ----
def test_rgb_to_intRgb():
  result = [rgbToIntRgb(rgb) for rgb in rgbList]
  assert result == intRgbGroupList

def test_intRgb_to_rgb():
  result = [reconstructRgb(intRgbGroup) for intRgbGroup in intRgbGroupList]
  np.testing.assert_almost_equal(result, rgbList, decimal=decimal)
# ----
# ----
def test_melodyParts_to_hex():
  result = melodyPartsToHexColor(melodyParts)
  for obtainedGroup, expectedGroup in zip(result, hexGroupList):
    assert obtainedGroup == expectedGroup

def test_hex_to_melodyParts():
  result = hexColorToMelodyParts(hexGroupList)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)
# ----
# ----
def test_melodyParts_to_color():
  result = melodyPartsToColor(melodyParts)
  for obtainedGroup, expectedGroup in zip(result, intRgbGroupList):
    assert obtainedGroup == expectedGroup

def test_color_to_melodyParts():
  result = colorToMelodyParts(intRgbGroupList)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)
# ----
# ----
def test_full_conversion_hex():
  hexColors = melodyPartsToHexColor(melodyParts)
  result = hexColorToMelodyParts(hexColors)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)

def test_full_conversion_color():
  colors = melodyPartsToColor(melodyParts)
  result = colorToMelodyParts(colors)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=decimal)
# ----
# ----
# ----
# ----
# READ FIRST!
# Used to populate __data.py. Only to be used if anything inside __melody.py
# changes, which will also make it necessary to update hlsList, rgbList,
# hexGroupList, and intRgbGroupList. If function is invoked for any other
# reason, test results may be unreliable.
def __update_data__():
  # Building hlsList is near identical to _melodyPartsLoop within convert.py
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
    if volumePtr < len(volumeChanges):
      volumeT, volumeValue = volumeChanges[volumePtr]
      if t == volumeT:
        l = volumeValue
        volumePtr += 1

    hlsList.append((h, l, s))

  rgbList = [hlsToRgb(hls) for hls in hlsList]
  hexGroupList = melodyPartsToHexColor(melodyParts)
  intRgbGroupList = melodyPartsToColor(melodyParts)
  import os
  path = os.getcwd()
  with open(f'{path}/__data.py', 'w+') as f:
    f.write(f'hlsList={hlsList}\n'.replace(' ', ''))
    f.write(f'rgbList={rgbList}\n'.replace(' ', ''))
    f.write(f'hexGroupList={hexGroupList}\n'.replace(' ', ''))
    f.write(f'intRgbGroupList={intRgbGroupList}\n'.replace(' ', ''))

