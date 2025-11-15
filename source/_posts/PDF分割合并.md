---
title: 'PDF分割合并'
date: '2024-04-26 20:29:29'
tags: ['python', 'pdf']
categories: ['默认分类']
description: ''
toc: 'True'
---
提取指定页面并合到一起，输出到代码目录下
````python
import os
import time
from PyPDF2 import PdfReader, PdfWriter

def extract_pages(pdf_path, page_numbers):
    # 创建PdfReader对象
    pdf_reader = PdfReader(open(pdf_path, "rb"))

    # 创建PdfWriter对象
    pdf_writer = PdfWriter()

    # 提取并合并指定页面
    try:
        for page_number in page_numbers:
            page = pdf_reader.pages[page_number - 1]  # 页面索引从0开始
            pdf_writer.add_page(page)
    except Exception as e:
        print(f"提取页面时发生错误: {e}")
        raise  # 保留异常，让程序终止

    return pdf_writer

def save_pdf(pdf_writer, output_path, increment=False):
    # 检查文件是否存在并询问用户是否替换或加编号
    while os.path.exists(output_path):
        response = input(f"文件 {output_path} 已存在，是否替换？(y或者回车) 或 输入 'n' 自动添加编号：").lower()
        if response == "y" or response == "":
            break
        elif response == "n":
            increment = True
            break
        else:
            print("无效输入，请重新选择。")

    if increment:
        base_name, ext = os.path.splitext(output_path)
        i = 1
        while os.path.exists(output_path):
            output_path = f"{base_name}_{i}{ext}"
            i += 1

    # 保存PDF文件
    with open(output_path, "wb") as out_file:
        pdf_writer.write(out_file)

def format_page_range_string(page_numbers):
    page_numbers.sort()  # 确保页码有序
    continuous_ranges = []

    current_start = page_numbers[0]
    current_end = page_numbers[0]

    for num in page_numbers[1:]:
        if num == current_end + 1:  # 如果当前页码与前一页面连续
            current_end = num  # 更新当前范围的结束页码
        else:  # 当前页码与前一页面不连续，开始新的范围
            continuous_ranges.append((current_start, current_end))
            current_start = current_end = num

    # 添加最后一个范围
    continuous_ranges.append((current_start, current_end))

    # 将连续范围转换为字符串形式并连接
    formatted_ranges = [f"{start}-{end}" if start != end else str(start) for start, end in continuous_ranges]
    return ",".join(formatted_ranges)

def parse_page_range(page_range_str):
    ranges = []
    for part in page_range_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ranges.extend(range(start, end + 1))
        else:
            ranges.append(int(part))
    return sorted(ranges)

def list_pdf_files(directory):
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(file)
    return pdf_files

def prompt_to_continue():
    print("提取完成，是否继续提取？(回车继续/任意键退出)")
    user_input = input().strip()
    return user_input == ""

def main():
    # 获取用户选择的PDF文件
    directory = input("请输入当前目录路径或输入 'L/回车' 列出当前目录下的PDF文件：")
    if directory.lower() == 'l' or directory.lower() == "":
        pdf_files = list_pdf_files(os.getcwd())
        print("当前目录下的PDF文件：")
        for i, file in enumerate(pdf_files, start=1):
            print(f"{i}. {file}")
        selection = input("请选择一个PDF文件（输入序号）：")
        if not selection.isdigit() or int(selection) < 1 or int(selection) > len(pdf_files):
            print("无效的选择，请输入有效的序号。")
            return
        pdf_path = os.path.join(os.getcwd(), pdf_files[int(selection) - 1])
    else:
        pdf_path = directory
        while not os.path.isfile(pdf_path):
            print("文件不存在，请检查路径是否正确。")
            pdf_path = input("请重新输入当前目录路径或输入 'L' 列出当前目录下的PDF文件：")
            if pdf_path.lower() == 'l':
                pdf_files = list_pdf_files(os.getcwd())
                print("当前目录下的PDF文件：")
                for i, file in enumerate(pdf_files, start=1):
                    print(f"{i}. {file}")
                selection = input("请选择一个PDF文件（输入序号）：")
                if not selection.isdigit() or int(selection) < 1 or int(selection) > len(pdf_files):
                    print("无效的选择，请输入有效的序号。")
                    return
                pdf_path = os.path.join(os.getcwd(), pdf_files[int(selection) - 1])
                break

    # 获取用户选择的打印类型
    print_types = {
        "1": "黑白单面",
        "2": "黑白双面",
        "3": "彩色单面",
        "4": "彩色双面"
    }
    for key, value in print_types.items():
        print(f"{key}. {value}")
    while True:
        print_type = input("请选择打印类型（输入数字）：")
        if print_type in print_types:
            break
        print("无效的打印类型，请输入正确的数字。")

    # 获取用户输入的页面范围
    while True:
        page_range = input("请输入需要提取的页面范围（例如：1,2-5）：")
        try:
            page_numbers = parse_page_range(page_range)
            break
        except Exception as e:
            print(f"输入的页面范围格式错误，请输入例如：1,2-5。错误信息：{e}")

    formatted_page_range = format_page_range_string(page_numbers)

    # 提取指定页面
    pdf_writer = extract_pages(pdf_path, page_numbers)

    # 根据打印类型和页面范围命名输出文件
    output_dir, output_file = os.path.split(pdf_path)
    output_name = f"{os.path.splitext(output_file)[0]}_{print_types[print_type]}_{formatted_page_range}.pdf"
    output_path = os.path.join(output_dir, output_name)

    # 保存PDF文件
    save_pdf(pdf_writer, output_path)

    # 提示用户是否继续
    if prompt_to_continue():
        main()  # 重新调用main函数

    print("等待10秒后自动退出...")
    time.sleep(10)

if __name__ == "__main__":
    main()
````