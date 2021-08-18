# -*- coding: utf-8 -*-

"""
Tests for pass_checker_async.
"""

from unittest.mock import Mock

import passpwnedcheck.constants as constants
import pytest
from passpwnedcheck.pass_checker_async import PassCheckerAsync


@pytest.mark.asyncio
async def test_is_password_compromised():
    '''
    Can check a single password.
    '''

    # Arrange
    response_texts = [
        'CBCD36D02E3B172B788D0CB372D168B30C3:1\r\n00F8AFEB99401868422C69E1A119902366A:1\r\n00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3',
        '00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3'
    ]

    results = [1, 0]
    pass_to_check = 'dummypassword'

    for response_text, result in zip(response_texts, results):
        resp = MockResponse(response_text, 200)

        session = Mock()
        session.get.return_value = resp
        pc = PassCheckerAsync(session)

        # Act
        pass_checked, compromised_count = await pc.is_password_compromised(pass_to_check)

        # Assert
        assert pass_checked == pass_to_check
        assert compromised_count == result

@pytest.mark.asyncio
async def test_is_password_compromised_error():
    '''
    If server returns error code, raise exception.
    '''

    # Arrange
    error_codes = [
        403,
        404,
        429,
        500
    ]

    error_msgs = [
        'Forbidden',
        'Not Found',
        'Too Many Requests',
        'Internal Server Error'
    ]

    for code, msg in zip(error_codes, error_msgs):
        resp = MockResponse(msg, code)

        session = Mock()
        session.get.return_value = resp
        pc = PassCheckerAsync(session)

        # Act
        with pytest.raises(ConnectionError) as ce:
            await pc.is_password_compromised('dummypassword')

        # Assert
        assert str(ce.value) == constants.RESPONSE_CODE_ERROR_MSG + msg

@pytest.mark.asyncio
async def test_is_passwords_compromised():
    '''
    Can check multiple passwords.
    '''

    # Arrange
    passwords = [
        'dummypassword',
        'dummypassword1',
        'dummypassword2'
    ]

    response = 'CBCD36D02E3B172B788D0CB372D168B30C3:1\r\nBE23871CC587D104D7099C05C481919B61F:10\r\n00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3'

    results = {
        'dummypassword':1,
        'dummypassword1': 10,
        'dummypassword2': 0
    }

    resp = MockResponse(response, 200)
    session = Mock()
    session.get.return_value = resp
    pc = PassCheckerAsync(session)

    # Act
    actual_results = await pc.is_passwords_compromised(passwords)

    # Assert
    assert actual_results == results

@pytest.mark.asyncio
async def test_is_passwords_compromised_error():
    '''
    If server returns error code, raise exception.
    '''

    # Arrange
    passwords = [
        'dummypassword',
        'dummypassword1',
        'dummypassword2'
    ]

    error_codes = [
        403,
        404,
        429,
        500
    ]

    error_msgs = [
        'Forbidden',
        'Not Found',
        'Too Many Requests',
        'Internal Server Error'
    ]

    for code, msg in zip(error_codes, error_msgs):
        resp = MockResponse(msg, code)

        session = Mock()
        session.get.return_value = resp
        pc = PassCheckerAsync(session)

        # Act
        with pytest.raises(ConnectionError) as ce:
            await pc.is_passwords_compromised(passwords)

        # Assert
        assert str(ce.value) == constants.RESPONSE_CODE_ERROR_MSG + msg

class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
