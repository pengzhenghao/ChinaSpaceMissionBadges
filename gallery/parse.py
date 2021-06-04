import datetime
import os
from os.path import join, abspath, dirname

import pandas as pd

root = abspath(dirname(__file__))

AUTOFILLED = "autofilled"

IMAGE_FILE = "image_file"
IMAGE_FILE_TO_ROOT = "image_file_to_root"
IMAGE_IDENTIFIER = "image_identifier"
IMAGE_FILE_2 = "image_file_2"
IMAGE_FILE_TO_ROOT_2 = "image_file_to_root_2"
IMAGE_IDENTIFIER_2 = "image_identifier_2"

MISSION_DATE = "mission_date"


def validate_date(date_text):
    try:
        assert isinstance(date_text, str)
        assert len(date_text) == 8
        date = datetime.datetime.strptime(date_text, '%Y%m%d')
    except (ValueError, AssertionError):
        raise ValueError("Incorrect data {}, should be YYYYMMDD.".format(date_text))
    return date


def _generate_test_file():
    df = pd.DataFrame([{
        MISSION_DATE: "20210529",
        "launch_vehicle": "长征七号遥三",
        "launch_vehicle_en": "LM-7",
        "payload": "天舟二号",
        "payload_en": "Tianzhou 2",
        IMAGE_FILE: AUTOFILLED,
        IMAGE_IDENTIFIER: AUTOFILLED,
        IMAGE_FILE_TO_ROOT: AUTOFILLED,
        IMAGE_FILE_2: AUTOFILLED,
        IMAGE_IDENTIFIER_2: AUTOFILLED,
        IMAGE_FILE_TO_ROOT_2: AUTOFILLED,
        "badge_source_name": "China航天",
        "badge_source_url": "https://weibo.com/5616492130/KhKKlaGS2",
        "badge_source_2_name": "百度百科",
        "badge_source_2_url": "https://baike.baidu.com/item/%E5%A4%A9%E8%88%9F%E4%BA%8C%E5%8F%B7/24695456",
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
    for row_count, row in data.iterrows():
        date = validate_date(row[MISSION_DATE])
        if (row == AUTOFILLED).any():
            df.iloc[row_count, IMAGE_IDENTIFIER] = row[MISSION_DATE]
            relative_mission_folder = join("gallery", str(date.year), row[MISSION_DATE])
            images = []
            for file in os.listdir(abspath(relative_mission_folder)):
                if file != "README.md":
                    images.append(file)
            assert len(images) > 0, "No image is found in {} ({})".format(
                relative_mission_folder, abspath(relative_mission_folder)
            )
            assert len(images) <= 2, "We only support maximally 2 images for one mission now!"

    return df


def generate_single_pages(data: pd.DataFrame):
    for row_count, row in data.iterrows():
        date = row.mission_date


def genertae_main_page(data, single_page_info):
    pass


def validate(data, single_page_info, main_page_info):
    pass


if __name__ == '__main__':
    _generate_test_file()
    data = read_dataset()
    single_page_info = generate_single_pages(data)
    main_page_info = genertae_main_page(data, single_page_info)
    validate(data, single_page_info, main_page_info)
    print("Successfully refresh all pages! 璀璨星空，吾心所向。向着我们的日月星辰，前进！")
