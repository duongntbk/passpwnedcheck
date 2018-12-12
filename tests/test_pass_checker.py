# -*- coding: utf-8 -*-

"""
Tests for pass_checker.
"""

import sys

import passpwnedcheck.constants as constants
import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from passpwnedcheck.pass_checker import PassChecker
from passpwnedcheck.pass_checker import main as pass_checker_main
from pytest_mock import mocker
from requests.models import Response

pc = PassChecker()
monkeypatch = MonkeyPatch()


def test_get_password_prefix_suffix():
    '''
    Text string can be hashed and divided into prefix and suffix.
    '''

    passes = [
        "password",
        '',
        '日本語',
        '1234567890qwertyuiop!"#$%&\'()"'
    ]

    ffixes = [
        ['5BAA6', '1E4C9B93F3F0682250B6CF8331B7EE68FD8'],
        ['DA39A', '3EE5E6B4B0D3255BFEF95601890AFD80709'],
        ['C1214', '0A0FFB4E56481B4FE0A7A25040C2EAFA9CA'],
        ['FB8A8', '2A3A3A1AFB63D48AF82C3CADC3875C653BC']
    ]

    for ps, ff in zip(passes, ffixes):
        prefix, suffix = pc.get_password_prefix_suffix(ps)
        assert prefix == ff[0] and suffix == ff[1]


def test_get_password_prefix_suffix_wrong_input():
    '''
    If input is not text, raise exception.
    '''

    passes = [
        1,
        [],
        object,
        None
    ]

    for ps in passes:
        with pytest.raises(TypeError) as te:
            pc.get_password_prefix_suffix(ps)
        assert str(te.value) == constants.PASSWORD_FORMAT_ERROR_MSG 


def test_response_to_dict():
    '''
    Response text can be properly converted into dictionary.
    '''

    response_texts = [
        '00F8AFEB99401868422C69E1A119902366A:1\r\n00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3',
        '',
        '00F8AFEB99401868422C69E1A119902366A:1'
    ]

    dicts = [
        {
            '00F8AFEB99401868422C69E1A119902366A': 1,
            '00FE7CEA0FC49CD44FFFE221B4E288E792D': 1,
            '01C91CC3B2BB8575CB715776DE723EF2A25': 8,
            '0246B0E85B76A83FCFDEFFE404046231CD9' :2,
            '024C755EAE375140CC7F5736766A93018FD' :3
        },
        {},
        {'00F8AFEB99401868422C69E1A119902366A': 1}
    ]

    for response_text, result in zip(response_texts, dicts):
        assert pc.response_to_dict(response_text) == result


def test_response_to_dict_wrong_input():
    '''
    If response is not text, raise exception.
    '''

    response_texts = [
        1,
        [],
        object,
        None
    ]

    for response_text in response_texts:
        with pytest.raises(TypeError) as te:
            pc.response_to_dict(response_text)
        assert str(te.value) == constants.RESPONSE_FORMAT_ERROR_MSG 


def test_is_password_compromised():
    '''
    Can send password prefix to API to check for pwnage.
    '''

    response_texts = [
        'CBCD36D02E3B172B788D0CB372D168B30C3:1\r\n00F8AFEB99401868422C69E1A119902366A:1\r\n00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3',
        '00FE7CEA0FC49CD44FFFE221B4E288E792D:1\r\n01C91CC3B2BB8575CB715776DE723EF2A25:8\r\n0246B0E85B76A83FCFDEFFE404046231CD9:2\r\n024C755EAE375140CC7F5736766A93018FD:3'
    ]

    results = [
        (True, 1),
        (False, 0)
    ]

    for response_text, result in zip(response_texts, results):
        response = Response()
        response.status_code = 200
        response._content  = response_text.encode('utf-8')

        with monkeypatch.context() as m:
            m.setattr(requests, 'get', lambda URL: response)
            assert pc.is_password_compromised('dummypassword') == result


def test_is_password_compromised_error():
    '''
    If server returns error code, raise exception.
    '''

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
        response = Response()
        response.status_code = code
        response.reason = msg

        with monkeypatch.context() as m:
            m.setattr(requests, 'get', lambda URL: response)
            with pytest.raises(ConnectionError) as ce:
                pc.is_password_compromised('dummypassword')
            assert str(ce.value) == constants.RESPONSE_CODE_ERROR_MSG + msg


def test_is_password_compromised_prefix_error():
    '''
    If get_password_prefix_suffix raises an exception,
    that exception will propagate to is_password_compromised.
    '''

    def raise_type_error(password):
        raise TypeError('Password must be string')

    with monkeypatch.context() as m:
        m.setattr(pc, 'get_password_prefix_suffix', raise_type_error)
        with pytest.raises(TypeError) as ve:
            pc.is_password_compromised('dummypassword')
        assert str(ve.value) == constants.PASSWORD_FORMAT_ERROR_MSG


def test_is_password_compromised_network_error():
    '''
    If requests.get raises an exception,
    that exception will propagate to is_password_compromised.
    '''
    
    def raise_network_error(url):
        raise Exception('Some error message from requests module')

    with monkeypatch.context() as m:
        m.setattr(requests, 'get', raise_network_error)
        with pytest.raises(Exception) as e:
            pc.is_password_compromised('dummypassword')
        assert str(e.value) == 'Some error message from requests module'


def test_main(mocker):
    '''
    This package can be called straight from command line.
    '''

    argvs_list = [
        ['pass_checker.py', 'password'],
        ['pass_checker.py', 'letmein']
    ]

    results = [
        (True, 1990),
        (False, 0)
    ]

    with monkeypatch.context() as m:
        for argvs, result in zip(argvs_list, results):
            m.setattr(sys, 'argv', argvs)
            mocker.patch.object(PassChecker, 'is_password_compromised')
            PassChecker.is_password_compromised.return_value = result

            pass_checker_main()
            PassChecker.is_password_compromised.assert_called_with(argvs[1])
            assert PassChecker.is_password_compromised(argvs[1]) == result


def test_main_error(mocker):
    '''
    When called from command line, if the number of arguments is not 1 then raise exception.
    '''

    argvs_list = [
        ['pass_checker.py'],
        ['pass_checker.py', 'letmein' , 1],
        ['pass_checker.py', 'letmein' , 1],
        ['pass_checker.py', 0 , 1 ,2 ,3],
        ['pass_checker.py', None, None]
    ]

    with monkeypatch.context() as m:
        for argvs in argvs_list:
            m.setattr(sys, 'argv', argvs)
            mocker.patch.object(PassChecker, 'is_password_compromised')
            PassChecker.is_password_compromised.return_value = (False, 0)

            pass_checker_main()
            PassChecker.is_password_compromised.assert_not_called()
