#!/usr/bin/python
# -*- coding:utf-8 -*-

# Small script to set keys
import logging

from piblo.provider import StabilityProvider, DalleProvider, ProvidersConst
from piblo.pycasso import Pycasso

instance = Pycasso()

print("Set key for provider")
mode = int(input(f"---Available Providers---\n"
                 f"[{ProvidersConst.STABLE.value}] - Stable Diffusion\n"
                 f"[{ProvidersConst.DALLE.value}] - Dalle\n"
                 f"-------------------------\n"
                 f"Choose Provider:"))
key = input("\nAPI key:")

if mode == ProvidersConst.STABLE.value:
    StabilityProvider.add_secret(key, instance.config.use_keychain, instance.config.credential_path)
elif mode == ProvidersConst.DALLE.value:
    DalleProvider.add_secret(key, instance.config.use_keychain, instance.config.credential_path)

print("Added key OK")
