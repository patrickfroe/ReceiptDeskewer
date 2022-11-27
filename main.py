import argparse
import os
from os import walk
import cv2

from image_manipulation import check_readability, rotate_picture, pre_processing, rotation, crop_background


def parse_args():
    parser = argparse.ArgumentParser(
        description="ReceiptDeskewer"
    )

    parser.add_argument(
        "--path",
        type=str,
        help="Optional add path"
    )

    parser.add_argument(
        '--intermediate_results',
        dest='feature',
        action='store_true'
    )
    parser.add_argument(
        '--no-intermediate_results',
        dest='intermediate_results',
        action='store_false'
    )
    parser.set_defaults(
        intermediate_results=True
    )

    return vars(parser.parse_args())


def main(input_folder: str, save_result: bool) -> None:
    filenames = next(walk(input_folder), (None, None, []))[2]

    for file in filenames:
        img = cv2.imread(path + file)
        raw_img = img.copy()

        # execute multiple steps to increase image quality, rotation angle,
        # and finally check if rotation was correct

        # preprocessing to increase image quality
        img = pre_processing(img, file, save_result)
        # rotate image based on edges detected
        img, angle_1 = rotation(img, file, save_result)
        # cop background for finally orientation testing
        img = crop_background(img, file, save_result)
        # check rotated image if readable
        angle_2 = check_readability(img, file, save_result)
        # get final rotation angle
        final_angle = angle_1 + angle_2
        # rotate initial image and save it
        rotate_picture(raw_img, final_angle, file)
        print(f"file: {file} was rotated with an angle of {final_angle}")


if __name__ == '__main__':
    args = parse_args()

    # optional: receive input path as argument
    if not args['path']:
        path = "./input/"
    else:
        path = args['path']

    if not os.path.isdir(path):
        raise ValueError(f"input path {path} is not valid")

    # optional: save intermediate results for debugging purpose
    intermediate_results = args['intermediate_results']

    main(path, intermediate_results)
