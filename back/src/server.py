from config import tempDir
from enum import Enum
from exceptions.NotFound import NotFound
from flask import Flask
from flask import jsonify
from flask import request
import os
from tempfile import mkstemp
from transform import fromAudio

class EType(Enum):
  AUDIO  = 'audio'
  CANVAS = 'canvas'

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
  uploadType = request.form.get('type').lower()
  f = request.files['file']
  fileBase, _ = f.filename.split('.')
  fileIn = saveFile(f, f"{fileBase}_in")
  if uploadType == EType.AUDIO.value:
    return prepareJSON(fromAudio(fileIn))
  elif uploadType == EType.CANVAS.value:
    #return fromCanvas(fileIn)
  else:
    msg = ''
    if not uploadType:
      msg = "To call this route, there must be an argument provided to type [type=audio]"
    else:
      msg = f"The upload type {uploadType} is not supported"

    raise NotFound(msg)

def saveFile(f, filename: str) -> str:
  fileDiscriptor, tempFile = mkstemp(dir=tempDir)
  f.save(tempFile)
  os.close(fileDiscriptor)
  return tempFile
  
def prepareJSON(responseBundle: dict):
  return jsonify(responseBundle)

@app.errorhandler(NotFound)
def handleNotFound(error):
  response = prepareJSON(error.toDict())
  response.status_code = error.statusCode
  return response
