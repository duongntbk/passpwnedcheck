'''
Test for util methods
'''

import passpwnedcheck.constants as constants
import pytest
from passpwnedcheck.utils import get_password_prefix_suffix, response_to_dict


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
        prefix, suffix = get_password_prefix_suffix(ps)
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
            get_password_prefix_suffix(ps)
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
        assert response_to_dict(response_text) == result


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
            response_to_dict(response_text)
        assert str(te.value) == constants.RESPONSE_FORMAT_ERROR_MSG
