import copy
import datetime
from numbers import Integral
from os.path import join, dirname

import pandas as pd

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


class YAMLBadge(Badge):
    def __init__(self, data):
        image_file = str(data["file"])
        date = str(data[MISSION_DATE])
        self.root_path = get_path_from_root(date, image_file)
        self.local_path = image_file
        self.source_name = str(data["name"])
        self.source_url = str(data["url"])
        # self.image_count = image_count


class Mission:
    def __init__(self, data: dict):
        # Load data
        assert len(data) == 1
        key = list(data.keys())[0]
        data_row = data[key]

        # Retrieve information
        self.mission_name = data_row[MISSION_NAME]
        self.mission_name_en = data_row[MISSION_NAME_EN]
        self.mission_date = str(key)
        date, _ = validate_date(self.mission_date)
        self.mission_date_formatted = datetime.datetime.strftime(date, "%Y年%m月%d日")
        self.mission_year = str(date.year)
        self.launch_vehicle = str(data_row[LAUNCH_VEHICLE])
        self.launch_vehicle_en = str(data_row[LAUNCH_VEHICLE_EN])
        self.payload = str(data_row[PAYLOAD])
        self.payload_en = str(data_row[PAYLOAD_EN])
        self.comment = data_row[COMMENT] if not pd.isna(data_row[COMMENT]) else None

        # Load images, single image or multiple images.
        images = data_row[IMAGE]
        if isinstance(images, dict):
            images = [images]
        assert isinstance(images, list)
        assert 1 <= len(images) <= 2, "We only support maximally 2 badges for single mission now!"
        badges = []
        for image_info in images:
            image_info[MISSION_DATE] = self.mission_date
            badges.append(YAMLBadge(image_info))
        self.badges = badges
        self.folder_path = dirname(self.badges[0].root_path)

        # Load information sources, single source or multiple sources.
        infos = data_row[INFO]
        if isinstance(infos, dict):
            infos = [infos]
        assert isinstance(infos, list)
        self.infos = infos

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

        message = ""
        message += "* 时间：{} ({})\n".format(self.mission_date_formatted, None)
        message += "* 载具：{} ({})\n".format(self.launch_vehicle, self.launch_vehicle_en)
        message += "* 载荷：{} ()\n".format(self.payload, self.launch_vehicle_en)
        message += "* 来源："
        for b in self.badges:
            message += "[{}]({}) ".format(b.source_name, b.source_url)
        message += "\n"
        message += "* 信息："
        for info in self.infos:
            message += "[{}]({}) ".format(info["name"], info["url"])
        message += "\n"
        if self.comment is not None:
            message += "* 其他："
            message += self.comment
            message += "\n"
        template = template.replace("INFO", message)

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
