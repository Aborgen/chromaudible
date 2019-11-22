class UnsupportedMediaType(Exception):
  statusCode = 415
  message = ''

  def __init__(self, message):
    self.message = message

  def toDict(self):
    return { 'message': self.message }
