#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

# Small script to set keys
from piblo.pycasso import Pycasso
from piblo.provider import StabilityProvider, DalleProvider
from piblo.constants import ProvidersConst, PosterConst
from piblo.post_wrapper import MastodonPoster

instance = Pycasso()

QUIT = 0
MODE_PROVIDER = 1
MODE_POSTER = 2


def set_provider():
    print("Set key for provider")
    mode = int(input(f"---Available Providers---\n"
                     f"[{ProvidersConst.STABLE.value}] - Stable Diffusion\n"
                     f"[{ProvidersConst.DALLE.value}] - Dalle\n"
                     f"-------------------------\n"
                     f"Choose Provider:"))

    if mode == ProvidersConst.STABLE.value:
        key = input("\nAPI key:")
        StabilityProvider.add_secret(key, mode=instance.config.use_keychain, path=instance.config.credential_path)
        print("Added Stable Diffusion key OK")
    elif mode == ProvidersConst.DALLE.value:
        key = input("\nAPI key:")
        DalleProvider.add_secret(key, mode=instance.config.use_keychain, path=instance.config.credential_path)
        print("Added DALLE key OK")
    else:
        print(f"Invalid option '{mode}'")


def set_poster():
    print("Set details for provider")
    mode = int(input(f"---Available Posters---\n"
                     f"[{PosterConst.MASTODON.value}] - Mastodon\n"
                     f"-----------------------\n"
                     f"Choose Poster:"))

    if mode == PosterConst.MASTODON.value:
        user = input("Username:")
        password = input("Password:")

        register = None
        try:
            while register != "n" and register != "y":
                register = input(f"Register app '{instance.config.mastodon_app_name}' (y/n):")
                register = register.lower()
                if register == "y":
                    MastodonPoster.create_app(instance.config.mastodon_app_name, instance.config.mastodon_base_url,
                                              instance.config.mastodon_client_cred_path)
                    print(f"Registered app '{instance.config.mastodon_app_name}' OK")
                elif register != "n":
                    print(f"Invalid response '{register}'")
        except ValueError as e:
            print(e)
        poster = MastodonPoster(mode=instance.config.use_keychain,
                                client_cred_file=instance.config.mastodon_client_cred_path,
                                user_cred_file=instance.config.mastodon_user_cred_path)

        saved_user_cred = poster.authenticate(user, password)

        print(f"Authenticated user '{user}' OK. Details stored in '{saved_user_cred}'")

    else:
        print(f"Invalid option '{mode}'")

    print("Added details OK")


print("pycasso Credential Management")

choice = None

while choice != QUIT:
    choice = int(input(f"---What To Do?---\n"
                       f"[{QUIT}] - Close Script\n"
                       f"[{MODE_PROVIDER}] - Add Provider Key\n"
                       f"[{MODE_POSTER}] - Add Poster Details\n"
                       f"-----------------\n"
                       f"Choose Mode:"))

    if choice == MODE_PROVIDER:
        set_provider()
    elif choice == MODE_POSTER:
        set_poster()
    elif choice == QUIT:
        print("Closing pycasso Credential Management")
    else:
        print(f"Invalid option '{choice}'")
