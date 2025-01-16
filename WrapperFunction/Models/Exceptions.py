"""
This file contains the custom exception classes for the WrapperFunction package.
"""


# Create custom exception class
class MessageException(Exception):
    """
    Custom message exception class
    """
    def __init__(self, code: int, message: str):
        self.code: int = code
        self.message: str = message

