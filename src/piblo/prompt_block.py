"""
Defines the base class for prompt generation blocks.
"""

import abc
import requests
import logging
import os
import openai

from piblo.file_operations import FileOperations
from piblo.constants import LLMConst, ProvidersConst
from piblo.provider import DalleProvider


class PromptBlock(abc.ABC):
    """
    Abstract base class for all prompt generation blocks.

    Subclasses must implement the `generate` method, which should return
    a string representing the content block.

    Error handling for external dependencies (e.g., APIs for weather, RSS) 
    should be implemented within the `generate` method of the respective subclasses.
    Consider appropriate fallbacks or raising specific exceptions.
    """

    @abc.abstractmethod
    def generate(self) -> str:
        """
        Generates the text content for this block.

        Returns:
            str: The generated text content, empty string on failure.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
            Exception: Subclasses should handle and potentially raise exceptions
                       related to their specific data fetching or processing logic.
        """
        raise NotImplementedError("Subclasses must implement the generate() method.")

    def __str__(self) -> str:
        """Provides a default string representation, useful for debugging."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Provides a detailed string representation."""
        return f"{self.__class__.__name__}()"


class QuoteBlock(PromptBlock):
    """
    A prompt block that generates text containing a random Zen quote.
    Fetches data from https://zenquotes.io/
    """
    API_URL = "https://zenquotes.io/api/random"
    TIMEOUT = 10  # seconds

    def __init__(self):
        # No specific initialization needed for this block
        pass

    def generate(self) -> str:
        """
        Fetches a random Zen quote and returns it.

        Returns:
            str: The Zen quote string, or an empty string on failure
        """
        try:
            logging.info(f"Fetching random zen quote from {self.API_URL}...")
            response = requests.get(self.API_URL, timeout=self.TIMEOUT)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            if data and isinstance(data, list) and len(data) > 0:
                quote_data = data[0]
                quote = quote_data.get('q')
                author = quote_data.get('a')
                if quote and author:
                    full_quote = f'\"{quote}\" - {author}'
                    logging.info(f"Successfully fetched quote: {full_quote}")
                    return full_quote
                else:
                    logging.error("API response missing quote or author.")
                    return ""
            else:
                logging.error(f"Unexpected API response format from ZenQuotes: {data}")
                return ""

        except requests.exceptions.Timeout:
            logging.error(f"Timeout occurred while fetching Zen quote from {self.API_URL}")
            return ""
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching zen quote: {e}")
            return ""
        except Exception as e:
            # Catch any other unexpected errors during processing
            logging.error(f"An unexpected error occurred processing the ZenQuotes API response: {e}")
            return ""


class FileBlock(PromptBlock):
    """
    A prompt block that generates text containing a random Zen quote.
    Fetches data from https://zenquotes.io/
    """
    API_URL = "https://zenquotes.io/api/random"
    TIMEOUT = 10  # seconds

    def __init__(self):
        # No specific initialization needed for this block
        pass

    def generate(self, path) -> str:
        """
        Fetches a line from a file available at 'path'

        Returns:
            str: A random line from the file, or empty string on failure
        """
        try:
            line = FileOperations.get_random_line(path)
            return line

        except FileNotFoundError as e:
            # Catch any other unexpected errors during processing
            logging.error(f"\"{path}\" not found or does not exist")
            return ""

        except Exception as e:
            # Catch any other unexpected errors during processing
            logging.error(f"An error occurred loading file from {path}")
            return ""

class LLMBlock(PromptBlock):
    """
    A prompt block that uses LLM APIs to enhance image generation prompts.
    Currently supports OpenAI's GPT models.
    """

    def __init__(self, key=None, creds_mode=ProvidersConst.USE_KEYCHAIN,
                 creds_path=ProvidersConst.CREDENTIAL_PATH.value):
        """
        Initialize the LLM block with model configuration.
        """
        logging.info(f"Initializing LLM block")

        self.llm_provider = DalleProvider(key=key, creds_mode=creds_mode, creds_path=creds_path)
        self.model_name = LLMConst.MODEL.value
        self.temperature = LLMConst.TEMPERATURE.value
        self.max_tokens = LLMConst.MAX_TOKENS.value

    def generate(self, prompt: str, system_prompt: str = LLMConst.SYSTEM_PROMPT.value) -> str:
        """
        Enhances an image generation prompt using the configured LLM.

        Args:
            prompt (str): The original image generation prompt to enhance
            system_prompt (str, optional): Custom system prompt to guide the LLM's behavior

        Returns:
            str: The enhanced prompt string, or empty string on failure
        """
        if not prompt:
            logging.error("No prompt provided to enhance")
            return ""   

        try:
            logging.info(f"Enhancing prompt with {self.model_name}...")
            
            response = self.llm_provider.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{prompt}"}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            enhanced_prompt = response.choices[0].message.content.strip()

            # Clean up the response
            if enhanced_prompt.startswith('"') and enhanced_prompt.endswith('"'):
                enhanced_prompt = enhanced_prompt[1:-1]
            if enhanced_prompt.startswith("'") and enhanced_prompt.endswith("'"):
                enhanced_prompt = enhanced_prompt[1:-1]
            enhanced_prompt = enhanced_prompt.replace('"', '')

            if not enhanced_prompt:
                logging.error("LLM returned an empty prompt")
                return prompt  # Return original prompt as fallback
            
            logging.info(f"Successfully enhanced prompt: {enhanced_prompt}")
            return enhanced_prompt

        except openai.APIConnectionError as e:
            logging.error(f"Connection error with OpenAI API: {e}")
            return prompt
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return prompt
        except openai.AuthenticationError as e:
            logging.error(f"OpenAI authentication error: {e}")
            return prompt
        except openai.RateLimitError as e:
            logging.error(f"OpenAI rate limit exceeded: {e}")
            return prompt
        except Exception as e:
            logging.error(f"An unexpected error occurred during prompt enhancement: {e}")
            return prompt
