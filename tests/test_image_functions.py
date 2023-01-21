#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for image_functions.py

from PIL import Image, ImageDraw
from piblo.image_functions import ImageFunctions


def test_max_area():
    func = ImageFunctions()
    area_list = [(40, 180, 80, 240), (20, 220, 50, 300)]
    result = func.max_area(area_list)
    expected = (20, 180, 80, 300)
    assert result == expected


def test_set_tuple_bottom():
    func = ImageFunctions()
    tup = (40, 180, 80, 240)
    bottom = 500
    result = func.set_tuple_bottom(tup, bottom)
    expected = (40, 180, 80, 500)
    assert result == expected


def test_set_tuple_sides():
    func = ImageFunctions()
    tup = (40, 180, 80, 240)
    left = 20
    right = 300
    result = func.set_tuple_sides(tup, left, right)
    expected = (20, 180, 300, 240)
    assert result == expected


def test_ceiling_multiple():
    func = ImageFunctions()
    result = func.ceiling_multiple(91, 10)
    expected = 100
    assert result == expected


def test_max_tup():
    tup = (10, 20)
    result = ImageFunctions.max_tup(tup)
    expected = (20, 20)
    assert result == expected


def test_min_possible_tup_a():
    large_tup = (50, 40)
    tup = (10, 20)
    result = ImageFunctions.min_possible_tup(tup, large_tup)
    expected = (25, 20)
    assert result == expected


def test_min_possible_tup_b():
    large_tup = (23, 77)
    tup = (10, 20)
    result = ImageFunctions.min_possible_tup(tup, large_tup)
    expected = (10, 34)
    assert result == expected


def test_resize_number_smaller():
    number = 100
    percent = 10
    result = ImageFunctions.resize_number_smaller(number, percent)
    expected = 90
    assert result == expected


def test_resize_tup_smaller():
    tup = (100, 200, 500)
    percent = 10
    result = ImageFunctions.resize_tup_smaller(tup, percent)
    expected = (90, 180, 450)
    assert result == expected


def test_get_crop_size():
    func = ImageFunctions()
    original_width = 800
    original_height = 600
    new_width = 450
    new_height = 200
    result = func.get_crop_size(original_width, original_height, new_width, new_height)
    expected = (175, 200, 625, 400)
    assert result == expected


def test_add_status_icon():
    func = ImageFunctions()
    img = Image.new(mode="RGBA", size=(600, 400))
    draw = ImageDraw.Draw(img)
    func.add_status_icon(draw, 0, 10, 20, 5, 255)

    # Check image is not all black
    extrema = img.convert("L").getextrema()

    # Check appropriate pixel is white
    pixel = img.getpixel((10, 10))

    unexpected_extrema = (0, 0)
    expected_pixel = (255, 255, 255, 255)

    assert extrema != unexpected_extrema
    assert pixel == expected_pixel
