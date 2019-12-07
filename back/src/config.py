import os
from pathlib import Path
from shutil import rmtree

tempDir = Path("../temp")
sampleRate = 44100
def _init():
  if os.path.exists(tempDir):
    rmtree(tempDir)

  os.makedirs(tempDir)

_init()

