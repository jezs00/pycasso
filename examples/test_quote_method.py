import requests
import datetime
import random
from PIL import Image
import os
import warnings
import traceback
import io
import argparse

# --- API Client Imports ---
try:
    import openai
except ImportError:
    print("Error: openai library not found. Please install it: pip install openai")
    exit()

try:
    from stability_sdk import client as stability_client
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
except ImportError:
    print("Error: stability-sdk library not found. Please install it: pip install stability-sdk")
    exit()

# Suppress specific warnings (optional)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Configuration ---
# API Models (you might want to choose different ones)
OPENAI_MODEL = "gpt-3.5-turbo"

# Find Stability AI engine IDs here: https://platform.stability.ai/docs/features/api-parameters#engine
STABILITY_ENGINE = "stable-diffusion-xl-1024-v1-0" # Example: Use SDXL 1.0
# STABILITY_ENGINE = "stable-diffusion-v1-6" # Alternative: Use SD 1.6

# Dynamic output paths based on mode (set later)
# OUTPUT_IMAGE_PATH = "generated_art.png"
# OUTPUT_EXPLANATION_PATH = "generated_explanation.txt"
# OUTPUT_SOURCE_PATH = "generated_source.txt" # New

IMAGE_WIDTH = 1024 # Desired image width (check Stability AI model compatibility)
IMAGE_HEIGHT = 1024 # Desired image height (check Stability AI model compatibility)

# --- API Key Check ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit()

if not STABILITY_API_KEY:
    print("Error: STABILITY_API_KEY environment variable not set.")
    exit()

# --- Helper Functions ---

def fetch_dad_joke():
    """Fetches a random dad joke from icanhazdadjoke.com."""
    api_url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    print(f"Fetching dad joke from {api_url}...")
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        joke = data.get("joke")
        if joke:
            print(f"Successfully fetched joke: {joke}")
            return joke
        else:
            print("Error: API response did not contain a 'joke' field.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dad joke: {e}")
        return None
    except Exception as e:
        print(f"An error occurred processing the dad joke API response: {e}")
        return None

def fetch_random_zen_quote():
    """Fetches a random quote from zenquotes.io."""
    api_url = "https://zenquotes.io/api/random"
    print(f"Fetching random zen quote from {api_url}...")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Response is a list containing one quote object
        if data and isinstance(data, list) and len(data) > 0:
            quote_data = data[0]
            quote = quote_data.get('q')
            author = quote_data.get('a')
            if quote and author:
                full_quote = f'"{quote}" - {author}'
                print(f"Successfully fetched quote: {full_quote}")
                return full_quote
            else:
                 print("Error: API response missing quote or author.")
                 return None
        else:
            print("Error: Unexpected API response format from ZenQuotes.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching zen quote: {e}")
        return None
    except Exception as e:
        print(f"An error occurred processing the ZenQuotes API response: {e}")
        return None

