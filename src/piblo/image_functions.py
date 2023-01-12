#!/usr/bin/python3
# -*- coding:utf-8 -*-

import numpy

from piblo.constants import DisplayShapeConst


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
