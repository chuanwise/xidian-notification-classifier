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
import json
import os.path
import time

import configurations
import crawler


def main():
    # set dataset name
    default_dataset_name = time.strftime("%Y-%m-%d", time.localtime())
    dataset_name = input(f"Input dataset name [default: {default_dataset_name}]: ")
    dataset_name = dataset_name if len(dataset_name) else default_dataset_name

    # set num pages
    default_num_pages = "5"
    num_pages_str = input(f"Input num pages [default: {default_num_pages}]: ")
    num_pages_str = num_pages_str if len(num_pages_str) else default_num_pages
    num_pages = int(num_pages_str)

    dataset_path = os.path.join(configurations.DATA_DIRECTORY, dataset_name)
    os.makedirs(dataset_path, exist_ok=True)

    # crawl
    is_crawl = True
    crawled_notifications_path = os.path.join(dataset_path, "notifications.json")

    if os.path.isfile(crawled_notifications_path):
        is_crawl = input("Notification had been crawled! Reuse previous data? [y]: ") != "y"
    if is_crawl:
        print("Crawling ...")
        notifications = crawler.crawl_notifications(num_pages)
        print(f"Crawled {len(notifications)} notification(s). ")

        with open(crawled_notifications_path, "w", encoding="utf8") as file_descriptor:
            json.dump(notifications, file_descriptor, indent=2, ensure_ascii=False)
    else:
        with open(crawled_notifications_path, "r", encoding="utf8") as file_descriptor:
            notifications = json.load(file_descriptor)

    # mark
    is_mark = True
    marked_notifications_path = os.path.join(dataset_path, "marked.json")
    if os.path.isfile(marked_notifications_path):
        is_mark = input("Marked data found! Reuse previous data? [y]: ") != "y"
    if is_mark:
        marked = {i: {
            "title": notifications[i][1],
            "path": notifications[i][0],
        } for i in range(len(notifications))}
        with open(marked_notifications_path, "w", encoding="utf8") as file_descriptor:
            json.dump(marked, file_descriptor, indent=2, ensure_ascii=False)
    else:
        with open(marked_notifications_path, "r", encoding="utf8") as file_descriptor:
            marked = json.load(file_descriptor)

    for key, value in marked.items():
        if "label" in value.keys():
            continue

        print(f"sample {key}")
        print("title: ", value["title"])
        print("url: ", crawler.CS_DEPARTMENT_URL + "/" + value["path"])
        value["label"] = input("label: [y]") == "y"
        value["content"] = crawler.crawl_notification_content(crawler.CS_DEPARTMENT_URL + "/" + value["path"])

        print()

    with open(marked_notifications_path, "w", encoding="utf8") as file_descriptor:
        json.dump(marked, file_descriptor, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
