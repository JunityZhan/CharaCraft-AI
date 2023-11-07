import argparse
import os
import glob
import re


def process_content(content):
    # 初始化一个空字符串，用来存储处理后的内容
    processed_content = ''

    # 逐行处理内容
    for line in content.splitlines():
        # 检查这一行是否以"[name="开头
        if line.startswith('[name='):
            # 使用正则表达式提取双引号内的内容以及后面的文本
            match = re.search(r'\[name="([^"]+)"\](.*)', line)
            if match:
                # 提取匹配的部分并加上冒号，同时保留该行其余的内容
                name = match.group(1)
                rest_of_line = match.group(2)
                processed_content += name + '：' + rest_of_line + '\n'
        # 如果不是以"[name="开头，则忽略这一行

    return processed_content


def main(folder_name):
    # 确保文件夹路径是正确的
    folder_path = os.path.join('./text/', folder_name)
    print(f"Processing folder {folder_path}")
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # 遍历文件夹内所有的.txt文件
    for txt_file in glob.glob(os.path.join(folder_path, '*.txt')):
        # 读取文件内容
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
        # 处理文件内容
        processed_content = process_content(content)

        # 将处理后的内容写回文件
        with open(txt_file, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        print(f"Processed {txt_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some text files.')
    parser.add_argument('--name', type=str, help='Name of the folder to process')

    args = parser.parse_args()

    main(args.name)