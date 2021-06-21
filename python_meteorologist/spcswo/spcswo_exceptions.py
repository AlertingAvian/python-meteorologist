"""
Copyright (C) 2021 Patrick Maloney
"""

class InvalidOutlookTypeError(Exception):
    """Raised when the Outlook type is invalid (not 1, 2, or 3)

    Attributes:
        otlk_type -- input outlook type which caused the error
        message -- explanation of the error
    """

    def __init__(self, otlk_type, message="Outlook is not one of (1, 2, 3)"):
        self.otlk_type = otlk_type
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.otlk_type} -> {self.message}'


class OutlookTypeNotSetError(Exception):
    """Raised when the Outlook Type is not set

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Outlook not set. Must be one of (1, 2, 3)"):
        self.message = message
        super().__init__()

    def __str__(self):
        return f'{self.message}'


class UnableToRetrieveSWOError(Exception):
    """Raised when the SWO is unable to be retrieved

    Attributes:
        http_code -- http code when the page was requested
        message -- explanation of the error
    """

    def __init__(self, http_code, message="Unable To Retrieve SWO Page."):
        self.http_code = http_code
        self.message = message
        super().__init__()

    def __str__(self):
        return f'{self.http_code} -> {self.message}'
