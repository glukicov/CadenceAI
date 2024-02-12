import argparse
import pathlib
import yaml

from typing import List
from loguru import logger
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

config = yaml.safe_load(open("config.yaml"))
VISION_MODEL = config["vision_model"]
VISION_CONTENT = config["vision_content"]
VISION_MAX_OUTPUT_TOKENS = config["vision_max_output_tokens"]
VISION_TEMPERATURE = config["vision_temperature"]
VISION_TOP_K = config["vision_top_k"]
VISION_TOP_P = config["vision_top_p"]
VISION_STREAM = config["vision_stream"]
IMG_PATH = config["img_path"]
IMG_TYPE = config['img_type']


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a vision request to a server.")
    parser.add_argument("--img_path", type=str, default=IMG_PATH,
                        help="Send request to a local server")
    return parser.parse_args()


def get_image(img_path: str = IMG_PATH) -> Part:
    image_bytes = pathlib.Path(img_path).read_bytes()
    part_image = Part.from_data(data=image_bytes, mime_type=IMG_TYPE)
    return part_image


def get_safety_settings():
    return {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }


def generate(input_image, vision_content: str = VISION_CONTENT) -> List[str]:
    model = GenerativeModel(VISION_MODEL)
    responses = model.generate_content(
        contents=[input_image, vision_content],
        generation_config={
            "max_output_tokens": VISION_MAX_OUTPUT_TOKENS,
            "temperature": VISION_TEMPERATURE,
            "top_p": VISION_TOP_P,
            "top_k": VISION_TOP_K
        },
        safety_settings=get_safety_settings(),
        stream=VISION_STREAM,
    )
    full_response = []
    for response in responses:
        full_response.append(response.text)
    return full_response


if __name__ == "__main__":
    args = create_parser()
    image = get_image(img_path=args.img_path)
    api_response = generate(input_image=image)
    logger.info(api_response)
