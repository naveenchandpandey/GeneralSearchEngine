

class InvalidManagerType(ValueError):
    def __init__(self, message='Invalid Manager Type Provided'):
        self.message = message
        super().__init__(self.message)


class DataUploadException(Exception):
    def __init__(self, message='Error while adding data to index'):
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    def __init__(self, data, message='There seems to be misspelling in the input. Please check. '
                                     'Following are some possible corrections: '):
        self.message = message + str(data)
        super().__init__(self.message)
