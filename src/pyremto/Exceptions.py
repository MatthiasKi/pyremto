class PyremtoException(Exception):
    pass

class PyremtoCommunicationError(PyremtoException):
    pass

class PyremtoJobsAlreadySetupError(PyremtoException):
    pass

class PyremtoAuthenticationError(PyremtoException):
    pass

class PyremtoMemoryExceededError(PyremtoException):
    pass