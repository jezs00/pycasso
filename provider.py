# Provider class to wrap APIs for web operations
import io
import os
import warnings

from PIL import Image
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
        Retrieves image from API. Returns PIL Image object.
    """

    def __init__(self):
        return

    def get_image_from_string(self, text):
        return


class StabilityProvider(Provider):
    stability_api = object

    # inherits from Provider
    def __init__(self):
        self.stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'],
            verbose=True,
        )

        return

    def get_image_from_string(self, text):
        # the object returned is a python generator
        answers = self.stability_api.generate(
            prompt=text
        )

        # iterating over the generator produces the api response
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
        return img
