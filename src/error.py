from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'

class NameException(HTTPException):
    code = 400
    message = "Name is invalid"

class KeyError(HTTPException):
    code = 400
    message  = "you're bad"