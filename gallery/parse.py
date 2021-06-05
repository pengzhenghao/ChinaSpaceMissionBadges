"""
The procedure of this file:

1. Read the data from dataset.csv
2. Check whether all images are there for each item (i.e. mission)
3. Check whether there are left images
4. Fulfill the dataset.csv if some item is unfilled, e.g. the image file path
5. Create single page for each mission
6. Gather the information to the main page

PENG Zhenghao, June 2021.
"""

import copy
import datetime
import os
from os.path import join, abspath, dirname

import pandas as pd

root = abspath(dirname(__file__))

MISSION_NAME = "mission_name"
MISSION_NAME_EN = "mission_name_en"

MISSION_DATE = "mission_date"
MISSION_DATE_FORMATTED = "mission_date_formatted"

LAUNCH_VEHICLE = "launch_vehicle"
PAYLOAD = "payload"

IMAGE_FILE = "image_file"
IMAGE_FILE_2 = "image_file_2"

IMAGE_FILE_TO_ROOT = "image_file_to_root"
IMAGE_FILE_TO_ROOT_2 = "image_file_to_root_2"

IMAGE_IDENTIFIER = "image_identifier"
IMAGE_IDENTIFIER_2 = "image_identifier_2"

IMAGE_SOURCE_NAME = "image_source_name"
IMAGE_SOURCE_NAME_2 = "image_source_name_2"

IMAGE_SOURCE_URL = "image_source_url"
IMAGE_SOURCE_URL_2 = "image_source_url_2"

INFORMATION_SOURCE_NAME = "information_source_name"
INFORMATION_SOURCE_URL = "information_source_url"

NAN = float("nan")

AUTOFILLED_DOMAINS = [
    IMAGE_FILE, IMAGE_IDENTIFIER, IMAGE_FILE_TO_ROOT
]

SINGLE_PAGE_FILLED_DOMAINS = [
    MISSION_NAME_EN,
    MISSION_NAME,
    MISSION_DATE_FORMATTED,
    LAUNCH_VEHICLE,
    PAYLOAD,
    IMAGE_FILE_2,
    IMAGE_FILE,
    IMAGE_SOURCE_URL_2,
    IMAGE_SOURCE_URL,
    IMAGE_SOURCE_NAME_2,
    IMAGE_SOURCE_NAME,
    INFORMATION_SOURCE_NAME,
    INFORMATION_SOURCE_URL
]


def validate_date(date_text):
    try:
        if isinstance(date_text, int):
            date_text = str(date_text)
        assert isinstance(date_text, str)
        assert len(date_text) == 8
        date = datetime.datetime.strptime(date_text, '%Y%m%d')
    except (ValueError, AssertionError):
        raise ValueError("Incorrect data {}, should be YYYYMMDD.".format(date_text))
    return date, date_text


def _generate_test_file():
    df = pd.DataFrame([{

        MISSION_NAME: "天舟二号",
        MISSION_NAME_EN: "Tianzhou 2",
        MISSION_DATE: "20210529",
        LAUNCH_VEHICLE: "长征七号遥三",
        PAYLOAD: "天舟二号",
        IMAGE_SOURCE_NAME: "China航天",
        IMAGE_SOURCE_URL: "https://weibo.com/5616492130/KhKKlaGS2",
        IMAGE_SOURCE_NAME_2: "百度百科",
        IMAGE_SOURCE_URL_2: "https://baike.baidu.com/item/%E5%A4%A9%E8%88%9F%E4%BA%8C%E5%8F%B7/24695456",
        INFORMATION_SOURCE_NAME: "百度百科",
        INFORMATION_SOURCE_URL: "https://baike.baidu.com/item/%E5%A4%A9%E8%88%9F%E4%BA%8C%E5%8F%B7/24695456",

        IMAGE_FILE: NAN,
        IMAGE_IDENTIFIER: NAN,
        IMAGE_FILE_TO_ROOT: NAN,
        IMAGE_FILE_2: NAN,
        IMAGE_IDENTIFIER_2: NAN,
        IMAGE_FILE_TO_ROOT_2: NAN,

    }])
    df.to_csv("dataset.csv")


