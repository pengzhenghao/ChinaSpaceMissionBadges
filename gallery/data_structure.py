import copy
import datetime
from numbers import Integral
from os.path import join, dirname

import pandas as pd
from pandas import Series

from constants import *


def validate_date(date_text):
    try:
        if isinstance(date_text, Integral):
            date_text = str(date_text)
        assert isinstance(date_text, str)
        assert len(date_text) == 8
        date = datetime.datetime.strptime(date_text, '%Y%m%d')
    except (ValueError, AssertionError):
        raise ValueError("Incorrect data {}, should be YYYYMMDD.".format(date_text))
    return date, date_text


def get_path_from_root(date_string, image_file):
    date, date_text = validate_date(date_string)
    relative_mission_folder = join(str(date.year), date_text)
    return join(relative_mission_folder, image_file)


class Badge:
    def __init__(self, date, image_file, image_count, data_row):
        image_file = str(image_file)
        self.root_path = get_path_from_root(date, image_file)
        self.local_path = image_file
        self.source_name = data_row[IMAGE_SOURCE_NAME][image_count]
        self.source_url = data_row[IMAGE_SOURCE_URL][image_count]
        self.image_count = image_count

    def __str__(self):
        return "Badge <{}>".format(self.local_path)


class Mission:
    def __init__(self, data_row: Series):
        self.mission_name = str(data_row[MISSION_NAME])
        self.mission_date = str(data_row[MISSION_DATE])

        date, _ = validate_date(self.mission_date)
        self.mission_date_formatted = datetime.datetime.strftime(date, "%Y年%m月%d日")
        self.mission_year = str(date.year)

        self.mission_name_en = str(data_row[MISSION_NAME_EN])
        self.launch_vehicle = str(data_row[LAUNCH_VEHICLE])
        self.payload = str(data_row[PAYLOAD])

        image_paths = list(data_row[IMAGE_FILE])
        assert 1 <= len(image_paths) <= 2, "We only support maximally 2 badges for single mission now!"

        self.badges = []
        for image_count, image_file in enumerate(image_paths):
            self.badges.append(Badge(self.mission_date, image_file, image_count, data_row))
        self.folder_path = dirname(self.badges[0].root_path)

        self.info_sources = [
            (info_name, info_url) for info_name, info_url in zip(data_row[INFO_SOURCE_NAME], data_row[INFO_SOURCE_URL])
        ]

        self.comment = data_row[COMMENT] if not pd.isna(data_row[COMMENT]) else None

    def generate_single_page(self):
        """Generate the whole markdown for single page of the mission"""
        template = copy.deepcopy(SINGLE_PAGE_TEMPLATE)

        image_row = ""
        for b in self.badges:
            image_item = copy.deepcopy(SINGLE_PAGE_IMAGE_ITEM_TEMPLATE)
            image_item = image_item.replace("image_file", b.local_path)
            image_row += image_item
        template = template.replace("IMAGE_ROW", image_row)

        caption_row = ""
        for b in self.badges:
            caption_item = copy.deepcopy(SINGLE_PAGE_CAPTION_ITEM_TEMPLATE)
            caption_item = caption_item.replace("mission_name", self.mission_name)
            caption_item = caption_item.replace("mission_date_formatted", self.mission_date_formatted)
            caption_row += caption_item
        template = template.replace("CAPTION_ROW", caption_row)

        template = template.replace("MISSION_NAME_EN", self.mission_name_en)  # This should be placed first
        template = template.replace("MISSION_NAME", self.mission_name)

        info = ""
        info += "* 时间：{}\n".format(self.mission_date_formatted)
        info += "* 载具：{}\n".format(self.launch_vehicle)
        info += "* 载荷：{}\n".format(self.payload)
        info += "* 来源："
        for b in self.badges:
            info += "[{}]({}) ".format(b.source_name, b.source_url)
        info += "\n"
        info += "* 信息："
        for i in self.info_sources:
            info += "[{}]({}) ".format(i[0], i[1])
        info += "\n"
        if self.comment is not None:
            info += "* 其他："
            info += self.comment
            info += "\n"
        template = template.replace("INFO", info)

        with open(join(self.folder_path, "README.md"), "w") as f:
            f.write(template)

        return dict(
            path=self.folder_path,
            # text=template,
            mission_name=self.mission_name,
            mission_name_en=self.mission_name_en,
            date=self.mission_date_formatted
        )


if __name__ == '__main__':
    df = pd.DataFrame([{
        MISSION_NAME: "天舟二号",
        MISSION_NAME_EN: "Tianzhou 2",
        MISSION_DATE: "20210529",
        LAUNCH_VEHICLE: "长征七号遥三",
        PAYLOAD: "天舟二号",
        IMAGE_FILE: ["20210529.jpeg", "202105292.png"],
        IMAGE_SOURCE_NAME: ["China航天", "百度百科"],
        IMAGE_SOURCE_URL: [
            "https://weibo.com/5616492130/KhKKlaGS2",
            "https://baike.baidu.com/item/%E5%A4%A9%E8%88%9F%E4%BA%8C%E5%8F%B7/24695456"
        ],
        INFO_SOURCE_NAME: ["百度百科"],
        INFO_SOURCE_URL: ["https://baike.baidu.com/item/%E5%A4%A9%E8%88%9F%E4%BA%8C%E5%8F%B7/24695456"],
    }])
    df.to_excel("dataset.xlsx")
    df = pd.read_excel("dataset.xlsx")
    for item in LIST_DATA_KEYS:
        df.loc[:, item] = df.loc[:, item].apply(eval)
    m = Mission(df.iloc[0])
    text = m.generate_single_page()
