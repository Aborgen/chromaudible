from .config import tempDir
from enum import Enum
from .exceptions.NotFound import NotFound
from .exceptions.UnprocessableEntity import UnprocessableEntity
from .exceptions.UnsupportedMediaType import UnsupportedMediaType
from flask import Flask
from flask import jsonify
from flask import request
from magic import Magic
import os
from tempfile import mkstemp
from typing import List, Tuple
from .transform import fromAudio
from .transform import fromImage
from werkzeug.exceptions import InternalServerError

class EType(Enum):
  AUDIO = 'audio'
  IMAGE = 'image'

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
  uploadType = request.form.get('type').lower()
  f = request.files['file']
  correctFileType, typeOptions = examineFile(f, uploadType)
  if not correctFileType:
    raise UnprocessableEntity(f'File type is inconsistent: (Expected: {uploadType}, Got: {typeOptions[0]})')

  if uploadType == EType.AUDIO.value:
    fileBase, _ = f.filename.split('.')
    fileIn = saveFile(f, f"{fileBase}_in")
    try:
      colors = fromAudio(fileIn)
      return prepareJSON(colors)
    except:
      raise UnprocessableEntity(f'Audio file is corrupted and cannot be loaded')

  elif uploadType == EType.IMAGE.value:
    return prepareJSON(fromImage(f))
  else:
    msg = ''
    if not uploadType:
      msg = "To call this route, there must be an argument provided to type [type=audio|image]"
      raise NotFound(msg)
    else:
      msg = f"The upload type {uploadType} is not supported"
      raise UnsupportedMediaType(msg)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response

def saveFile(f, filename: str) -> str:
  fileDiscriptor, tempFile = mkstemp(dir=tempDir)
  f.save(tempFile)
  os.close(fileDiscriptor)
  return tempFile

def examineFile(f, fileType: str) -> Tuple[bool, List[str]]:
  f.seek(0)
  magic = Magic(mime=True, keep_going=True)
  mimetype = magic.from_buffer(f.read(2048)).split('/')[0]
  # Mp3 files pose interesting problems in mimetype detection
  if f.filename.split('.')[-1] == 'mp3' and mimetype != 'audio':
    mimetype = 'audio'

  f.seek(0)
  types = [mimetype, f.mimetype.split('/')[0]]
  status = all(fileType == x for x in types)
  return (status, types)

def prepareJSON(responseBundle: dict):
  return jsonify(responseBundle)

@app.errorhandler(NotFound)
@app.errorhandler(UnprocessableEntity)
@app.errorhandler(UnsupportedMediaType)
def handleError(error):
  response = prepareJSON(error.toDict())
  response.status_code = error.statusCode
  return response

@app.errorhandler(InternalServerError)
def syntaxError(error):
  response = prepareJSON({'message':'There is an issue with the server'})
  response.status_code = 500
  return response
