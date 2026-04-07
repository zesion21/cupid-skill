#!/usr/bin/env python3
"""QQ聊天记录解析器

支持QQ聊天记录导出格式。

Usage:
    python3 qq_parser.py --file <path> --target <name> --output <output_path>
"""

import argparse
import re
import os
import sys
from pathlib import Path


def parse_qq_log(file_path: str, target_name: str) -> dict:
    """解析QQ聊天记录"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # QQ消息格式：2024-01-01 12:00:00 昵称
    # 消息内容
    msg_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([^\n]+)\n([^\n]*(?:\n(?!\d{4}-\d{2}-\d{2})[^\n]*)*)',
        re.MULTILINE
    )

    messages = []
    for match in msg_pattern.finditer(content):
        timestamp, sender, msg_content = match.groups()
        messages.append({
            'timestamp': timestamp.strip(),
            'sender': sender.strip(),
            'content': msg_content.strip()
        })

    return analyze_messages(messages, target_name, content)


def analyze_messages(messages: list, target_name: str, raw_content: str) -> dict:
    target_msgs = [m for m in messages if target_name in m.get('sender', '')]
    user_msgs = [m for m in messages if target_name not in m.get('sender', '')]

    all_target_text = ' '.join([m['content'] for m in target_msgs if m.get('content')])

    return {
        'target_name': target_name,
        'total_messages': len(messages),
        'target_messages': len(target_msgs),
        'user_messages': len(user_msgs),
        'analysis': {
            'avg_message_length': len(all_target_text) / len(target_msgs) if target_msgs else 0,
        },
        'sample_messages': [m['content'] for m in target_msgs[:30] if m.get('content')],
    }


def main():
    parser = argparse.ArgumentParser(description='QQ聊天记录解析器')
    parser.add_argument('--file', required=True, help='输入文件路径')
    parser.add_argument('--target', required=True, help='对方的名字/昵称')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    result = parse_qq_log(args.file, args.target)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# QQ聊天记录分析 — {args.target}\n\n")
        f.write(f"**总消息数**：{result.get('total_messages', 'N/A')}\n")
        f.write(f"**ta的消息数**：{result.get('target_messages', 'N/A')}\n\n")

        if result.get('sample_messages'):
            f.write("## 消息样本\n")
            for i, msg in enumerate(result['sample_messages'], 1):
                if len(msg) > 100:
                    msg = msg[:100] + '...'
                f.write(f"{i}. {msg}\n")

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()