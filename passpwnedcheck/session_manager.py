# -*- coding: utf-8 -*-

"""
This module helps manage asyncio session.
"""

import aiohttp


class SessionManager:
    '''
    Usage:
    async with SessionManager() as manager:
        session = manager.get_session()
        # code to use session
    '''

    def __init__(self):
        self._session = None

    def get_session(self):
        if not self._session:
            raise Exception('Please use SessionManager inside with statement.')

        return self._session

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None
