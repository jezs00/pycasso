#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for pycasso.py

import os.path

from omni_epd import displayfactory
from pycasso.constants import PromptModeConst, PropertiesConst, ConfigConst, ProvidersConst
from pycasso.pycasso import Pycasso
from PIL import Image, PngImagePlugin, ImageDraw


def test_parse_args():
    config_path = os.path.join(os.getcwd(), "test_pycasso_content", ".testconfig")
    instance = Pycasso(config_path)
    expected = 0
    assert instance.args.savekeys == expected


def test_load_config():
    config_path = os.path.join(os.getcwd(), "test_pycasso_content", ".testconfig")
    instance = Pycasso(config_path)
    path = os.path.join(os.getcwd(), "test_pycasso_content", ".testconfig")
    config = instance.load_config(path)
    expected = 160
    assert config.opacity == expected


def test_display_image_on_epd():
    output_path = "mock_output.png"

    # Cleanup file before
    if os.path.exists(output_path):
        os.remove(output_path)

    epd = displayfactory.load_display_driver("omni_epd.mock")
    epd.width = 400
    epd.height = 200
    res = (epd.width, epd.height)
    img = Image.new(mode="RGB", size=res)

    Pycasso.display_image_on_epd(img, epd)
    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_load_external_image():
    path = os.path.join(os.getcwd(), "test_pycasso_content")
    tup = Pycasso.load_external_image(path, 400, 400)
    pixel = tup[0].getpixel((200, 200))
    expected = (158, 142, 138)

    assert pixel == expected


def test_load_historic_image_load_image():
    path = os.path.join(os.getcwd(), "test_pycasso_content")
    tup = Pycasso.load_historic_image(path)
    pixel = tup[0].getpixel((200, 200))
    expected = (158, 142, 138)

    assert pixel == expected


def test_load_historic_image_load_metadata():
    path = os.path.join(os.getcwd(), "test_pycasso_content")
    tup = Pycasso.load_historic_image(path)
    title = tup[1]
    artist = tup[2]
    expected_title = "A border collie with a phone"
    expected_artist = "Banksy"

    assert title == expected_title
    assert artist == expected_artist


def test_prep_prompt_text():
    config_path = os.path.join(os.getcwd(), "test_pycasso_content", ".testconfig")
    instance = Pycasso(config_path)
    tup = instance.prep_prompt_text(PromptModeConst.PROMPT.value)
    expected_prompt = "PreambleTest PromptPostscript"
    assert tup[0] == expected_prompt


def test_parse_multiple_brackets():
    text = "Test(5:pass|0:fail|[pass|{pass|20:pass|0:fail}|0:fail])(1:pass|0:fail)"
    result = Pycasso.parse_multiple_brackets(text, ["()", "[]", "{}"])
    expected = "Testpasspass"
    assert result == expected


def test_prep_subject_artist_prompt():
    preamble = "Preamble"
    connector = "Connector"
    postscript = "Postscript"
    artist_path = os.path.join(os.getcwd(), "test_pycasso_content", "artists.txt")
    subject_path = os.path.join(os.getcwd(), "test_pycasso_content", "subjects.txt")
    prompt, artist_text, title_text = Pycasso.prep_subject_artist_prompt(artist_path, subject_path, preamble, connector,
                                                                         postscript)
    expected_prompt = "PreambleTest SubjectConnectorTest ArtistPostscript"
    expected_artist = "Test Artist"
    expected_subject = "Test Subject"
    assert prompt == expected_prompt
    assert artist_text == expected_artist
    assert title_text == expected_subject


def test_prep_normal_prompt():
    preamble = "Preamble"
    postscript = "Postscript"
    prompt_path = os.path.join(os.getcwd(), "test_pycasso_content", "prompts.txt")
    prompt, title_text = Pycasso.prep_normal_prompt(prompt_path, preamble, postscript)
    expected_prompt = "PreambleTest PromptPostscript"
    expected_title = "Test Prompt"

    assert prompt == expected_prompt
    assert title_text == expected_title


def test_save_image():
    dir_path = os.path.join(os.getcwd(), "test_temp")
    save_path = os.path.join(dir_path,
                             PropertiesConst.FILE_PREAMBLE.value + "TestPrompt." + ConfigConst.FILE_IMAGE_FORMAT.value)
    img = Image.new(mode="RGBA", size=(600, 400))
    prompt = "TestPrompt"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(PropertiesConst.PROMPT.value, prompt)

    # Cleanup files before
    if os.path.exists(save_path):
        os.remove(save_path)

    Pycasso.save_image(prompt, img, metadata, dir_path, ConfigConst.FILE_IMAGE_FORMAT.value)

    assert os.path.exists(save_path)

    # Cleanup files after
    if os.path.exists(save_path):
        os.remove(save_path)


def test_get_random_provider_mode():
    config_path = os.path.join(os.getcwd(), "test_pycasso_content", ".testconfig")
    instance = Pycasso(config_path)
    provider = instance.get_random_provider_mode()
    expected = [ProvidersConst.EXTERNAL.value, ProvidersConst.HISTORIC.value]
    assert provider in expected


def test_add_text_to_image():
    title_text = "TITLE"
    artist_text = "ARTIST"
    font_path = os.path.join(os.getcwd(), "test_pycasso_content", "Font.ttc")
    img = Image.new(mode="RGBA", size=(600, 400))
    draw = ImageDraw.Draw(img, "RGBA")

    Pycasso.add_text_to_image(draw, font_path, img.height, img.width, title_text, artist_text, opacity=255)

    pixel = img.getpixel((10, 350))
    expected = (255, 255, 255, 255)

    assert pixel == expected


def test_add_text_to_image_blank():
    title_text = ""
    artist_text = ""
    font_path = os.path.join(os.getcwd(), "test_pycasso_content", "Font.ttc")
    img = Image.new(mode="RGBA", size=(600, 400))
    draw = ImageDraw.Draw(img, "RGBA")

    Pycasso.add_text_to_image(draw, font_path, img.height, img.width, title_text, artist_text, opacity=255)

    pixel = img.getpixel((10, 350))
    expected = (0, 0, 0, 0)

    assert pixel == expected


