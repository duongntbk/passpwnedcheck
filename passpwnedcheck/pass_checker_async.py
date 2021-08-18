# -*- coding: utf-8 -*-

"""
This module checks for password pwnage using k-anonimity.
All remote calls are non-blocking.
"""

import asyncio

from requests.compat import urljoin

import passpwnedcheck.constants as constants
from passpwnedcheck.utils import get_password_prefix_suffix, response_to_dict


class PassCheckerAsync:
    '''
    This is the non-blocking version of PassChecker.
    It supports both checking a single password and multiple passwords.
    '''

    def __init__(self, session):
        self._session = session

    async def is_passwords_compromised(self, passwords, batch_size=constants.BATCH_SIZE):
        '''
        Check multiple passwords to see if they are compromised.
        Calls are made to haveibeenpwned in batch and are non-blocking.
        '''

        rs = {}

        batch_generator = self._batch_generator(passwords, batch_size)
        for batch in batch_generator:
            tasks = []

            for password in batch:
                task_run = self.is_password_compromised(password)
                task = asyncio.ensure_future(task_run)
                tasks.append(task)

            batch_results = await asyncio.gather(*tasks)

            for password, count in batch_results:
                rs[password] = count

        return rs

    async def is_password_compromised(self, password):
        '''
        This is the non-blocking version of PassChecker.is_password_compromised.
        '''

        prefix, suffix = get_password_prefix_suffix(password)
        url = urljoin(constants.URL, prefix)

        async with self._session.get(url) as response:
            response_text = await self._ensure_success(response)
            response_dict = response_to_dict(response_text)

            if suffix in response_dict:
                return password, response_dict[suffix]
            else:
                return password, 0

    def _batch_generator(self, collection, batch_size):
        '''
        This method returns a generator which batches the input into smaller chunks.
        '''

        head_index = 0
        while (head_index < len(collection)):
            yield collection[head_index:head_index+batch_size]
            head_index += batch_size

    async def _ensure_success(self, response):
        '''
        Make sure that the status code of a response is 200 OK.
        '''

        status = response.status
        response_text = await response.text()

        if status == 200:
            return response_text
        else:
            raise ConnectionError(constants.RESPONSE_CODE_ERROR_MSG + response_text)
