#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Post class to wrap posting to third party websites
import logging

from mastodon import Mastodon


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

    def authenticate(self):
        return

    def post_image(self, img, text):
        return


class MastodonPost(PostWrapper):

    # inherits from Post
    def __init__(self, client_cred_file=None, user_cred_file=None):
        self.client_cred_file = client_cred_file
        self.user_cred_file = user_cred_file
        self.mastodon = Mastodon(access_token=self.user_cred_file)
        return

    def authenticate(self):
        self.mastodon.log_in(
            self.user,
            self.password,
            to_file=self.cred_file
        )
        return

    def post_image(self, img, text):
        return

    def register(self, img, text):
        return
