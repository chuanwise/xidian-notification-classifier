import re

import requests

NOTIFICATION_PATTERN = re.compile("<a href=\"(?P<path>.*?)\" target=\"_blank\">(?P<title>.*?)</a><span class=\"rq\">")

NEXT_PAGE_LINK_PATTERN = re.compile("<a href=\"(?P<path>.*?)\" class=\"Next\">下页</a>")

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
        url = CS_DEPARTMENT_URL + _append_notifications_from_single_page(notifications, url)
    return notifications


def _append_notifications_from_single_page(notifications: list[tuple[str, str]], url: str) -> str:
    response_content = _get_decoded_content(url)
    notifications += NOTIFICATION_PATTERN.findall(response_content)
    return "/" + NEXT_PAGE_LINK_PATTERN.findall(response_content)[0]


if __name__ == '__main__':
    notifications = crawl_notifications(2)
    print(notifications)
