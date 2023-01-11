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
