#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for pycasso.py

import os.path

from omni_epd import displayfactory
from piblo.constants import PromptModeConst, PropertiesConst, ConfigConst, ProvidersConst, UnitTestConst, IconConst
from piblo.file_operations import FileOperations
from piblo.pycasso import Pycasso
from PIL import Image, PngImagePlugin, ImageDraw


def test_parse_args():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    instance = Pycasso(config_path)
    expected = 0
    assert instance.args.savekeys == expected


def test_load_config():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    instance = Pycasso(config_path=config_path)
    config = instance.load_config(config_path)
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

    Pycasso.display_image_on_epd(img, epd, 0)
    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_load_test_image():
    tup = Pycasso.load_test_image(400, 400)
    pixel = tup[0].getpixel((100, 100))
    expected = (85, 149, 194)
    assert pixel == expected


def test_load_external_image():
    path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value)
    tup = Pycasso.load_external_image(path, 400, 400)
    pixel = tup[0].getpixel((200, 200))
    expected = (158, 142, 138)
    assert pixel == expected


def test_load_historic_image_load_image():
    path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value)
    tup = Pycasso.load_historic_image(path)
    pixel = tup[0].getpixel((200, 200))
    expected = (158, 142, 138)

    assert pixel == expected


def test_load_historic_image_load_metadata():
    path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value)
    tup = Pycasso.load_historic_image(path)
    title = tup[1]
    artist = tup[2]
    expected_title = "A border collie with a phone"
    expected_artist = "Banksy"

    assert title == expected_title
    assert artist == expected_artist


def test_prep_prompt_text():
    here = os.path.dirname(__file__)
    config_path = os.path.join(here, UnitTestConst.PYCASSO_FOLDER.value, UnitTestConst.CONFIG_FILE.value)
    instance = Pycasso(config_path, here)
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
    artist_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                               UnitTestConst.ARTISTS_FILE.value)
    subject_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                                UnitTestConst.SUBJECTS_FILE.value)
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
    prompt_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                               UnitTestConst.PROMPTS_FILE.value)
    prompt, title_text = Pycasso.prep_normal_prompt(prompt_path, preamble, postscript)
    expected_prompt = "PreambleTest PromptPostscript"
    expected_title = "Test Prompt"

    assert prompt == expected_prompt
    assert title_text == expected_title


def test_save_image():
    dir_path = os.path.join(os.path.dirname(__file__), UnitTestConst.TEMP_FOLDER.value)
    save_path = os.path.join(dir_path, PropertiesConst.FILE_PREAMBLE.value + "TestPrompt." +
                             ConfigConst.FILE_IMAGE_FORMAT.value)
    img = Image.new(mode="RGBA", size=(600, 400))
    prompt = "TestPrompt"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(PropertiesConst.PROMPT.value, prompt)

    # Cleanup files before
    if os.path.exists(save_path):
        os.remove(save_path)

    Pycasso.save_image(prompt, img, metadata, dir_path, ConfigConst.FILE_IMAGE_FORMAT.value, save_date=False)

    assert os.path.exists(save_path)

    # Cleanup files after
    if os.path.exists(save_path):
        os.remove(save_path)


def test_get_random_provider_mode():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    instance = Pycasso(config_path)
    provider = instance.get_random_provider_mode()
    expected = [ProvidersConst.EXTERNAL.value, ProvidersConst.HISTORIC.value]
    assert provider in expected


def test_add_text_to_image():
    title_text = "TITLE"
    artist_text = "ARTIST"
    font_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                             UnitTestConst.FONT_FILE.value)
    img = Image.new(mode="RGBA", size=(600, 400))
    draw = ImageDraw.Draw(img, "RGBA")

    Pycasso.add_text_to_image(draw, font_path, img.height, img.width, title_text, artist_text, opacity=255)

    pixel = img.getpixel((10, 350))
    expected = (255, 255, 255, 255)

    assert pixel == expected


