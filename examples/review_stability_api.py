#!/usr/bin/python
# -*- coding:utf-8 -*-

# Test whether the API works
import logging
import os

from piblo.provider import StabilityProvider

logging.basicConfig(level=logging.DEBUG)

# Get prompt, API Key and Endpoint

prompt = input("Prompt:\n")
os.environ["STABILITY_KEY"] = input("API key:\n")
os.environ["STABILITY_HOST"] = input("Endpoint:\n")

logging.info("Loading Stability API")
stability_provider = StabilityProvider()
logging.info("Getting Image")
image = stability_provider.get_image_from_string(prompt)
image.save("api_output.png")
