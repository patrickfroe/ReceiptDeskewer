import os

import numpy as np
from PIL import Image


def get_or_create_path(path: str) -> None:
    """ Create folder if it does not exist """
    os.makedirs(path, exist_ok=True)


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    """ Convert cv2 image to pil image """
    return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    """ Convert pil image to cv2 image """
    return np.asarray(img)
