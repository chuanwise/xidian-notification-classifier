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
import random

import numpy
import sklearn.svm
import text2vec

TEXT_TO_VECTOR_MODEL = text2vec.SentenceModel("shibing624/text2vec-base-chinese")


def to_vector(text: str):
    return TEXT_TO_VECTOR_MODEL.encode(text)


def pure_content_processor(sample: dict):
    return to_vector(sample["content"])


def pure_title_processor(sample: dict):
    return to_vector(sample["title"])


def title_and_content_processor(sample: dict):
    return to_vector(sample["title"] + ", " + sample["content"])


def title_cat_content_processor(sample: dict):
    return numpy.concatenate((to_vector(sample["title"]), to_vector(sample["content"])))




def fit_and_evaluation(marked_notifications: list, input_processor, test_ratio=0.3, c=0.05) -> float:
    model = sklearn.svm.SVC(
        C=c,
        kernel="rbf",
        gamma="scale"
    )

    random.shuffle(marked_notifications)

    test_len = int(len(marked_notifications) * test_ratio)
    test = marked_notifications[:test_len]
    train = marked_notifications[test_len:]

    train_X = [input_processor(element) for element in train]
    train_y = [1 if element["label"] else 0 for element in train]

    test_X = [input_processor(element) for element in test]
    test_y = [1 if element["label"] else 0 for element in test]

    standard_scaler = sklearn.preprocessing.StandardScaler()
    train_X = standard_scaler.fit_transform(train_X)
    test_X = standard_scaler.fit_transform(test_X)

    model.fit(train_X, train_y)

    predictions = model.predict(test_X)
    num_correct = 0
    for i in range(len(test)):
        if predictions[i] == test_y[i]:
            num_correct += 1

    return num_correct / len(test)
