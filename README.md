# XiDian Notification Classifier

This project is a classifier to find to which notification you should pay attention. 

The average accuracy is above `0.83` based on our published tiny dataset `2023-01-04` with less than 100 samples. We believe that it may be above `0.93` with more data. 

## Eval

Run `eval.py` to fit and eval our classifier. 

```
test ratio = 0.05, acc = 0.8571428571428571
test ratio = 0.1, acc = 0.8571428571428571
test ratio = 0.15000000000000002, acc = 0.7857142857142857
test ratio = 0.2, acc = 0.7857142857142857
test ratio = 0.25, acc = 0.7142857142857143
test ratio = 0.3, acc = 0.8571428571428571
test ratio = 0.35, acc = 0.9285714285714286
test ratio = 0.39999999999999997, acc = 0.9285714285714286
test ratio = 0.44999999999999996, acc = 0.8571428571428571
test ratio = 0.49999999999999994, acc = 0.8571428571428571
test ratio = 0.5499999999999999, acc = 0.7142857142857143
test ratio = 0.6, acc = 0.9285714285714286
test ratio = 0.65, acc = 0.8571428571428571
test ratio = 0.7000000000000001, acc = 0.8571428571428571
test ratio = 0.7500000000000001, acc = 0.9285714285714286
test ratio = 0.8000000000000002, acc = 0.9285714285714286
test ratio = 0.8500000000000002, acc = 0.7857142857142857
test ratio = 0.9000000000000002, acc = 0.8571428571428571
test ratio = 0.9500000000000003, acc = 0.7142857142857143
mean acc: 0.8421052631578949
```

The default dataset is `2024-01-23` set in variable `marked_json_path`. Change it to load our own dataset generated from following part. 

## Mark

To generate your own custom dataset, run `marker.py` to crawl some latest notifications published in [XiDian University CS Department Page](https://cs.xidian.edu.cn/tzgg.htm) and mark them as interested or not interested. 

```
Input dataset name [default: 2024-01-04]:           # press enter to use defualt one directly
Input num pages [default: 5]:                       # press enter to use defualt one directly
Crawling ...
Crawled 131 notification(s). 

sample 0
title:  西电计算机科学与技术学院2024届毕业生用人单位招聘手册
url:  https://cs.xidian.edu.cn/info/1003/15943.htm
label: [y]                                          # press enter to mark it as 'False' (no interested)
                                                    # or input 'y' and press enter to mark it as 'True' (interested)

... (other samples)
```

Crawled and marked data will be storage in `data/${dataset}/marked.json` (default). 

Change variable `marked_json_path` in `eval.py` and run it to use your custom dataset. 

## License

XiDian Notification Classifier is open source under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). 

```text
Copyright 2023 Chuanwise.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Appreciations

1. **Prof. XK Ma**: my teacher in course `Maching Learning`. 
2. [Text to Vector Model](https://huggingface.co/shibing624/text2vec-base-chinese): used to embedding notification content in our project. 
3. [PyCharm](https://www.jetbrains.com/pycharm/): one of the most useful python IDEs. 
