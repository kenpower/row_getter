class SpreadSheetNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class NotAGooogleSpreadSheetError(Exception):
    def __init__(self, message):
        self.message = message

class SomeUnknownGooogleSpreadSheetError(Exception):
    def __init__(self, message):
        self.message = message

class PermissionDeniedError(Exception):
    def __init__(self, message):
        self.message = message