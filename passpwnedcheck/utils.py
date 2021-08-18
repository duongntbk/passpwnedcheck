# -*- coding: utf-8 -*-

'''
Helper methods used by both pass_checker and pass_checker_async
'''

from hashlib import sha1

import passpwnedcheck.constants as constants


def get_password_prefix_suffix(password):
    '''
    Calculate prefix and suffix for password.

    Prefix: the first 5 characters of hashed value in hex
    of password. This value will be sent to pwnedpasswords API.

    Suffix: the rest of hashed value in hex of password.
    This value won't be sent to API.
    '''

    if not isinstance(password, str):
        raise TypeError(constants.PASSWORD_FORMAT_ERROR_MSG)

    hash = sha1(password.encode('utf-8')).hexdigest()
    return hash[:5].upper(), hash[5:].upper()

def response_to_dict(text):
    '''
    Convert response data from string to dictionary format.
    '''

    if not isinstance(text, str):
        raise TypeError(constants.RESPONSE_FORMAT_ERROR_MSG)

    if not text:
        return {}

    # Create dictionary using dictionary comprehesion.
    return {row.split(constants.DELIMITER)[0]: int(row.split(constants.DELIMITER)[-1]) \
                for row in text.split(constants.LINE_BREAK)}
