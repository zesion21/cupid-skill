#!/usr/bin/env python3
"""社交媒体内容解析器

解析朋友圈、微博、小红书等社交媒体截图或文本。

Usage:
    python3 social_parser.py --dir <screenshot_dir> --output <output_path>
    python3 social_parser.py --file <text_file> --output <output_path>
"""

import argparse
import os
import sys
from pathlib import Path


def parse_screenshots(directory: str) -> dict:
    """解析截图目录"""
    results = {
        'source': directory,
        'images': [],
        'total_files': 0,
    }

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

    for root, dirs, files in os.walk(directory):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in image_extensions:
                results['images'].append(os.path.join(root, f))
                results['total_files'] += 1

    return results


def parse_text_file(file_path: str) -> dict:
    """解析文本文件"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    return {
        'source': file_path,
        'content': content,
        'length': len(content),
    }


def main():
    parser = argparse.ArgumentParser(description='社交媒体内容解析器')
    parser.add_argument('--dir', help='截图目录路径')
    parser.add_argument('--file', help='文本文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    if not args.dir and not args.file:
        print("错误：需要指定 --dir 或 --file", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("# 社交媒体内容分析\n\n")

        if args.dir:
            result = parse_screenshots(args.dir)
            f.write(f"**来源目录**：{args.dir}\n")
            f.write(f"**截图数量**：{result['total_files']}\n\n")
            f.write("## 截图列表\n")
            for img in result['images']:
                f.write(f"- {img}\n")
            f.write("\n**提示**：请使用 Read 工具读取具体截图内容进行分析。\n")

        if args.file:
            result = parse_text_file(args.file)
            f.write(f"**来源文件**：{args.file}\n")
            f.write(f"**内容长度**：{result['length']} 字\n\n")
            f.write("## 内容\n\n")
            f.write(result['content'])

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()