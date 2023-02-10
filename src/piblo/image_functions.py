#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import math
import os

import numpy
from PIL import Image, ImageColor, ImageStat

from piblo.constants import DisplayShapeConst, ConfigConst, IconConst, ImageConst


class ImageFunctions:
    """
    A class used to provide image operations for pycasso.

    Attributes
    ----------

    Methods
    -------
    max_area(area_list)
        Takes an array of tuples and returns the largest area within them
        (a, b, c, d) - will return the smallest value for a,b and largest value for c,d

    set_tuple_bottom(tup, bottom)
        Helper to set fourth element in four element tuple
        In context of application, sets the bottom coordinate of the box

    set_tuple_sides(tup, left, right)
        Helper to set first and third element in four element tuple
        In context of application, sets the left and right coordinates of the box

    ceiling_multiple(number, multiple)
        Helper to find next multiple of 'multiple' for number

    max_tup(tup)
        Takes tuple with 2 values, takes the maximum and returns a tuple both set to the maximum

    min_possible_tup(tup, large_tup)
        Takes a tuple tup, with a larger tuple large_tup, and provide a tuple with the same ratio as large_tup, as small
        as possible, without either number being smaller than tup.

    resize_number_smaller(number, percent)
        Returns integer 'number' smaller by 'percent' percent

    resize_tup_smaller(tup, percent):
        Returns tuple with all numbers smaller by 'percent' percent

    get_crop_size(original_width, original_height, new_width, new_height)
        Returns a tuple to use as crop coordinates when turning original width/height into new width/height

    add_status_icon(draw, display_shape, icon_padding=5, icon_size=10, icon_width=3, icon_opacity=150)
        Adds a status icon of type 'display_shape' on draw object 'draw'. Draws a rectangle if no display_shape provided
        'icon_padding' sets pixel distance from edge
        'icon_size' sets pixel size of object
        'icon_width' sets line width for icon
        'icon opacity' sets opacity for icon
        returns draw object
    """

    @staticmethod
    def max_area(area_list):
        # initialise
        a, b, c, d = area_list[0]

        # find max for each element
        for t in area_list:
            at, bt, ct, dt = t
            a = min(a, at)
            b = min(b, bt)
            c = max(c, ct)
            d = max(d, dt)
        tup = (a, b, c, d)
        return tup

    @staticmethod
    def set_tuple_bottom(tup, bottom):
        a, b, c, d = tup
        tup = (a, b, c, bottom)
        return tup

    @staticmethod
    def set_tuple_sides(tup, left, right):
        a, b, c, d = tup
        tup = (left, b, right, d)
        return tup

    @staticmethod
    def ceiling_multiple(number, multiple):
        return int(multiple * numpy.ceil(number / multiple))

    @staticmethod
    def max_tup(tup):
        a, b = tup
        max_size = max(a, b)
        tup = (max_size, max_size)
        return tup

    @staticmethod
    def min_possible_tup(tup, large_tup):
        a, b = tup
        al, bl = large_tup

        fac_a = al/a
        fac_b = bl/b

        if fac_a > fac_b:
            factor = fac_b
        else:
            factor = fac_a

        min_tup = (math.ceil(al / factor), math.ceil(bl / factor))
        return min_tup

    @staticmethod
    def resize_number_smaller(number, percent):
        number = number-((number/100)*percent)
        return number

    @staticmethod
    def resize_tup_smaller(tup, percent):
        tup = tuple(ImageFunctions.resize_number_smaller(x, percent) for x in tup)
        return tup

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

    @staticmethod
    def add_status_icon(draw, display_shape, icon_padding=5, icon_size=10, icon_width=3, icon_opacity=150):
        status_corner = icon_padding + icon_size
        status_box = (icon_padding, icon_padding, status_corner, status_corner)
        if display_shape == DisplayShapeConst.CROSS.value:
            draw.rectangle(status_box,
                           width=0,
                           fill=(0, 0, 0, icon_opacity))
            draw.line(status_box,
                      width=icon_width,
                      fill=(255, 255, 255, icon_opacity))
            status_box = (status_corner, icon_padding, icon_padding, status_corner)
            draw.line(status_box,
                      width=icon_width,
                      fill=(255, 255, 255, icon_opacity))
        elif display_shape == DisplayShapeConst.TRIANGLE.value:
            status_circle = (icon_padding + icon_size / 2, icon_padding
                             + icon_size / 2, icon_size / 2)
            draw.regular_polygon(status_circle,
                                 n_sides=3,
                                 fill=(0, 0, 0, icon_opacity),
                                 outline=(255, 255, 255, icon_opacity))
        elif display_shape == DisplayShapeConst.CIRCLE.value:
            draw.ellipse(status_box,
                         width=icon_width,
                         fill=(0, 0, 0, icon_opacity),
                         outline=(255, 255, 255, icon_opacity))
        else:
            draw.rectangle(status_box,
                           width=icon_width,
                           fill=(0, 0, 0, icon_opacity),
                           outline=(255, 255, 255, icon_opacity))
        return draw

    @staticmethod
    def color_icon(img, rgb):
        # From https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color
        if rgb == (0, 0, 0):
            # Don't do anything if we're requesting black
            return img

        data = numpy.array(img)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace black with color
        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = rgb  # Transpose back needed

        img = Image.fromarray(data)
        return img

    @staticmethod
    def is_range_dark(img, area):
        # Uses process 3 from https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image
        # -brightness-using-python
        img = img.crop(area)
        stat = ImageStat.Stat(img)
        brightness = math.sqrt(0.241 * (stat.mean[0] ** 2) + 0.691 * (stat.mean[1] ** 2) + 0.068 * (stat.mean[2] ** 2))
        if brightness < IconConst.BACKGROUND_DARK_LIMIT.value:
            return True
        return False

    @staticmethod
    def set_image_alpha(img, alpha):
        a_channel = img.getchannel('A')
        alpha_quotient = alpha/255

        # Update all opaque pixels
        a_update = a_channel.point(lambda i: i*alpha_quotient if i > 0 else 0)
        img.putalpha(a_update)
        return

    @staticmethod
    def draw_icons(image_base, icons, icon_path=ConfigConst.ICON_PATH.value, icon_color=ConfigConst.ICON_COLOR.value,
                   icon_location=ConfigConst.ICON_CORNER.value, icon_padding=ConfigConst.ICON_PADDING.value,
                   icon_size=ConfigConst.ICON_SIZE.value, icon_gap=ConfigConst.ICON_GAP.value,
                   icon_opacity=ConfigConst.ICON_OPACITY.value):
        if len(icons) == 0:
            # Don't bother doing all the rest if the list is empty
            return image_base

        icon_point = icon_padding + icon_size

        # Default to top left
        x = icon_padding
        y = icon_padding
        left_to_right = True
        bright_zone = (0, 0, image_base.width, icon_point)

        if icon_location == IconConst.LOC_TOP_RIGHT.value:
            x = image_base.width - icon_point
            left_to_right = False
        elif icon_location == IconConst.LOC_BOTTOM_LEFT.value:
            y = image_base.height - icon_point
            bright_zone = (0, y, image_base.width, image_base.height)
        elif icon_location == IconConst.LOC_BOTTOM_RIGHT.value:
            x = image_base.width - icon_point
            y = image_base.height - icon_point
            left_to_right = False
            bright_zone = (0, y, image_base.width, image_base.height)

        # Set icons in order of weight
        icons.sort(key=lambda item: item[1])

        color = (0, 0, 0)
        # Get color
        if icon_color == "auto":
            # Set color differently based on brightness of area
            if ImageFunctions.is_range_dark(image_base, bright_zone):
                color = (255, 255, 255)
        else:
            color = ImageColor.getcolor(icon_color, ImageConst.CONVERT_MODE.value)

        for icon in icons:
            path = os.path.join(icon_path, icon[0])
            if os.path.exists(path):
                img = Image.open(path)
                img = img.convert(ImageConst.DRAW_MODE.value)
                img = ImageFunctions.color_icon(img, color)
                ImageFunctions.set_image_alpha(img, icon_opacity)
                tup = (icon_size, icon_size)
                img.resize(tup, resample=0)
                image_base.paste(img, (x, y), img)

                hop = icon_gap + img.width
                if left_to_right:
                    x += hop
                else:
                    x -= hop
            else:
                logging.warning(f"Path to icon '{path}' does not appear to exist.")

        return image_base