def generate_creative_prompt_openai(mode, source_content):
    """
    Generates an image prompt using OpenAI based on the mode and source content.
    Returns a tuple: (creative_prompt, source_content) or (None, None) on failure.
    """
    if not source_content:
        print("Error: No source content provided to generate prompt.")
        return (None, None)

    print(f"\nGenerating image prompt with OpenAI ({OPENAI_MODEL}) based on {mode}...")

    if mode == "dadjoke":
        system_prompt = "You are a surrealist artist tasked with visualizing terrible puns and dad jokes."
        user_prompt = f"""
The following dad joke needs to be turned into an artistic image prompt for an AI image generator:
'{source_content}'

Create a short, creative, and visually absurd image prompt (around 15-30 words). Focus on the pun or the ridiculous scenario implied by the joke. Lean into the weirdness. Aim for styles like 'surreal oil painting', 'bizarre illustration', 'photorealistic absurdity', or 'comedic fantasy art'. Do not include any introductory text, just the prompt itself.
"""
        fallback_prompt = "A rubber chicken reading philosophy, photorealistic."

    elif mode == "twistedzen":
        system_prompt = "You are a thoughtful visual artist skilled at interpreting philosophical concepts and translating their essence into compelling prompts for an advanced AI image generator."
        user_prompt = f"""
Consider the following philosophical quote:
'{source_content}'

Your task is to generate a *highly descriptive* and *artistically compelling* image prompt (around 25-50 words) for an AI image generator.

The prompt MUST visually represent the *meaning, essence, or feeling* of the quote. Aim for a thoughtful and evocative interpretation, not a literal depiction unless appropriate.

Instructions for the prompt content:
- **Focus:** Clearly describe a scene, subject, or abstract concept that captures the quote's core idea.
- **Environment:** Include details about the setting or background that enhance the theme.
- **Mood & Atmosphere:** Specify the desired feeling (e.g., serene, contemplative, profound, peaceful, insightful, mysterious).
- **Artistic Style:** MUST include a specific artistic style (e.g., 'luminous oil painting', 'minimalist ink wash', 'symbolic watercolor', 'ethereal digital art', 'style of Hiroshi Yoshida', 'style of Georgia O'Keeffe', 'impressionistic landscape').
- **Quality Descriptors:** Include terms suggesting high quality and detail (e.g., 'highly detailed', 'subtle textures', 'masterpiece quality', 'soft ambient lighting', 'sharp focus', 'exquisite detail').
- **Format:** Output ONLY the prompt itself, with no introductory text or explanation.
"""
        fallback_prompt = "A single beam of light illuminating a still pond in a misty forest, serene watercolor, highly detailed, masterpiece."
    else:
        print(f"Error: Unknown mode '{mode}' for prompt generation.")
        return (None, None)

    creative_prompt = None
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7, # Slightly lower temp for more thoughtful interpretation
            max_tokens=80, # Allow slightly longer prompts
            top_p=1.0,
            frequency_penalty=0.0, # Less penalty needed probably
            presence_penalty=0.0
        )
        creative_prompt = response.choices[0].message.content.strip()

        if creative_prompt.startswith('"') and creative_prompt.endswith('"'):
            creative_prompt = creative_prompt[1:-1]
        if creative_prompt.startswith("'") and creative_prompt.endswith("'"):
             creative_prompt = creative_prompt[1:-1]

        if not creative_prompt:
            print(f"OpenAI API returned an empty prompt for {mode}, using fallback.")
            creative_prompt = fallback_prompt
        else:
            # Simple clean: remove extra quotes if they exist sometimes
            creative_prompt = creative_prompt.replace('"', '')
            print(f"Generated Image Prompt: {creative_prompt}")

    except Exception as e:
        print(f"An error occurred during OpenAI prompt generation: {e}")
        traceback.print_exc()
        creative_prompt = None

    if not creative_prompt:
       print(f"Using fallback prompt for {mode} due to error or empty response.")
       creative_prompt = fallback_prompt

    # Return the generated prompt and the original source content string
    return (creative_prompt, source_content)

def generate_explanation_openai(mode, image_prompt, source_content):
    """Generates a creative explanation for the image based on the mode."""
    print(f"\nGenerating explanation for the {mode} image with OpenAI ({OPENAI_MODEL})...")

    if mode == "dadjoke":
         system_prompt = "You are a slightly unhinged art critic trying to find meaning in art based on dad jokes."
         user_prompt = f"""
An AI generated an image based on the following prompt (which itself came from a dad joke):
'{image_prompt}'

The original dad joke was:
'{source_content}'

Write a short (2-3 paragraphs), humorous, and perhaps slightly absurd explanation or interpretation of the generated image. Pretend you are taking it *very* seriously as art, while acknowledging the ridiculous source material. Use creative and funny language.
"""
    elif mode == "twistedzen":
         system_prompt = "You are a thoughtful art critic interpreting digital art intended to capture philosophical meaning."
         user_prompt = f"""
An AI generated an image based on the following prompt:
'{image_prompt}'

This prompt was created to visually represent the *meaning and essence* of the philosophical quote:
'{source_content}'

Write a short (2-3 paragraphs), creative, and engaging explanation or interpretation of the generated image. Explore how the artwork attempts to capture the quote's message, discussing the mood, style, symbolism, and overall artistic impression. Use vivid and insightful language.
"""
    else:
        print(f"Error: Unknown mode '{mode}' for explanation generation.")
        return "Explanation generation failed due to unknown mode."

    explanation = None
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7, # Keep balanced temp
            max_tokens=250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        explanation = response.choices[0].message.content.strip()

        if not explanation:
             print("OpenAI returned an empty explanation.")
             explanation = f"An explanation could not be generated for this {mode}-based image."
        else:
            print("Generated Explanation snippet:", explanation[:150] + "...")

    except Exception as e:
        print(f"An error occurred during OpenAI explanation generation: {e}")
        traceback.print_exc()

    if not explanation:
         explanation = "An explanation could not be automatically generated due to an error."

    return explanation