def collect_all_images():
    file_dict = {}
    for relative_year_folder in os.listdir(root):
        year_folder = join(root, relative_year_folder)
        for relative_mission_folder in os.listdir(year_folder):
            mission_folder = join(root, relative_mission_folder)
            for image_file in os.listdir(mission_folder):
                if image_file != "README.md":  # A real image file
                    image_identifier = image_file.split(".")[0]
                    file_dict[image_identifier] = dict(
                        image_file_path_to_root=join(
                            "gallery", relative_year_folder, relative_mission_folder, image_file
                        ),
                        image_file=image_file,
                        image_identifier=image_identifier
                    )
    return file_dict


def collect_all_pages():
    pass


def read_dataset():
    df = pd.read_csv("dataset.csv")
    for row_count, row in df.iterrows():
        date, date_text = validate_date(row[MISSION_DATE])
        if pd.isna(row[AUTOFILLED_DOMAINS]).any():
            # We need to fulfill some domains if not provided.

            # Find the images
            relative_mission_folder = join(str(date.year), date_text)
            images = []
            for file in os.listdir(abspath(relative_mission_folder)):
                if file != "README.md":
                    images.append(file)
            images = sorted(images)

            assert len(images) > 0, "No image is found in {} ({})".format(
                relative_mission_folder, abspath(relative_mission_folder)
            )
            assert len(images) <= 2, "We only support maximally 2 images for one mission now!"

            # Fill the first image
            assert images[0].split(".")[0] == date_text, "The first image file should be like YYMMDD.png"
            df.loc[row_count, IMAGE_IDENTIFIER] = date_text
            df.loc[row_count, IMAGE_FILE] = images[0]
            df.loc[row_count, IMAGE_FILE_TO_ROOT] = join(relative_mission_folder, images[0])

            # Fill the possible second image
            if len(images) == 2:
                date_text_2 = date_text + "2"
                assert images[1].split(".")[0] == date_text_2, "The first image file should be like YYMMDD2.png"
                df.loc[row_count, IMAGE_IDENTIFIER_2] = date_text_2
                df.loc[row_count, IMAGE_FILE_2] = images[1]
                df.loc[row_count, IMAGE_FILE_TO_ROOT_2] = join(str(date.year), date_text_2, images[1])
    # df.to_csv("dataset_autofilled.csv")  # For backup purpose
    return df


def generate_single_pages(data: pd.DataFrame):
    with open(join(root, "templates", "detail_page_single_image.md"), "r") as f:
        template_text_single_image = f.read()
    with open(join(root, "templates", "detail_page_two_images.md"), "r") as f:
        template_text_two_images = f.read()
    for row_count, row in data.iterrows():
        if pd.isna(row[IMAGE_IDENTIFIER_2]):
            text = copy.deepcopy(template_text_single_image)
        else:
            text = copy.deepcopy(template_text_two_images)
        row = row.to_dict()

        date, _ = validate_date(row[MISSION_DATE])
        row[MISSION_DATE_FORMATTED] = datetime.datetime.strftime(date, "%Y年%m月%d日")
        for key in SINGLE_PAGE_FILLED_DOMAINS:
            text = text.replace(key, row[key])

        with open(join(dirname(row[IMAGE_FILE_TO_ROOT]), "README.md"), "w") as f:
            f.write(text)


def genertae_main_page(data, single_page_info):
    pass


def validate(data, single_page_info, main_page_info):
    pass


def main():
    data = read_dataset()
    single_page_info = generate_single_pages(data)
    main_page_info = genertae_main_page(data, single_page_info)
    validate(data, single_page_info, main_page_info)
    print("Successfully refresh all pages! 璀璨星空，吾心所向。向着我们的日月星辰，前进！")


if __name__ == '__main__':
    # For testing only!
    _generate_test_file()
    main()
