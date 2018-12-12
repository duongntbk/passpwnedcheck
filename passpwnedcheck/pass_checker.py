# -*- coding: utf-8 -*-

"""
This module checks for password pwnage using k-anonimity.
"""

import sys
from hashlib import sha1

import requests
from requests.compat import urljoin

import passpwnedcheck.constants as constants


class PassChecker:
    '''
    Receive password from input and check for pwnage.

    Use k-anonymity to make sure that server cannot know 
    which password is being checked.

    Step:
      +  Encode input password using utf-8 then hash it using SHA-1.
      +  Send the first 5 characters of hashed value in hex to API.
      +  Check if the rest of hashed value in hex is included in returning data.
      +  If password has been compromised, the rest of hashed value in hex
      and number of compromised times will be included in response data of server.

    This package can be included into other projects
    or called straight from command line.
    '''

    def is_password_compromised(self, password):
        '''
        Check if a password has been compromised
        using pwnedpasswords API
        '''

        prefix, suffix = self.get_password_prefix_suffix(password)
        response = requests.get(urljoin(constants.URL, prefix))
        
        if response.status_code == constants.STATUS_CODE_OK:
            response_dict = self.response_to_dict(response.text)

            if suffix in response_dict:
                return True, response_dict[suffix]

            else:
                return False, 0

        else:
            raise ConnectionError(constants.RESPONSE_CODE_ERROR_MSG + response.reason)

    def get_password_prefix_suffix(self, password):
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

    def response_to_dict(self, text):
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


def main():
    '''
    Entry point of script when run from command line.
    '''

    argvs = sys.argv

    # This script only takes 1 argument,
    # which is the password being checked.
    # Display help message if input is invalid,
    # args[0] is always script's name.
    if len(argvs) != 2: 
        print(constants.HELP_MSG)
        return

    password = argvs[1]
    pc = PassChecker()

    try:
        result, count = pc.is_password_compromised(password)

        if result:
            print(constants.PASSWORD_COMPROMISED_MSG.format(count))

        else:
            print(constants.PASSWORD_NOT_COMPROMISED_MSG)

    except TypeError as te:
        print(constants.INPUT_FORMAT_ERROR_MSG)
        print(str(te))

    except ConnectionError as ce:
        print(constants.CONNECTION_ERROR_MSG)
        print(str(ce))

    except Exception as e:
        print(constants.UNKNOWN_ERROR_MSG)
        print(str(e))


if __name__ == '__main__':
    main()
