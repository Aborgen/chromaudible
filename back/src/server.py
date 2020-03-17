from .config import tempDir
from enum import Enum
from .exceptions.NotFound import NotFound
from .exceptions.UnprocessableEntity import UnprocessableEntity
from .exceptions.UnsupportedMediaType import UnsupportedMediaType
from flask import Flask
from flask import jsonify
from flask import request
import magic
import os
from tempfile import mkstemp
from .transform import fromAudio
from .transform import fromImage

class EType(Enum):
  AUDIO = 'audio'
  IMAGE = 'image'

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
  uploadType = request.form.get('type').lower()
  f = request.files['file']
  actualType = getFileType(f, uploadType)
  if uploadType != actualType:
    raise UnprocessableEntity(f'File type is inconsistent: (Expected: {uploadType}, Got: {actualType})')
  if uploadType == EType.AUDIO.value:
    fileBase, _ = f.filename.split('.')
    fileIn = saveFile(f, f"{fileBase}_in")
    return prepareJSON(fromAudio(fileIn))
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
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response

def saveFile(f, filename: str) -> str:
  fileDiscriptor, tempFile = mkstemp(dir=tempDir)
  f.save(tempFile)
  os.close(fileDiscriptor)
  return tempFile

def getFileType(f, fileType: str) -> str:
  f.seek(0)
  mimeType = ''
  if f.filename.split('.')[-1] == 'mp3':
    mimeType = magic.from_buffer(f.read(), mime=True)
  else:
    mimeType = magic.from_buffer(f.read(2048), mime=True)

  f.seek(0)
  return mimeType.split('/')[0]

def prepareJSON(responseBundle: dict):
  return jsonify(responseBundle)

@app.errorhandler(NotFound)
@app.errorhandler(UnprocessableEntity)
@app.errorhandler(UnsupportedMediaType)
def handleError(error):
  response = prepareJSON(error.toDict())
  response.status_code = error.statusCode
  return response
