class HTTPException(Exception):
    code = None
    message = u''
    headers = {
        'Content-Length': 0,
        'Content-Type': 'application/JSON',
    }


class HTTP401(HTTPException):
    def __init__(self):
        self.code = 401
        self.message = u'Unauthorized'
        self.headers = {
            'Content-Length': 0,
            'Content-Type': 'application/JSON',
            'WWW-Authentication': 'Basic realm="API Key Required"'
        }


class HTTP400(HTTPException):
    def __init__(self):
        self.code = 400
        self.message = u'Bad Request'
        self.headers = {
            'Content-Length': 0,
            'Content-Type': 'application/JSON',
        }
