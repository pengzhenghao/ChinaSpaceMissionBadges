THIS_YEAR = "2021"

MISSION_NAME = "mission_name"
MISSION_NAME_EN = "mission_name_en"
MISSION_DATE = "mission_date"
MISSION_DATE_FORMATTED = "mission_date_formatted"
LAUNCH_VEHICLE = "launch_vehicle"
PAYLOAD = "payload"
IMAGE_FILE = "image_file"
IMAGE_SOURCE_NAME = "image_source_name"
IMAGE_SOURCE_URL = "image_source_url"
INFO_SOURCE_NAME = "info_source_name"
INFO_SOURCE_URL = "info_source_url"
COMMENT = "comment"

LIST_DATA_KEYS = [IMAGE_FILE, IMAGE_SOURCE_NAME, IMAGE_SOURCE_URL, INFO_SOURCE_NAME, INFO_SOURCE_URL]

SINGLE_PAGE_TEMPLATE = """
<table border="0" width=550px align="center" style="margin-bottom: 100px;">
  <tr>
  IMAGE_ROW
  </tr>
  <tr>
  CAPTION_ROW
  </tr>
</table>


# **MISSION_NAME** MISSION_NAME_EN

INFO
"""

SINGLE_PAGE_IMAGE_ITEM_TEMPLATE = """<td align="center" width=500px><img align="center" width=500px style=" """ \
                                  """box-shadow:2px 2px 5px #333333;" src="image_file" /></td>"""
SINGLE_PAGE_CAPTION_ITEM_TEMPLATE = """<td align="center"><b> mission_name <br>（mission_date_formatted）</b></td>"""

MAIN_PAGE_TEMPLATE = """
# 中国航天任务徽章大赏  China Space Mission Badge Gallery

*收集者：彭正皓（pengzh ie.cuhk.edu.hk）*

*上次更新日期：TODAY*


### 徽章大赏

CONTENT

### 待办事项

* [x] 实现自动化生成主、分页面
* [ ] 添加2021年徽章
* [ ] 完善社区提交工作流

...

"""

MAIN_PAGE_BLOCK_TEMPLATE = """
<details OPEN_FLAG> 
<summary>YEAR</summary> 
<table border="0" width=WIDTH align="center" style="margin-bottom: 100px;">
TABLE_CONTENT
</table>
</details>
"""

MAIN_PAGE_BLOCK_ROW_TEMPLATE = """<tr>IMAGE_ROW</tr><tr>CAPTION_ROW</tr>"""

MAIN_PAGE_IMAGE_ITEM_TEMPLATE = """<td align="center" width=240px><img align="center" width=240px style=" """ \
                                """box-shadow:2px 2px 5px #333333;" src="image_file" /></td>"""
MAIN_PAGE_CAPTION_ITEM_TEMPLATE = """<td align="center"><b><a href="MISSION_LINK">MISSION_NAME</a>""" \
                                  """<br>（mission_date_formatted）</b></td>"""
