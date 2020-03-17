class UnprocessableEntity(Exception):
  statusCode = 422
  message = ''
  
  def __init__(self, message):
    self.message = message

  def toDict(self):
    return { 'message': self.message }
