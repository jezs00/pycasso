#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Provider class to wrap APIs for web operations
import base64
import configparser
import io
import logging
import os
import warnings
import webuiapi
from io import BytesIO

import keyring
import openai
import requests
import stability_sdk
from stability_sdk import client
from PIL import Image, ImageDraw

from piblo.constants import ProvidersConst, StabilityConst, DalleConst, AutomaticConst
from piblo.file_operations import FileOperations
from piblo.image_functions import ImageFunctions


class Provider(object):
    """
    A superclass used to wrap APIs for web operations from pycasso.

    Attributes
    ----------

    Methods
    -------
    get_image_from_string(text)
        Retrieves image from API. Returns PIL Image object. Returns 'None' object on failure

    resize_image(img, width, height)
        Resizes image object img to fill width, height. Returns PIL Image object.

    fit_image(img, width, height)
        Resizes image object so that it can be shown on screen with no black space. Returns PIL Image object.

    read_creds(keyname, path, example_path)
        Reads credentials from .creds file with variable name 'keyname'. 'path' and 'example_path' default to constant
        location.
        Returns the key as a string

    add_secret(text):
        Adds a secret 'text' to the keyring for the appropriate provider

    get_secret(text):
        Retrieves appropriate secret from the keyring for the appropriate provider
    """

    def __init__(self, key=None, keyname=None, creds_mode=ProvidersConst.USE_KEYCHAIN,
                 creds_path=ProvidersConst.CREDENTIAL_PATH.value):
        self.key = key
        self.creds_mode = creds_mode
        self.creds_path = creds_path
        self.keychain = ProvidersConst.KEYCHAIN.value
        self.keyname = keyname
        self.host = None
        return

    def get_image_from_string(self, text):
        return

    def load_key(self, key=None, mode=ProvidersConst.USE_KEYCHAIN.value, path=ProvidersConst.CREDENTIAL_PATH.value):

        return

    def get_secret(self):
        if self.keychain is None:
            warnings.warn("Keychain is empty")
            exit()
        if self.key is None:
            self.key = self.process_get_secret(keychain=self.keychain, keyname=self.keyname, mode=self.creds_mode,
                                               path=self.creds_path)
            if self.key is None:
                warnings.warn(f"'{self.keyname}' API key not in keychain, environment or provided")
                exit()
        pass

    @staticmethod
    def resize_image(img, width, height):
        tup = (width, height)
        tup = ImageFunctions.max_tup(tup)
        img.thumbnail(tup)
        return img

    @staticmethod
    def fit_image(img, width, height):
        tup = (width, height)
        large_tup = (img.width, img.height)
        tup = ImageFunctions.min_possible_tup(tup, large_tup)
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
    def write_creds(keyname, key, path=ProvidersConst.CREDENTIAL_PATH.value,
                    example_path=ProvidersConst.CREDENTIAL_PATH_EG.value):
        # Create new config file if necessary
        path = FileOperations.backup_file(path, example_path)

        # Method to read config file settings
        config = configparser.ConfigParser()
        config.read(path)

        if os.path.exists(path):
            config.set(ProvidersConst.CREDENTIAL_SECTION.value, keyname, key)
            with open(path, 'w') as file:
                config.write(file)
        return

    @staticmethod
    def add_secret(text, mode=ProvidersConst.USE_KEYCHAIN, path=ProvidersConst.CREDENTIAL_PATH.value):
        pass

    @staticmethod
    def process_add_secret(keychain, keyname, text, mode=ProvidersConst.USE_KEYCHAIN.value,
                           path=ProvidersConst.CREDENTIAL_PATH.value):
        if mode:
            keyring.get_keyring()
            keyring.set_password(keychain, keyname, text)
        else:
            Provider.write_creds(keyname, text, path)
        return

    @staticmethod
    def process_get_secret(keychain, keyname, mode=ProvidersConst.USE_KEYCHAIN.value,
                           path=ProvidersConst.CREDENTIAL_PATH.value):
        if mode:
            keyring.get_keyring()
            key = keyring.get_password(keychain, keyname)
        else:
            key = Provider.read_creds(keyname, path)
        return key


