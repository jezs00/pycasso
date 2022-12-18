# Unit tests for provider.py
import keyring

from constants import ProvidersConst


def test_stability_get_secret():
    keyring.get_keyring()
    keyring.set_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.STABLE_KEYNAME.value, "TEST")
    result = keyring.get_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.STABLE_KEYNAME.value)
    expected = "TEST"
    assert result == expected


def test_dalle_get_secret():
    keyring.get_keyring()
    keyring.set_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.DALLE_KEYNAME.value, "TEST")
    result = keyring.get_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.DALLE_KEYNAME.value)
    expected = "TEST"
    assert result == expected
