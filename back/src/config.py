import os
from pathlib import Path
from shutil import rmtree

tempDir = Path("../temp")
sampleRate = 44100
melodyBounds = {
  'minBound': 55.0, 'maxBound': 800.0,
  'newMin'  : 0,    'newMax'  : 360
}

timbreBounds = {
  'minBound': 350.0, 'maxBound': 5000.0,
  'newMin'  : 0,     'newMax'  : 100
}

loudnessBounds = {
  'minBound': -100.0, 'maxBound': 0,
  'newMin'  : 0,      'newMax'  : 100
}

def _init():
  if os.path.exists(tempDir):
    rmtree(tempDir)

  os.makedirs(tempDir)

_init()

