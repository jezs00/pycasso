#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for provider.py
import os

from piblo.constants import UnitTestConst, ProvidersConst
from piblo.provider import Provider


def test_read_creds():
    directory = os.path.join(os.path.dirname(__file__), UnitTestConst.PROVIDER_FOLDER.value)
    path = os.path.join(directory, UnitTestConst.PROVIDER_CRED.value)
    result = Provider.read_creds(ProvidersConst.DALLE_KEYNAME.value, path)
    expected = "DALLE-Result"
    assert result == expected


def test_write_creds():
    directory = os.path.join(os.path.dirname(__file__), UnitTestConst.PROVIDER_FOLDER.value)
    new_path = os.path.join(directory, UnitTestConst.PROVIDER_CRED_NEW.value)
    path = os.path.join(directory, UnitTestConst.PROVIDER_CRED.value)
    test_key = "Test-Key"

    # Cleanup files before
    if os.path.exists(new_path):
        os.remove(new_path)

    Provider.write_creds(ProvidersConst.MIDJOURNEY_KEYNAME.value, test_key, new_path, path)

    result = Provider.read_creds(ProvidersConst.MIDJOURNEY_KEYNAME.value, new_path)
    expected = test_key
    assert result == expected

    # Cleanup files after
    if os.path.exists(new_path):
        os.remove(new_path)