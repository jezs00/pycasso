#!/usr/bin/python
# -*- coding:utf-8 -*-

# Small script to set keys
import logging

from src import StabilityProvider, DalleProvider, ProvidersConst

logging.basicConfig(level=logging.DEBUG)

print("Set key for provider")
mode = int(input(f"---Available Providers---\n"
                 f"[{ProvidersConst.STABLE.value}] - Stable Diffusion\n"
                 f"[{ProvidersConst.DALLE.value}] - Dalle\n"
                 f"-------------------------\n"
                 f"Choose Provider:"))
key = input("\nAPI key:")

if mode == ProvidersConst.STABLE.value:
    StabilityProvider.add_secret(key)
elif mode == ProvidersConst.DALLE.value:
    DalleProvider.add_secret(key)

print("Added key OK")
