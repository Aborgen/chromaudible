class NotFound(Exception):
  statusCode = 404
  message = ''
  
  def __init__(self, message):
    self.message = message

  def toDict(self):
    return { 'message': self.message }