def test_add_text_to_image_blank():
    title_text = ""
    artist_text = ""
    font_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                             UnitTestConst.FONT_FILE.value)
    img = Image.new(mode="RGBA", size=(600, 400))
    draw = ImageDraw.Draw(img, "RGBA")

    Pycasso.add_text_to_image(draw, font_path, img.height, img.width, title_text, artist_text, opacity=255)

    pixel = img.getpixel((10, 350))
    expected = (0, 0, 0, 0)

    assert pixel == expected


def test_override_text():
    here = os.path.dirname(__file__)
    output_path = "mock_output.png"
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_RUN.value)
    instance = Pycasso(config_path, file_path=os.path.dirname(__file__))
    instance.config.override_text = True
    instance.config.override_path = os.path.join(os.path.dirname(__file__), UnitTestConst.PYCASSO_FOLDER.value,
                                                 UnitTestConst.ARTISTS_FILE.value)
    instance.run()

    assert os.path.exists(output_path)
    assert instance.title_text == "Test Artist"

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_run_normal():
    here = os.path.dirname(__file__)
    output_path = "mock_output.png"
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_RUN.value)
    instance = Pycasso(config_path, file_path=os.path.dirname(__file__))
    instance.run()

    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_run_external():
    here = os.path.dirname(__file__)
    output_path = "mock_output.png"
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_RUN.value)
    instance = Pycasso(config_path, file_path=os.path.dirname(__file__))
    instance.config.external_amount = 1
    instance.run()

    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_run_generated():
    here = os.path.dirname(__file__)
    output_path = "mock_output.png"
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_RUN.value)
    instance = Pycasso(config_path, file_path=here)
    instance.config.historic_amount = 1
    instance.run()

    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_run_fallback():
    here = os.path.dirname(__file__)
    output_path = "mock_output.png"
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_RUN.value)
    instance = Pycasso(config_path, file_path=here)
    instance.config.external_image_location = "bad folder"
    instance.config.generated_image_location = "bad folder"
    instance.config.historic_amount = 1
    instance.config.external_amount = 1
    instance.config.provider_fallback = True
    instance.config.test_enabled = True
    instance.run()

    assert os.path.exists(output_path)

    # Cleanup files after
    if os.path.exists(output_path):
        os.remove(output_path)


def test_set_rotate_normal():
    width = 467
    height = 212
    new_width, new_height = Pycasso.set_rotate(width, height, 0)
    expected_width = 467
    expected_height = 212
    assert new_width == expected_width
    assert new_height == expected_height


def test_set_rotate_side():
    width = 400
    height = 200
    new_width, new_height = Pycasso.set_rotate(width, height, 90)
    expected_width = 200
    expected_height = 400
    assert new_width == expected_width
    assert new_height == expected_height


