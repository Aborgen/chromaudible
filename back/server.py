from src.config import tempDir
from enum import Enum
from src.exceptions.NotFound import NotFound
from src.exceptions.UnprocessableEntity import UnprocessableEntity
from src.exceptions.UnsupportedMediaType import UnsupportedMediaType
from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.routing import Mount
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from typing import List, Tuple
from src.transform import fromAudio
from src.transform import fromImage
from src.utils import examineFile
from src.utils import saveFile

class EType(Enum):
  AUDIO = 'audio'
  IMAGE = 'image'

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


config = Config('.env')
debug = config('DEBUG', cast=bool, default=False)
environment = config('UVICORN_ENV', cast=str, default='development')
if environment == 'production':
  cors = Middleware(CORSMiddleware, allow_origins=['https://0.0.0.0:80'])
  homepage = Mount('/', StaticFiles(directory='dist', html=True))
elif environment == 'development':
  cors = Middleware(CORSMiddleware, allow_origins=['*'])
  homepage = Route('/', PlainTextResponse('Hello! You are running the server in development mode!'))
else:
  homepage = Route('/', PlainTextResponse('$UNICORN_ENV environment variable is unset'))

routes = [
  Route('/upload', upload, methods=['POST']),
  homepage
]

middleware = [
  cors
]

app = Starlette(debug=debug, routes=routes, middleware=middleware)

@app.exception_handler(NotFound)
@app.exception_handler(UnprocessableEntity)
@app.exception_handler(UnsupportedMediaType)
def handleError(request, error):
  response = JSONResponse(error.toDict())
  response.status_code = error.statusCode
  return response

