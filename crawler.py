#  Copyright 2024 Chuanwise.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re

import requests

NOTIFICATION_PATTERN = re.compile("<a href=\"(?P<path>.*?)\" target=\"_blank\">(?P<title>.*?)</a><span class=\"rq\">")

NEXT_PAGE_LINK_PATTERN = re.compile("<a href=\"[^\d]*?(?P<num>\d+?)[^\d]*?\"\s+?class=\"Next\">下页</a>")

CS_DEPARTMENT_NOTIFICATION_URL = "https://cs.xidian.edu.cn/tzgg.htm"

URL_PATTERN = re.compile(r"https?://(?P<host>[^/]+?)(?P<path>/[^?]+)")

CS_DEPARTMENT_URL = f"https://{URL_PATTERN.match(CS_DEPARTMENT_NOTIFICATION_URL).group(1)}"


def _get_decoded_content(url: str) -> str:
    response = requests.get(url)
    if response.status_code // 100 != 2:
        raise IOError(
            f"Status code of getting request of url '{url}' is {response.status_code}! ")

    return response.content.decode()


def crawl_notifications(num_pages: int) -> list[tuple[str, str]]:
    notifications = []
    url = CS_DEPARTMENT_NOTIFICATION_URL
    for i in range(num_pages):
        url = CS_DEPARTMENT_URL + "/tzgg/" + str(_append_notifications_from_single_page(notifications, url)) + ".htm"
    return notifications


def _append_notifications_from_single_page(notifications: list[tuple[str, str]], url: str) -> int:
    response_content = _get_decoded_content(url)
    notifications += NOTIFICATION_PATTERN.findall(response_content)
    return NEXT_PAGE_LINK_PATTERN.findall(response_content)[0]


if __name__ == '__main__':
    notifications = crawl_notifications(2)
    print(notifications)
