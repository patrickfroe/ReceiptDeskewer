from typing import Tuple

import cv2
import math
import numpy as np
from pytesseract import Output
import pytesseract
import imutils

from PIL import ImageEnhance, Image
from scipy import ndimage
from helper_functions import get_or_create_path, convert_from_image_to_cv2, convert_from_cv2_to_image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def rotation(img: np.ndarray, filename: str, save_result: bool = False) -> Tuple[np.ndarray, float]:
    """ rotate image by detecting edges and angles of detected edges """

    inital_img = img.copy()

    # detect edges within the image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=185, maxLineGap=5)

    # get all angles of the lines
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # get median angle and rotate image based on it
    median_angle = np.median(angles)
    img_rotated = ndimage.rotate(inital_img, median_angle + 90)

    if save_result:
        path = "./after_rotation/"
        get_or_create_path(path)
        cv2.imwrite(path + filename, img_rotated)

    return img_rotated, median_angle + 90


def pre_processing(img: np.ndarray, filename: str, save_result: bool = False) -> np.ndarray:
    """
    improve quality of input images by reducing lowering brightness,
    increasing contrast and making image gray scaled
    """

    pil_img = convert_from_cv2_to_image(img)

    enhancer_color = ImageEnhance.Color(pil_img)
    pil_img = enhancer_color.enhance(0.0)

    enhancer_br = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer_br.enhance(0.7)

    enhancer_co = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer_co.enhance(2.2)

    if save_result:
        path = "./preprocessed_data/"
        get_or_create_path(path)
        pil_img.save(path + filename)

    return convert_from_image_to_cv2(pil_img)


def crop_background(img: np.ndarray, filename: str, save_result: bool = False) -> np.ndarray:
    """
    Cropping background for final readability testing
    """

    # Usage of gaussian blur to remove possible background patterns
    blur = cv2.GaussianBlur(img, (15, 15), 0)
    thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)[1]

    grayscale = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    bbox = cv2.boundingRect(threshold)

    x, y, w, h = bbox
    cropped_img = img[y:y+h, x:x+w]
    if save_result:
        path = "./cropped/"
        get_or_create_path(path)
        cv2.imwrite(path + filename, cropped_img)

    return cropped_img


def check_readability(img: np.ndarray, filename: str, save_result: bool = False) -> float:
    """
    Check if rotated picture is readable. In case image is not readable rotation
    angle is returned
    """

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # get rotation angle if not oriented correctly
    results = pytesseract.image_to_osd(rgb, output_type=Output.DICT, config='--psm 0 -c min_characters_to_try=15')

    # rotate the image to correct the orientation
    rotated = imutils.rotate_bound(img, angle=results["rotate"])

    if save_result:
        path = "./final/"
        get_or_create_path(path)
        cv2.imwrite(path + filename, rotated)

    return results["rotate"]


def rotate_picture(img: np.ndarray, angle: float, filename: str) -> None:
    """
    Rotate and save image with white background
    """
    # convert input to pil image
    pil_image = convert_from_cv2_to_image(img)
    white = (255, 255, 255)
    img = pil_image.rotate(angle, Image.NEAREST, expand=1, fillcolor=white)

    path = "./output/"
    get_or_create_path(path)
    # save image to output folder
    img.save(path + filename)
