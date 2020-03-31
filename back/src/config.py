import os
from pathlib import Path
from shutil import rmtree

tempDir = Path("temp")
sampleRate = 44100
denormalizeRgbPasses = 5
melodyBounds = {
  'minBound': 55.0, 'maxBound': 1760.0,
  'newMin'  : 0.05,  'newMax'  : 1.0
}

timbreBounds = {
  'minBound': 350.0, 'maxBound': 5000.0,
  'newMin'  : 0,     'newMax'  : 1.0
}

# The range of loudness is [-1, +1], due to the fact that the values
# are dBFS converted into ampheres utilizing convert.dBFStoGainAmps
loudnessBounds = {
  'minBound': -1.0,     'maxBound': 1.0,
  'newMin'  : 0,        'newMax'  : 1.0
}

def _init():
  if os.path.exists(tempDir):
    rmtree(tempDir)

  os.makedirs(tempDir)

_init()

