from src.config import tempDir
from enum import Enum
from src.exceptions.NotFound import NotFound
from src.exceptions.UnprocessableEntity import UnprocessableEntity
from src.exceptions.UnsupportedMediaType import UnsupportedMediaType
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from typing import List, Tuple
from src.transform import fromAudio
from src.transform import fromImage
from src.utils import examineFile
from src.utils import saveFile

class EType(Enum):
  AUDIO = 'audio'
  IMAGE = 'image'

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(debug=True, middleware=middleware)

@app.route('/upload', methods=['POST'])
async def upload(request):
  form = await request.form()
  uploadType = form['type']
  f = form['file']
  correctFileType, typeOptions = await examineFile(f, uploadType)
  if not correctFileType:
    raise UnprocessableEntity(f'File type is inconsistent: (Expected: {uploadType}, Got: {typeOptions[0]})')

  if uploadType == EType.AUDIO.value:
    fileIn = saveFile(await f.read())
    try:
      colors = fromAudio(fileIn)
      return JSONResponse(colors)
    except Exception as e:
      raise UnprocessableEntity(f'Audio file is corrupted and cannot be loaded')

  elif uploadType == EType.IMAGE.value:
    return JSONResponse(fromImage(f.file))
  else:
    msg = ''
    if not uploadType:
      msg = "To call this route, there must be an argument provided to type [type=audio|image]"
      raise NotFound(msg)
    else:
      msg = f"The upload type {uploadType} is not supported"
      raise UnsupportedMediaType(msg)


  os.close(fileDiscriptor)
  return path




@app.exception_handler(NotFound)
@app.exception_handler(UnprocessableEntity)
@app.exception_handler(UnsupportedMediaType)
def handleError(request, error):
  response = JSONResponse(error.toDict())
  response.status_code = error.statusCode
  return response

#@app.errorhandler(InternalServerError)
#def syntaxError(error):
#  response = prepareJSON({'message':'There is an issue with the server'})
#  response.status_code = 500
#  return response
