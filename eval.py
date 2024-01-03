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

import json

import model

# replace following line to your marked dataset
marked_json_path = "data/2024-01-04/marked.json"

with open(marked_json_path, "r", encoding="utf8") as file_descriptor:
    marked_notifications = json.load(file_descriptor)

len_before_filtering = len(marked_notifications)
marked_notifications = [element for element in marked_notifications.values() if "label" in element.keys()]
len_after_filtering = len(marked_notifications)

if len_before_filtering != len_after_filtering:
    print(f"WARN: {len_before_filtering - len_after_filtering} sample(s) hasn't label(s)! ")

test_ratio = 0.05
test_count = 0

acc_sum = 0
while test_ratio < 1:
    accuracy = model.fit_and_evaluation(marked_notifications, 0.15)
    acc_sum += accuracy

    print(f"test ratio = {test_ratio}, acc = {accuracy}")

    test_ratio += 0.05
    test_count += 1

print(f"mean acc: {acc_sum / test_count}")

