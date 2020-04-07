from magic import Magic
import os
from tempfile import mkstemp
from typing import Callable, List, Tuple
from .config import tempDir

# From Jonathan Feinberg's answer on Stackoverflow
# https://stackoverflow.com/a/1701229
def index_of_first(l: List, predicate: Callable):
  for i, v in enumerate(l):
      if predicate(v):
          return i

  return None

def index_of_first_not(l: List, predicate:Callable):
  for i, v in enumerate(l):
      if not predicate(v):
          return i

  return None

def reversed_index_of_first_not(l: List, predicate: Callable) -> int:
  return (len(l)-1) - index_of_first_not(reversed(l), predicate)

def reversed_index_of_first(l: List, predicate: Callable) -> int:
  return (len(l)-1) - index_of_first(reversed(l), predicate)

def saveFile(f) -> str:
  fileDiscriptor, path = mkstemp(dir=tempDir)
  with open(path, 'w+b') as tempfile:
    tempfile.write(f)

  os.close(fileDiscriptor)
  return path

async def examineFile(f, fileType: str) -> Tuple[bool, List[str]]:
  await f.seek(0)
  magic = Magic(mime=True, keep_going=True)
  # Mp3 files pose interesting problems in mimetype detection. Let the audio
  # loading mechanism tell us if it actually is audio.
  if f.filename.split('.')[-1] == 'mp3':
    typeGuess = typeIncluded = 'audio'
  else:
    typeGuess = magic.from_buffer(await f.read(2048)).split('/')[0]
    typeIncluded = f.content_type.split('/')[0]

  await f.seek(0)
  types = [typeGuess, typeIncluded]
  status = all(fileType == mimetype for mimetype in types)
  return (status, types)
