#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Post class to wrap posting to third party websites
import io
import logging

from mastodon import Mastodon
from piblo.constants import ProvidersConst, PosterConst, ConfigConst


class PostWrapper(object):
    """
    A superclass used to post image and text to third party websites.

    Attributes
    ----------

    Methods
    -------
    post_image(img, text)
        Posts an image to the website of choice.

    """

    def __init__(self, user=None, password=None):
        self.user = user
        self.password = password
        if self.user is None:
            logging.warning("Username not provided. Post service may not function correctly")
            return None

        if self.host is None:
            logging.warning("Password not provided. Post service may not function correctly")
            return None

        try:
            self.authenticate()

        except BaseException as e:
            logging.warning(e)
            return
        return

    def post_image(self, img, text):
        return


class MastodonPoster(PostWrapper):

    # inherits from Post
    def __init__(self, mode=ProvidersConst.USE_KEYCHAIN.value, creds_path=ProvidersConst.CREDENTIAL_PATH.value,
                 client_cred_file=ConfigConst.MASTODON_CLIENT_CRED_PATH.value,
                 user_cred_file=ConfigConst.MASTODON_USER_CRED_PATH.value):
        self.mode = mode
        self.creds_path = creds_path
        self.client_cred_file = client_cred_file
        self.user_cred_file = user_cred_file
        self.mastodon = Mastodon(client_id=self.client_cred_file, access_token=self.user_cred_file)
        return

    def post_image(self, img, text):
        try:
            buffer = io.BytesIO()
            img.save(buffer, format=PosterConst.MASTODON_IMG_FORMAT.value)
            media_dict = self.mastodon.media_post(buffer.getvalue(), mime_type=PosterConst.MASTODON_MIME_FORMAT.value,
                                                  description=text)
            self.mastodon.status_post(text, media_ids=media_dict)
        except Exception as e:
            logging.error(e)
        return

    def authenticate(self, user, password):
        self.mastodon.log_in(
            user,
            password,
            to_file=self.user_cred_file
        )
        return self.user_cred_file

    @staticmethod
    def create_app(app_name, base_url, client_cred_path):
        Mastodon.create_app(
            app_name,
            api_base_url=base_url,
            to_file=client_cred_path
        )
