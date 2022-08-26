# Provider class to wrap APIs for web operations

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


class Provider:
    """
    A class used to wrap APIs for web operations from pycasso.

    Attributes
    ----------
    provider_type:enum
        provider to be used for all operations

    Methods
    -------
    get_image_from_string(text)
        retrieves image from API. Returns file path of image.
    """

    def __init__(self, provider_type):
        self.provider_type = provider_type
        return

    def get_image_from_string(text):
        return
