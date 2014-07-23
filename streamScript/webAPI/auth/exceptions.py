class HTTP401(Exception):
    def __init__(self):
        self.code = 401
        self.message = u'Unauthorized'
        self.headers = {}