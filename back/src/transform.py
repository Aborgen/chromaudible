import warnings
# Turn off tensorflow warnings from spleeter library
warnings.filterwarnings('ignore')

from .config import melodyBounds
from .config import sampleRate
from .config import tempDir
from .convert import colorToMelodyParts
from .convert import dBFStoGainAmps
from .convert import melodyPartsToColor
from .extract import extractImage
import librosa
import numpy as np
import os
from pathlib import Path
from spleeter.separator import Separator
from tempfile import mkdtemp
from typing import Dict, List, Tuple
import vamp
from werkzeug.datastructures import FileStorage

def fromAudio(tempFile: str):
  outDir = Path(mkdtemp(dir=tempDir))
  vocals, drums = isolateAudio(tempFile, outDir)
  os.unlink(tempFile)
  bpm = getBPM(drums)
#  silenceRanges = detectSilence(drums)
  melodyParts = { 
    'melody': extractMelody(vocals, bpm),
    'volumeChanges': detectVolumeChanges(vocals),
    'timbreTexture': getTimbreTexture(vocals)
  }

  colors = melodyPartsToColor(melodyParts)
  return colors

def fromImage(f: FileStorage):
  ## Use computer vision to extract hexColors from image
  # hexColors = extractHexColors(tempFile)
  # melodyParts = hexColorToMelodyParts(hexColors)
  # return melodyParts
  colors = extractImage(f)
  melodyParts = colorToMelodyParts(colors)
  return melodyParts

# Use spleeter to separate audio file into vocals and drums, and then
# return those same wavelengths
def isolateAudio(tempFile: str, outDir: Path) -> Tuple[np.ndarray, np.ndarray]:
  separator = Separator('spleeter:4stems', stft_backend='librosa')
  separator.separate_to_file(tempFile, outDir, filename_format='{instrument}.{codec}')

  vocals, _ = librosa.load(outDir / 'vocals.wav', sampleRate, mono=True)
  drums, _ = librosa.load(outDir / 'drums.wav', sampleRate, mono=True)
  return (vocals, drums) 

# The idea is to know at what timestamps(ms) the 'loudness' changes, and
# what, in mels, it has changed to.
def detectVolumeChanges(y: np.ndarray, threshold: float = 1.0) -> List[Tuple[float, float]]:
  # Compute power spectrogram, weigh it perceptualy to dBFS values.
  SPower = np.abs(librosa.core.stft(y)) ** 2
  SWeighted = librosa.core.perceptual_weighting(SPower, frequencies=librosa.core.fft_frequencies(sampleRate))
  # Take the average of each spectrogram bin, convert from dBFS to amps in the range [-1, +1]
  gainLevels = dBFStoGainAmps(np.average(SWeighted, axis=0))
  timestamps = librosa.core.frames_to_time(np.arange(gainLevels.shape[0]), sampleRate)
  volumeChanges = []
  previousGain = gainLevels[0]
  previousTime = timestamps[0]
  # Options I came up with to prevent skipping the first timestamp included
  # this, or enumerating the zip to prevent continuing the loop on index 0.
  volumeChanges.append((previousTime, previousGain))
  # I am only interested in new gain values and their corresponding timestamp:
  # when does the loudness change?
  for A, t in zip(gainLevels.tolist(), timestamps.tolist()):
    if A == previousGain or t < previousTime + threshold:
      continue

    volumeChanges.append((t, A))
    previousGain, previousTime = A, t

  return volumeChanges

# Based on plugin author's notebook:
# https://github.com/justinsalamon/melodia_python_tutorial/blob/master/melodia_python_tutorial.ipynb
def extractMelody(y: np.ndarray, bpm: int) -> List[Tuple[int, float]]:
  params = { 'minfqr': melodyBounds['minBound'], 'maxfqr': melodyBounds['maxBound'] }
  melody = vamp.collect(y, sampleRate, "mtg-melodia:melodia", parameters=params)['vector'][1]
  timestamps = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
  melodyAtTime = []
  for i, (f, t) in enumerate(zip(melody.tolist(), timestamps.tolist())):
    # Due to the inner workings of melodia, the first timestamp is always 24 ms.
    # I need a key of 0 for timing purposes.
    if i == 0:
      melodyAtTime.append((0, f))

    melodyAtTime.append((t, f))

  return melodyAtTime

# Averages the spectral centroids over time. The spectral centroid correlates
# with the 'brightness' of sound
def getTimbreTexture(y: np.ndarray) -> float:
  averageTimbre = np.average(librosa.feature.spectral_centroid(y, sampleRate))
  return averageTimbre

# As the name implies, return the silence ranges [start, end] that are longer
# than threshold. On the frontend, there will be some drum track playing
# continuously except for the time ranges from this function.
def detectSilence(y: np.ndarray, threshold: int = 1000) -> np.ndarray:
  timestamps = librosa.onset.onset_detect(y, sampleRate, units='time')
  timestamps = np.append(timestamps, librosa.get_duration(y, sampleRate))
  timestamps = np.round(timestamps * 1000).astype(int)
  silences = []
  beginRange = endRange = 0
  for i, timestamp in enumerate(timestamps):
    if timestamp > endRange + threshold:
      endRange = timestamp[...]
      if i != len(timestamps) - 1:
        continue
    
    if beginRange != endRange:
      silences.append((beginRange, endRange))

    beginRange = endRange = timestamp[...]

  return np.asarray(silences)

def getBPM(y: np.ndarray) -> int:
  onsetEnvelope = librosa.onset.onset_strength(y, sampleRate)
  return int(round(librosa.beat.tempo(onsetEnvelope, sampleRate)[0]))

