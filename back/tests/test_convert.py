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
from src.convert import rgbToHex
from src.convert import rgbToHls
from .__config import hexStringList
from .__config import hlsList
from .__config import melodyParts
from .__config import normMelodyParts
from .__config import rgbList

import json

decimal = 7
def test_normalize_melodyParts():
  result = {
    'melody': normalizeMelody(melodyParts['melody']),
    'volumeChanges': normalizeVolume(melodyParts['volumeChanges']),
    'timbreTexture': normalizeTimbre(melodyParts['timbreTexture'])
  }

  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], normMelodyParts[key], decimal=decimal)

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
  assert result == hexStringList

def test_hex_to_hls():
  result = [hexToHls(hexString) for hexString in hexStringList]
  np.testing.assert_almost_equal(result, hlsList, decimal=decimal)
# ----
# ----
def test_rgb_to_hex():
  result = [rgbToHex(rgb) for rgb in rgbList]
  print(json.dumps(result))
  assert result == hexStringList

def test_hex_to_rgb():
  result = [hexToRgb(hexString) for hexString in hexStringList]
  np.testing.assert_almost_equal(result, rgbList, decimal=decimal)
# ----
# ----
def test_melodyParts_to_hex():
  result = melodyPartsToHexColor(melodyParts)
  for i, (_, got) in enumerate(result.items()):
    assert got == hexStringList[i]

def test_hex_to_melodyParts():
  foo = {i[0]: h for i, h in zip(melodyParts['melody'], hexStringList)}
  result = hexColorToMelodyParts(foo)
  for key in list(melodyParts.keys()):
    np.testing.assert_almost_equal(result[key], melodyParts[key], decimal=0)
