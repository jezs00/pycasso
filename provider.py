# Provider class to wrap APIs for web operations

class Provider:
    """
    A class used to wrap APIs for web operations from pycasso.

    Attributes
    ----------
    provider_type:enum
        provider to be used for all operations

    Methods
    -------

    """

    def __init__(self, provider_type):
        self.provider_type = provider_type
        return
