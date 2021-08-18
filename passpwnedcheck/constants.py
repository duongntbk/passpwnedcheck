# -*- coding: utf-8 -*-

"""
Constants for pass_checker.
"""

# Constants for pass_checker.
LINE_BREAK = '\r\n'
DELIMITER = ':'
URL = 'https://api.pwnedpasswords.com/range/'
STATUS_CODE_OK = 200
BATCH_SIZE = 10


# Error messages for pass_checker.
PASSWORD_FORMAT_ERROR_MSG = 'Password must be string'
RESPONSE_FORMAT_ERROR_MSG = 'Response text must be string'
RESPONSE_CODE_ERROR_MSG = 'Cannot check pwn site: '
PASSWORD_COMPROMISED_MSG = 'Your password has been compromised {} time(s)'
PASSWORD_NOT_COMPROMISED_MSG = 'Your password has not been compromised (yet)'
INPUT_FORMAT_ERROR_MSG = 'Input parameter or response text from server was in wrong format'
CONNECTION_ERROR_MSG = 'An error occurred while connecting to pwn server: '
UNKNOWN_ERROR_MSG = 'An unknown error occurred while checking password'

# Help message for pass_checker.
HELP_MSG = '\n' + \
            'Input parameter was incorrect\n' + \
            'Usage: # python pass_checker.py [password]' + \
            '\n' + \
            'password : (Required) Password you want to check\n'
