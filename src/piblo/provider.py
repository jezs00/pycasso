#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Provider class to wrap APIs for web operations
import configparser
import io
import logging
import os
import warnings
from io import BytesIO

import keyring
import openai
import requests
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image, ImageDraw
from stability_sdk import client

from .constants import ProvidersConst, StabilityConst, DalleConst, ConfigConst
from .file_operations import FileOperations
from .image_functions import ImageFunctions


class Provider(object):
    """
    A superclass used to wrap APIs for web operations from pycasso.

    Attributes
    ----------

    Methods
    -------
    get_image_from_string(text)
        Retrieves image from API. Returns PIL Image object.

    resize_image(img, width, height)
        Resizes image object img to fill width, height

    read_creds(keyname, path, example_path)
        Reads credentials from .creds file with variable name 'keyname'. 'path' and 'example_path' default to constant
        location.
        Returns the key as a string

    add_secret(text):
        Adds a secret 'text' to the keyring for the appropriate provider

    get_secret(text):
        Retrieves appropriate secret from the keyring for the appropriate provider
    """

    def __init__(self):
        return

    def get_image_from_string(self, text):
        return

    @staticmethod
    def resize_image(img, width, height):
        tup = (width, height)
        tup = ImageFunctions.max_tup(tup)
        img.thumbnail(tup)
        return img

    @staticmethod
    def read_creds(keyname, path=ProvidersConst.CREDENTIAL_PATH.value,
                   example_path=ProvidersConst.CREDENTIAL_PATH_EG.value):
        # Create new config file if necessary
        path = FileOperations.backup_file(path, example_path)

        # Method to read config file settings
        config = configparser.ConfigParser()
        config.read(path)

        key = ""
        if os.path.exists(path):
            key = config.get(ProvidersConst.CREDENTIAL_SECTION.value, keyname)

        return key

    @staticmethod
    def add_secret(text):
        pass

    @staticmethod
    def get_secret():
        pass


class StabilityProvider(Provider):
    stability_api = object

    # inherits from Provider
    def __init__(self, key=None, host=None):
        # Get the inputs if necessary
        super().__init__()
        if key is None:
            stability_key = self.get_secret()
            if stability_key is None:
                warnings.warn("Stability API key not in keychain, environment or provided")
                exit()
        else:
            stability_key = key

        if host is None:
            host = StabilityConst.DEFAULT_HOST.value
            logging.info(f"Using {host} as stability host")

        self.stability_api = client.StabilityInference(
            key=stability_key,
            host=host,
            verbose=False,
        )

        return

    def get_image_from_string(self, text, height=0, width=0):
        fetch_height = ImageFunctions.ceiling_multiple(height, StabilityConst.MULTIPLE.value)
        fetch_width = ImageFunctions.ceiling_multiple(width, StabilityConst.MULTIPLE.value)
        if height == 0 or width == 0:
            answers = self.stability_api.generate(
                prompt=text,
            )
        else:
            answers = self.stability_api.generate(
                prompt=text,
                height=fetch_height,
                width=fetch_width
            )

        # iterating over the generator produces the api response
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the APIs safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                    return None
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
        img = self.resize_image(img, width, height)
        return img

    @staticmethod
    def add_secret(text):
        keyring.get_keyring()
        keyring.set_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.STABLE_KEYNAME.value, text)
        return

    @staticmethod
    def get_secret():
        keyring.get_keyring()
        return keyring.get_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.STABLE_KEYNAME.value)


class DalleProvider(Provider):
    dalle_api = object

    # inherits from Provider
    def __init__(self, key=None, host=None):
        # Get the inputs if necessary
        super().__init__()
        if key is None:
            dalle_key = self.get_secret()
            if dalle_key is None:
                warnings.warn("Dalle API key not in keychain, environment or provided")
                exit()
        else:
            dalle_key = key
        openai.api_key = dalle_key

        return

    def get_image_from_string(self, text, height=0, width=0):

        # Select appropriate size from options in
        res = list(DalleConst.SIZES.value.keys())[0]

        if height != 0 and width != 0:
            for key in DalleConst.SIZES.value:
                if key > height or key > width:
                    res = DalleConst.SIZES.value[key]
                    break

        response = openai.Image.create(prompt=text, n=1, size=res)

        url = response['data'][0]['url']
        img = Image.open(BytesIO(requests.get(url).content))
        return img

    @staticmethod
    def infill_image_from_image(text, img, infill_percent=0):
        # Infills image based on next size up possible from available image
        mask_size = (0, 0)

        for key in DalleConst.SIZES.value:
            res = DalleConst.SIZES.value[key]
            mask_size = (key, key)
            if key > img.height and key > img.height:
                break

        mask = DalleProvider.create_image_mask(img, mask_size)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        mask_bytes = io.BytesIO()
        mask.save(mask_bytes, format='PNG')

        response = openai.Image.create_edit(
            image=mask_bytes.getvalue(),
            mask=mask_bytes.getvalue(),
            prompt=text,
            n=1,
            size=res
        )

        url = response['data'][0]['url']
        img = Image.open(BytesIO(requests.get(url).content))

        # Resize image based on infill_percent
        if infill_percent > 0:
            res = (img.width, img.height)
            new_res = ImageFunctions.resize_tup_smaller(res, infill_percent)
            img.thumbnail(new_res)

        return img

    @staticmethod
    def create_image_mask(img, new_size):
        # Creates an image mask for dalle extending out on all sides equally
        original_width, original_height = img.size
        new_width, new_height = new_size

        image_loc = (original_width / 2, original_height / 2, (original_width + original_width / 2) - 1,
                     (original_height + original_height / 2) - 1)
        mask = Image.new('L', (new_width, new_height), color=0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(image_loc, fill=255)

        image_crop = ImageFunctions.get_crop_size(original_width, original_height, new_width, new_height)
        img = img.crop(image_crop)

        img.putalpha(mask)
        return img

    @staticmethod
    def add_secret(text):
        keyring.get_keyring()
        keyring.set_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.DALLE_KEYNAME.value, text)
        return

    @staticmethod
    def get_secret():
        keyring.get_keyring()
        return keyring.get_password(ProvidersConst.KEYCHAIN.value, ProvidersConst.DALLE_KEYNAME.value)
