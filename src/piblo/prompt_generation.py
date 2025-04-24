"""
Defines the base class for prompt generation blocks.
"""

import abc
import requests
import logging

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
            str: The generated text content.

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
    TIMEOUT = 10 # seconds

    def __init__(self):
        # No specific initialization needed for this block
        pass

    def generate(self) -> str:
        """
        Fetches a random Zen quote and returns it.

        Returns:
            str: The Zen quote string, or an error message/fallback.
        """
        try:
            logging.info(f"Fetching random zen quote from {self.API_URL}...")
            response = requests.get(self.API_URL, timeout=self.TIMEOUT)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
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
                    return None
            else:
                logging.error(f"Unexpected API response format from ZenQuotes: {data}")
                return None

        except requests.exceptions.Timeout:
            logging.error(f"Timeout occurred while fetching Zen quote from {self.API_URL}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching zen quote: {e}")
            return None
        except Exception as e:
            # Catch any other unexpected errors during processing
            logging.exception(f"An unexpected error occurred processing the ZenQuotes API response: {e}")
            return None
 