class StabilityProvider(Provider):
    stability_api = object

    # inherits from Provider
    def __init__(self, key=None, host=None, creds_mode=ProvidersConst.USE_KEYCHAIN,
                 creds_path=ProvidersConst.CREDENTIAL_PATH.value):
        super().__init__(key=key, keyname=ProvidersConst.STABLE_KEYNAME.value, creds_mode=creds_mode,
                         creds_path=creds_path)
        self.get_secret()

        self.host = host
        if self.host is None:
            self.host = StabilityConst.DEFAULT_HOST.value

        logging.info(f"Using {host} as stability host")

        return

    def get_image_from_string(self, text, height=0, width=0):
        try:
            fetch_height = ImageFunctions.ceiling_multiple(height, StabilityConst.MULTIPLE.value)
            fetch_width = ImageFunctions.ceiling_multiple(width, StabilityConst.MULTIPLE.value)

            url = self.host

            body = {
                "width": fetch_width,
                "height": fetch_height,
                "steps": 50,
                "seed": 0,
                "cfg_scale": 7,
                "samples": 1,
                "style_preset": "enhance",
                "text_prompts": [
                    {
                        "text": text,
                        "weight": 1
                    }
                ],
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.key}",
            }

            response = requests.post(
                url,
                headers=headers,
                json=body,
            )

            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            data = response.json()

            for i, image in enumerate(data["artifacts"]):
                img = Image.open(BytesIO(base64.b64decode(image["base64"])))

            img = self.fit_image(img, width, height)

        except BaseException as e:
            logging.error(e)
            return None

        return img

    @staticmethod
    def add_secret(text, mode=ProvidersConst.USE_KEYCHAIN.value, path=ProvidersConst.CREDENTIAL_PATH.value):
        Provider.process_add_secret(ProvidersConst.KEYCHAIN.value, ProvidersConst.STABLE_KEYNAME.value, text=text,
                                    mode=mode, path=path)
        return


class DalleProvider(Provider):
    dalle_api = object

    # inherits from Provider
    def __init__(self, key=None, creds_mode=ProvidersConst.USE_KEYCHAIN,
                 creds_path=ProvidersConst.CREDENTIAL_PATH.value):
        super().__init__(key=key, keyname=ProvidersConst.DALLE_KEYNAME.value, creds_mode=creds_mode,
                         creds_path=creds_path)

        self.get_secret()

        openai.api_key = self.key
        return

    def get_image_from_string(self, text, height=0, width=0):
        try:
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

        except openai.error.APIConnectionError as e:
            logging.error(e)
            logging.error("Unable to contact OpenAI. Internet or provider may be down.")
            return None
        except openai.error.APIError as e:
            logging.error(e)
            return None
        except openai.error.AuthenticationError as e:
            logging.error(e)
            logging.error("Error authenticating with OpenAI. Please check your credentials in '.creds'.")
            return None
        except openai.error.InvalidAPIType as e:
            logging.error(e)
            return None
        except openai.error.InvalidRequestError as e:
            logging.error(e)
            return None
        except openai.error.OpenAIError as e:
            logging.error(e)
            return None
        except openai.error.PermissionError as e:
            logging.error(e)
            return None
        except openai.error.RateLimitError as e:
            logging.error(e)
            logging.error("OpenAI reporting Rate Limiting. Please check your account at openai.com.")
            return None
        except openai.error.ServiceUnavailableError as e:
            logging.error(e)
            return None
        except openai.error.SignatureVerificationError as e:
            logging.error(e)
            return None
        except openai.error.Timeout as e:
            logging.error(e)
            logging.error("Timeout contacting OpenAI. Internet or provider may be down.")
            return None
        except openai.error.TryAgain as e:
            logging.error(e)
            return None
        except BaseException as e:
            logging.error(e)
            return None

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
    def add_secret(text, mode=ProvidersConst.USE_KEYCHAIN.value, path=ProvidersConst.CREDENTIAL_PATH.value):
        Provider.process_add_secret(ProvidersConst.KEYCHAIN.value, ProvidersConst.DALLE_KEYNAME.value, text, mode, path)
        return


class AutomaticProvider(Provider):
    automatic_api = object

    # inherits from Provider
    def __init__(self, host=None, port=None):
        # Get the inputs if necessary
        super().__init__()

        if host is None:
            host = AutomaticConst.DEFAULT_HOST.value
            logging.info(f"Using {host} as Automatic host")

        if port is None:
            port = AutomaticConst.DEFAULT_PORT.value
            logging.info(f"Using {port} as Automatic port")

        self.automatic_api = webuiapi.WebUIApi(
            host=host,
            port=port
        )

        return

    def get_image_from_string(self, text, height=0, width=0):
        try:
            fetch_height = ImageFunctions.ceiling_multiple(height, AutomaticConst.MULTIPLE.value)
            fetch_width = ImageFunctions.ceiling_multiple(width, AutomaticConst.MULTIPLE.value)
            if height == 0 or width == 0:

                answers = self.automatic_api.txt2img(
                    prompt=text,
                    steps=60
                )

            else:
                answers = self.automatic_api.txt2img(
                    prompt=text,
                    steps=60,
                    height=fetch_height,
                    width=fetch_width
                )

            img = answers.image
            img = self.fit_image(img, width, height)

        except BaseException as e:
            logging.error(e)
            return None

        return img