def test_major_complete_config():
    here = os.path.dirname(__file__)
    test_folder = UnitTestConst.PYCASSO_FOLDER.value
    config_path = os.path.join(here, test_folder, UnitTestConst.PYCASSO_CONFIG_COMPLETE.value)

    instance = Pycasso(config_path, file_path=os.path.dirname(__file__))
    file = FileOperations(here)
    config_dict = instance.config.read_config()
    # File Settings
    assert instance.config.save_image is False
    assert instance.config.save_date is False
    assert instance.config.external_image_location == file.get_full_path("test_location")
    assert instance.config.generated_image_location == file.get_full_path("test_location")
    assert instance.config.image_format == "jpg"
    assert instance.config.font_file == file.get_full_path("test_location/Font.ttc")
    assert instance.config.subjects_file == file.get_full_path("test_pycasso_content/test_subjects.txt")
    assert instance.config.artists_file == file.get_full_path("test_pycasso_content/test_artists.txt")
    assert instance.config.prompts_file == file.get_full_path("test_pycasso_content/test_prompts.txt")
    assert instance.config.resize_external is False

    # Text Settings
    assert instance.config.add_text is False
    assert instance.config.parse_file_text is True
    assert instance.config.preamble_regex == " .* - test - "
    assert instance.config.artist_regex == "test_artist"
    assert instance.config.remove_text == ["test _ one", "test element two", "test element 3"]
    assert instance.config.parse_random_text is False
    assert instance.config.parse_brackets == ["{}", "()", "[]"]
    assert instance.config.box_to_floor is False
    assert instance.config.box_to_edge is False
    assert instance.config.artist_loc == 50
    assert instance.config.artist_size == 30
    assert instance.config.title_loc == 70
    assert instance.config.title_size == 40
    assert instance.config.padding == 20
    assert instance.config.opacity == 220
    assert instance.config.override_text is True
    assert instance.config.override_path == file.get_full_path("prompts/test.txt")

    # Icon Settings
    assert instance.config.icon_color == "#FABDAB"
    assert instance.config.icon_padding == 20
    assert instance.config.icon_corner == IconConst.LOC_BOTTOM_RIGHT.value
    assert instance.config.icon_size == 30
    assert instance.config.icon_width == 6
    assert instance.config.icon_gap == 2
    assert instance.config.icon_opacity == 190
    assert instance.config.icon_path == file.get_full_path("test_location/test/test")
    assert instance.config.icon_size == 30
    assert instance.config.icon_width == 6
    assert instance.config.icon_opacity == 190
    assert instance.config.show_battery_icon is False
    assert instance.config.show_provider_icon is False
    assert instance.config.show_status_icon is False

    # Prompt Settings
    assert instance.config.prompt_mode == 2
    assert instance.config.prompt_preamble == "test preamble"
    assert instance.config.prompt_connector == "test connector"
    assert instance.config.prompt_postscript == "{test postscript|0:don't display this}"

    # Display Settings
    assert instance.config.display_type == "test_display"
    assert config_dict.get("EPD", "mode") == "bw"
    assert config_dict.get("EPD", "palette_filter") == "[[0, 0, 0], [255, 255, 255], [0, 255, 0], [0, 0, 255], " \
                                                       "[255, 0, 0], [255, 255, 0], [255, 128, 0]]"
    assert config_dict.getint("Display", "rotate") == 180
    assert config_dict.getboolean("Display", "flip_horizontal") is True
    assert config_dict.getboolean("Display", "flip_vertical") is True
    assert config_dict.get("Display", "dither") == "FloydSteinberg"
    assert config_dict.getfloat("Display", "dither_strength") == 1.0
    assert config_dict.getboolean("Display", "dither_serpentine") is False
    assert config_dict.getint("Image Enhancements", "contrast") == 2
    assert config_dict.getint("Image Enhancements", "brightness") == 2
    assert config_dict.getint("Image Enhancements", "sharpness") == 2

    # Provider Settings
    assert instance.config.external_amount == 12
    assert instance.config.historic_amount == 74
    assert instance.config.stability_amount == 23
    assert instance.config.dalle_amount == 56
    assert instance.config.automatic_amount == 39
    assert instance.config.use_keychain is True
    assert instance.config.credential_path == file.get_full_path(".test_creds")
    assert instance.config.test_enabled is False
    assert instance.config.stable_host == "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"
    assert instance.config.automatic_host == "1.1.1.1"
    assert instance.config.automatic_port == 1337
    assert instance.config.provider_fallback is False

    # Logging Settings
    assert instance.config.log_file == "pycasso_test.log"
    assert instance.config.log_level == 50

    # Generation Settings
    assert instance.config.image_rotate == 90
    assert instance.config.infill is True
    assert instance.config.infill_percent == 40

    # PiJuice Settings
    assert instance.config.use_pijuice is True
    assert instance.config.shutdown_on_battery is False
    assert instance.config.shutdown_on_exception is True
    assert instance.config.wait_to_run == 50
    assert instance.config.charge_display == 30

    # Post Settings
    assert instance.config.post_connector == "TEST POST CONNECTOR"
    assert instance.config.post_to_mastodon is True
    assert instance.config.mastodon_app_name == "test_app"
    assert instance.config.mastodon_base_url == "https://aus.social"
    assert instance.config.mastodon_client_cred_path == file.get_full_path("test1.secret")
    assert instance.config.mastodon_user_cred_path == file.get_full_path("test2.secret")

    # Debug Settings
    assert instance.config.test_epd_width == 900
    assert instance.config.test_epd_height == 500
