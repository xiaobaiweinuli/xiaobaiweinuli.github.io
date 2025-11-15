---
title: '文本转JSON'
date: '2024-04-17 19:05:52'
tags: ['格式转换']
categories: ['默认分类']
description: ''
toc: 'True'
---
```python
import json
# 定义文本文件（UTF-8）内容到JSON格式的转换函数
def convert_line_to_json(line):
    parts = line.strip().split('￥')
    if len(parts) == 2:
        taskname, shareurl = parts
        # 根据给定的示例JSON结构填充字段
        task = {
            "savepath": "/资源分享/3月更新",
            "pattern": "$TV",
            "replace": "",
            "taskname": taskname,
            "shareurl": shareurl
        }
        return json.dumps(task, ensure_ascii=False)
    else:
        # 如果行不符合预期格式，则不进行转换
        return None

# 读取文本文件并转换为JSON格式
def text_to_json(text_filename, json_filename):
    try:
        with open(text_filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 转换每一行并保存到JSON文件
        json_data = [convert_line_to_json(line) for line in lines if line.strip() and '￥' in line]

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            for data in json_data:
                if data:  # 确保数据不为None
                    json_file.write(data + '\n')
    except FileNotFoundError as e:
        print(f"Error: {e}")

# 使用示例
text_filename = r'D:\15268\Desktop\your_text_file.txt'  # 使用原始字符串
json_filename = r'D:\15268\Desktop\output.json'         # 使用原始字符串
text_to_json(text_filename, json_filename)
```
**文本格式**
金山文档￥https://kdocs.cn/l/crzS58nUMuN2
