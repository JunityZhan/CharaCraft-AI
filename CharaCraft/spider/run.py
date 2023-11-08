import argparse
import subprocess
import os
import sys
from urllib import parse



def main(args):
    """Main function to run the Scrapy spider with given arguments."""

    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 spider_helper.py 的完整路径
    spider_helper_path = os.path.join(current_dir, 'spider_helper.py')

    for url, depth in zip(args.urls, args.depths):
        url = parse.unquote(url)
        print(url)
        # 使用绝对路径调用 subprocess
        subprocess.run([sys.executable, spider_helper_path, url, str(depth), '1' if args.dynamic else '0'])
