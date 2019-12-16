import os
from pathlib import Path
from shutil import rmtree

tempDir = Path("../temp")
sampleRate = 44100
melodyParams = { 'minFreq': 55.0, 'maxFreq': 800.0 }
timbreBounds = {
  'minBound': 350.0, 'maxBound': 5000.0,
  'newMin'  : 0,     'newMax'  : 1
}

def _init():
  if os.path.exists(tempDir):
    rmtree(tempDir)

  os.makedirs(tempDir)

_init()