def generate_image_stabilityai(prompt):
    """Generates an image using the Stability AI API based on the prompt."""
    print(f"\nGenerating image with Stability AI (Engine: {STABILITY_ENGINE})... (This may take a while)")
    
    try:
        # Initialize Stability API client
        stability_api = stability_client.StabilityInference(
            key=STABILITY_API_KEY,
            verbose=True, # Print status messages
            engine=STABILITY_ENGINE,
        )

        # Generate the image
        answers = stability_api.generate(
            prompt=prompt,
            # seed=random.randint(0, 2**32 - 1), # Optional: for reproducibility
            steps=50, # Default is 50, adjust as needed
            cfg_scale=7.0, # Default is 7.0, adjust as needed
            width=IMAGE_WIDTH, # Must be multiple of 64 for some models
            height=IMAGE_HEIGHT, # Must be multiple of 64 for some models
            samples=1, # Number of images to generate
            # sampler=generation.SAMPLER_K_DPMPP_2M # Optional: Specify sampler
        )

        # Process the response
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Stability AI rejected the request due to safety filters. "
                        "Try a different prompt.")
                    return None
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    print("Image generated successfully by Stability AI.")
                    return img # Return the first image generated

        print("Error: No image artifact received from Stability AI.")
        return None

    except Exception as e:
        print(f"An error occurred during Stability AI image generation: {e}")
        traceback.print_exc()
        return None

def save_image(image, path):
    """Saves the generated image to the specified path."""
    if image:
        try:
            image.save(path)
            print(f"Image saved to: {os.path.abspath(path)}")
            # No longer relevant: print("\nHistorical event data provided by: https://today.zenquotes.io/")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    else:
        print("Save failed: No valid image provided.")
        return False

def save_explanation(explanation, path):
    """Saves the generated explanation text to the specified path."""
    if explanation:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(explanation)
            print(f"Explanation saved to: {os.path.abspath(path)}")
            return True
        except Exception as e:
            print(f"Error saving explanation: {e}")
            return False
    else:
        print("Save failed: No valid explanation provided.")
        return False

def save_source_content(content, path):
    """Saves the original source content (joke or quote) to a text file."""
    if content:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Source content saved to: {os.path.abspath(path)}")
            return True
        except Exception as e:
            print(f"Error saving source content: {e}")
            return False
    else:
        print("Save failed: No source content provided.")
        return False

# --- Argument Parser Setup ---
parser = argparse.ArgumentParser(description="Generate art and explanations based on different modes.")
parser.add_argument(
    "--mode",
    type=str,
    choices=["dadjoke", "twistedzen"],
    required=True,
    help="The mode for generating input: 'dadjoke' or 'twistedzen'."
)
args = parser.parse_args()

# --- Dynamic Path Configuration ---
OUTPUT_IMAGE_PATH = f"{args.mode}_art.png"
OUTPUT_EXPLANATION_PATH = f"{args.mode}_explanation.txt"
OUTPUT_SOURCE_PATH = f"{args.mode}_source.txt" # New path for source

# --- Main Execution ---
if __name__ == "__main__":
    print(f"--- Starting Art Generation Script (Mode: {args.mode}) ---")

    source_data = None
    image_prompt = None
    input_context = None
    final_image = None
    explanation_text = None
    image_generated_and_saved = False
    explanation_generated_and_saved = False
    source_saved = False # New flag

    # 1. Fetch data based on mode
    if args.mode == "dadjoke":
        source_data = fetch_dad_joke()
    elif args.mode == "twistedzen":
        source_data = fetch_random_zen_quote()

    if source_data:
        # 1b. Save source data
        if save_source_content(source_data, OUTPUT_SOURCE_PATH):
            source_saved = True

        # 2. Generate prompt (get prompt and source content)
        prompt_result = generate_creative_prompt_openai(args.mode, source_data)
        if prompt_result:
             image_prompt, input_context = prompt_result # Unpack

        if image_prompt:
            # 3. Generate image
            final_image = generate_image_stabilityai(image_prompt)

            if final_image:
                # 4. Save image
                if save_image(final_image, OUTPUT_IMAGE_PATH):
                   image_generated_and_saved = True

                # 5. Generate explanation
                explanation_text = generate_explanation_openai(args.mode, image_prompt, input_context)

                if explanation_text:
                    # 6. Save explanation
                    if save_explanation(explanation_text, OUTPUT_EXPLANATION_PATH):
                         explanation_generated_and_saved = True

                else: # If explanation generation failed
                    print("Explanation generation failed.")
            else: # If image generation failed
                print("Image generation failed.")
        else: # If prompt generation failed
            print("Prompt generation failed.")
    else: # If fetching source data failed
        print(f"Failed to fetch source data for mode '{args.mode}'. Cannot proceed.")

    print("\n--- Script Finished ---")

    # --- Final Summary ---
    if source_saved: print(f"Source content successfully saved to {OUTPUT_SOURCE_PATH}")
    else: print("Source content fetching or saving was unsuccessful.")

    if image_generated_and_saved: print(f"Image successfully generated and saved to {OUTPUT_IMAGE_PATH}")
    else: print("Image generation or saving was unsuccessful.")

    if explanation_generated_and_saved: print(f"Explanation successfully generated and saved to {OUTPUT_EXPLANATION_PATH}")
    else: print("Explanation generation or saving was unsuccessful.") 