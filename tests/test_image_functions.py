#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for image_functions.py
import os.path
from pathlib import Path

from PIL import Image, ImageDraw

from piblo.constants import IconFileConst, ConfigConst, IconConst, ImageConst
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


def test_color_icon():
    img = Image.new(mode="RGBA", size=(600, 400), color="black")
    img = ImageFunctions.color_icon(img, (255, 0, 0))
    red_pixel = img.getpixel((300, 300))
    expected_red_pixel = (255, 0, 0, 255)
    assert red_pixel == expected_red_pixel


def test_is_range_dark():
    img = Image.new(mode="RGBA", size=(600, 400), color="black")
    draw = ImageDraw.Draw(img, ImageConst.DRAW_MODE.value)
    draw.rectangle((0, 0, 600, 200), fill=(255, 255, 255))
    top = ImageFunctions.is_range_dark(img, (0, 0, 600, 100))
    bottom = ImageFunctions.is_range_dark(img, (0, 300, 600, 400))
    upper = ImageFunctions.is_range_dark(img, (0, 50, 600, 300))
    lower = ImageFunctions.is_range_dark(img, (0, 150, 600, 400))

    assert top is False
    assert bottom is True
    assert upper is False
    assert lower is True


def test_draw_icons():
    here = os.path.dirname(__file__)
    path = Path(here)
    parent = path.parent.absolute()
    func = ImageFunctions()
    img = Image.new(mode="RGBA", size=(600, 400), color="black")
    draw = ImageDraw.Draw(img, ImageConst.DRAW_MODE.value)

    draw.rectangle((0, 0, 600, 200), fill=(255, 255, 255))
    icons = []
    for icon in IconFileConst:
        icons.append(icon.value)

    icons.sort(key=lambda item: item[1])

    img = func.draw_icons(img, icons, icon_path=os.path.join(parent, ConfigConst.ICON_PATH.value),
                          icon_location=IconConst.LOC_TOP_RIGHT.value, icon_color="auto", icon_opacity=255)
    img = func.draw_icons(img, icons, icon_path=os.path.join(parent, ConfigConst.ICON_PATH.value),
                          icon_location=IconConst.LOC_BOTTOM_LEFT.value, icon_color="auto")
    img = func.draw_icons(img, icons, icon_path=os.path.join(parent, ConfigConst.ICON_PATH.value),
                          icon_location=IconConst.LOC_BOTTOM_RIGHT.value, icon_color="#FF0000")

    # Check image is not all black
    extrema = img.convert("L").getextrema()
    # Check appropriate pixel is white
    white_pixel = img.getpixel((20, 386))
    black_pixel = img.getpixel((580, 16))
    red_pixel = img.getpixel((585, 387))

    unexpected_extrema = (0, 0)
    expected_white_pixel = (150, 150, 150, 193)
    expected_black_pixel = (0, 0, 0, 255)
    expected_red_pixel = (150, 0, 0, 193)

    assert extrema != unexpected_extrema
    assert white_pixel == expected_white_pixel
    assert black_pixel == expected_black_pixel
    assert red_pixel == expected_red_pixel
