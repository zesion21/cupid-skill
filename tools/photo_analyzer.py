#!/usr/bin/env python3
"""照片元信息分析器

提取照片的EXIF信息：拍摄时间、地点等。

Usage:
    python3 photo_analyzer.py --dir <photo_dir> --output <output_path>
"""

import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def get_exif_data(image_path: str) -> dict:
    """提取EXIF信息"""
    if not HAS_PIL:
        return {'error': 'PIL未安装，无法提取EXIF信息'}

    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data is None:
            return {'error': '无EXIF信息'}

        result = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            # 处理时间
            if 'Date' in str(tag) or 'Time' in str(tag):
                try:
                    if isinstance(value, str):
                        result[tag] = value
                except:
                    pass

            # 处理GPS信息
            if 'GPS' in str(tag):
                result[tag] = str(value)

        return result

    except Exception as e:
        return {'error': str(e)}


def analyze_photos(directory: str) -> dict:
    """分析目录下所有照片"""
    results = {
        'source': directory,
        'photos': [],
        'total_files': 0,
    }

    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.webp'}

    for root, dirs, files in os.walk(directory):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in image_extensions:
                path = os.path.join(root, f)
                exif = get_exif_data(path)
                results['photos'].append({
                    'path': path,
                    'exif': exif,
                })
                results['total_files'] += 1

    return results


def main():
    parser = argparse.ArgumentParser(description='照片元信息分析器')
    parser.add_argument('--dir', required=True, help='照片目录路径')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"错误：目录不存在 {args.dir}", file=sys.stderr)
        sys.exit(1)

    result = analyze_photos(args.dir)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("# 照片元信息分析\n\n")
        f.write(f"**来源目录**：{args.dir}\n")
        f.write(f"**照片数量**：{result['total_files']}\n\n")

        if not HAS_PIL:
            f.write("**警告**：PIL未安装，无法提取EXIF信息。\n")
            f.write("安装方法：`pip install Pillow`\n\n")

        f.write("## 照片列表\n\n")

        for photo in result['photos']:
            f.write(f"### {Path(photo['path']).name}\n")
            exif = photo.get('exif', {})

            if 'error' in exif:
                f.write(f"- {exif['error']}\n")
            else:
                for key, value in exif.items():
                    f.write(f"- {key}: {value}\n")
            f.write("\n")

        # 时间线分析
        dates = []
        for photo in result['photos']:
            exif = photo.get('exif', {})
            for key, value in exif.items():
                if 'Date' in str(key) or 'Time' in str(key):
                    dates.append(str(value))

        if dates:
            f.write("## 时间线\n\n")
            for d in sorted(set(dates)):
                f.write(f"- {d}\n")

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()