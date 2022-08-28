# Provider class to wrap APIs for web operations
import os

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from constants import Providers


class Provider(object):
    """
    A superclass used to wrap APIs for web operations from pycasso.

    Attributes
    ----------

    Methods
    -------
    get_image_from_string(text)
        retrieves image from API. Returns file path of image.
    """

    def __init__(self):
        return

    def get_image_from_string(text):
        return


class StabilityProvider(Provider):
    # inherits from Provider
    def __init__(self, provider_type):
        self.provider_type = provider_type

        # Stable Diffusion Setup
        if provider_type == Providers.STABLE:
            stability_api = client.StabilityInference(
                key=os.environ['STABILITY_KEY'],
                verbose=True,
            )
        return

    def get_image_from_string(text):
        return
