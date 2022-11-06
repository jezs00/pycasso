

class ImageFunctions:
    """
    A class used to provide image operations for pycasso.

    Attributes
    ----------

    Methods
    -------
    get_crop_size(original_width, original_height, new_width, new_height)
        returns a tuple to use as crop coordinates when turning original width/height into new width/height
    """

    @staticmethod
    def get_crop_size(original_width, original_height, new_width, new_height):
        # returns a tuple to use as crop coordinates when turning original width/height into new width/height
        width_diff = (new_width - original_width) / 2
        height_diff = (new_height - original_height) / 2
        left_pixel = 0 - width_diff
        top_pixel = 0 - height_diff
        right_pixel = original_width + width_diff
        bottom_pixel = original_height + height_diff
        image_crop = (left_pixel, top_pixel, right_pixel, bottom_pixel)
        return image_crop
