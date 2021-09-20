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
import math
from os.path import join, dirname, abspath

import pandas as pd

from constants import *
from data_structure import Mission

root = abspath(dirname(__file__))


def _generate_test_file():
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
    df.to_csv("test.csv")


def read_dataset(test=False):
    data_path = "dataset.csv" if not test else "test.csv"
    df: pd.DataFrame = pd.read_csv(data_path)
    df["mission_year"] = df["mission_date"].apply(lambda x: str(str(x)[:4]))
    for item in LIST_DATA_KEYS:
        try:
            df.loc[:, item] = df.loc[:, item].apply(eval)
        except:
            print("Error happens at: ", df.loc[:, item])
    mission_list = [Mission(row) for _, row in df.iterrows()]
    return df, mission_list


def generate_single_pages(mission_list):
    single_page_info = []
    for m in mission_list:
        single_page_info.append(m.generate_single_page())
    return single_page_info


def generate_main_page(data, mission_list):
    template = copy.deepcopy(MAIN_PAGE_TEMPLATE)

    year_list = data.mission_year.unique()

    content = "\n"
    for year in year_list:
        block_template = build_block_content(year, mission_list)
        content += block_template
        content += "\n\n"

    template = template.replace("TODAY", datetime.datetime.strftime(datetime.datetime.today(), "%Y年%m月%d日"))
    template = template.replace("CONTENT", content)

    path = join(dirname(root), "README.md")
    with open(path, "w") as f:
        f.write(template)

    return template


def build_block_content(year, mission_list):
    # Filter mission, only keep this year.
    filtered = [m for m in mission_list if m.mission_year == str(year)]
    filtered = sorted(filtered, key=lambda m: m.mission_date, reverse=True)

    block_template = copy.deepcopy(MAIN_PAGE_BLOCK_TEMPLATE)
    block_template = block_template.replace("YEAR", year)
    block_template = block_template.replace("WIDTH", "1000px" if len(filtered) >= 3 else "550px")
    block_template = block_template.replace("OPEN_FLAG", "open" if str(year) == THIS_YEAR else "")

    count = 0

    num_rows = int(math.ceil((len(filtered) + 1) / 3))
    assert num_rows >= 1

    table_content = ""
    for i in range(num_rows - 1):
        row_content = copy.deepcopy(MAIN_PAGE_BLOCK_ROW_TEMPLATE)
        image_row = ""
        caption_row = ""
        for m_index in range(3):
            mission = filtered[m_index + i * 3]
            image_row, caption_row = add_one_mission(image_row, caption_row, mission)
            count += 1
        row_content = row_content.replace("IMAGE_ROW", image_row)
        row_content = row_content.replace("CAPTION_ROW", caption_row)
        table_content += row_content

    num_extra_items = int(len(filtered) % 3)
    row_content = copy.deepcopy(MAIN_PAGE_BLOCK_ROW_TEMPLATE)
    image_row = ""
    caption_row = ""
    for j in range(len(filtered) - num_extra_items, len(filtered)):
        mission = filtered[j]
        image_row, caption_row = add_one_mission(image_row, caption_row, mission)
        count += 1
    row_content = row_content.replace("IMAGE_ROW", image_row)
    row_content = row_content.replace("CAPTION_ROW", caption_row)
    table_content += row_content

    block_template = block_template.replace("TABLE_CONTENT", table_content)

    assert count == len(filtered), (count, len(filtered), num_rows, num_extra_items)

    return block_template


def add_one_mission(image_row, caption_row, mission):
    """Add one cell in the blocks in the main page."""
    image_item = copy.deepcopy(MAIN_PAGE_IMAGE_ITEM_TEMPLATE)
    caption_item = copy.deepcopy(MAIN_PAGE_CAPTION_ITEM_TEMPLATE)
    image_item = image_item.replace("image_file", join("gallery", mission.badges[0].root_path))
    image_row += image_item

    # caption_item = caption_item.replace("MISSION_NAME_EN", mission.mission_name_en)  # This line is first
    caption_item = caption_item.replace("MISSION_NAME", mission.mission_name)
    caption_item = caption_item.replace("mission_date_formatted", mission.mission_date_formatted)
    caption_item = caption_item.replace("MISSION_LINK", join("gallery", mission.folder_path))
    caption_row += caption_item

    return image_row, caption_row


def main(test=False):
    data, mission_list = read_dataset(test=test)
    single_page_info = generate_single_pages(mission_list)
    print("Successfully generated pages for: ", single_page_info)
    generate_main_page(data, mission_list)
    print("Successfully refresh all pages! 璀璨星空，吾心所向。向着我们的日月星辰，前进！")


if __name__ == '__main__':
    main()

    # For testing only!
    # _generate_test_file()
    # main(test=True)
