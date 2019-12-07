import warnings
# Turn off tensorflow warnings from spleeter library
warnings.filterwarnings('ignore')

from config import sampleRate
from config import tempDir
import librosa
import numpy as np
import os
from pathlib import Path
from spleeter.separator import Separator
from tempfile import mkdtemp
from typing import List, Tuple
import vamp

def fromAudio(tempFile: str):
  outDir = Path(mkdtemp(dir=tempDir))
  vocals, drums = isolateAudio(tempFile, outDir)
  os.unlink(tempFile)
  bpm = getBPM(drums)
  return { 
    'bpm': bpm,
    'melody': extractMelody(vocals, bpm),
    'volumeChanges': detectVolumeChanges(vocals),
    'silenceRanges': detectSilence(drums),
    'melodyFlavor': centroid(vocals)
  }

# Use spleeter to separate audio file into vocals and drums, and then
# return those same wavelengths
def isolateAudio(tempFile: str, outDir: Path) -> Tuple[np.ndarray, np.ndarray]:
  separator = Separator('spleeter:4stems')
  separator.separate_to_file(tempFile, str(outDir), filename_format='{instrument}.{codec}')

  vocals, _ = librosa.load(outDir / 'vocals.wav', sampleRate, mono=True)
  drums, _ = librosa.load(outDir / 'drums.wav', sampleRate, mono=True)
  return (vocals, drums) 

# The idea is to know at what timestamps(ms) the 'loudness' changes, and
# what, in mels, it has changed to.
def detectVolumeChanges(y: np.ndarray) -> np.ndarray:
  S = librosa.feature.melspectrogram(y, sampleRate, power=1)
  summedMel = np.round(S.sum(axis=0), 2)
  timestamps = librosa.core.frames_to_time(np.arange(summedMel.shape[0]), sampleRate)

  volumeChanges = []
  previousMel = 0.0
  # I am only interested in new mels and their corresponding timestamp:
  # when does the volume change?
  for m, t in zip(summedMel, timestamps):
    if m == 0.0 or m == previousMel:
      continue

    ms = int(round(t * 1000))
    volumeChanges.append((round(m, 2), ms))
    previousMel = m

  return np.asarray(volumeChanges)

# Based on plugin author's notebook:
# https://github.com/justinsalamon/melodia_python_tutorial/blob/master/melodia_python_tutorial.ipynb
def extractMelody(y: np.ndarray, bpm: int) -> List[Tuple[float, int]]:
  melody = vamp.collect(y, sampleRate, "mtg-melodia:melodia")['vector'][1]
  timestamps = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
  melodyAtTime = [(f, int(round(t * 1000))) for f, t in zip(melody, timestamps)]
  return np.asarray(melodyAtTime)

# Not entirely sure if this does what I need it to. The idea is to get a
# sense of the 'quality' (timbre) of the singer's voice as a float. This float
# will be found within a range, which matches to a synth 'voice' in the frontend.
def centroid(y: np.ndarray) -> float:
  centers = librosa.feature.spectral_centroid(y, sampleRate)[0]
  return centers

# As the name implies, return the silence ranges [start, end] that are longer
# than threshold. On the frontend, there will be some drum track playing
# continuously except for the time ranges from this function.
def detectSilence(y: np.ndarray, threshold = 1000) -> np.ndarray
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

