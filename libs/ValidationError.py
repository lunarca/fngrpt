class ValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(message)