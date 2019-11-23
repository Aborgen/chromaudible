from enum import Enum
from flask import Flask
from flask import jsonify
from flask import request
from exceptions.NotFound import NotFound

class EType(Enum):
  AUDIO  = 'audio'
  CANVAS = 'canvas'

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
  uploadType = request.form.get('type')
#  f = request.files['upload']
#  f.save
  if uploadType == EType.AUDIO.value:
    #return audioToCanvas(f)
    return "GOT AUDIO"
  elif uploadType == EType.CANVAS.value:
    #return canvasToAudio(f)
    return "GOT CANVAS"
  else:
    msg = ''
    if not uploadType:
      msg = "To call this route, there must be an argument provided to type [type=audio]"
    else:
      msg = f"The upload type {uploadType} is not supported"
    raise NotFound(msg)

@app.errorhandler(NotFound)
def handleNotFound(error):
  response = jsonify(error.toDict())
  response.status_code = error.statusCode
  return response
