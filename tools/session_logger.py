#!/usr/bin/env python3
"""倾听会话记录器

管理用户的倾诉会话记录。

Usage:
    python3 session_logger.py --action <list|log|get> --slug <slug> [--content "..."] [--analysis "..."] [--advice "..."]
"""

import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path


def get_session_dir(slug: str) -> str:
    """获取会话目录"""
    return os.path.join('sessions', slug, 'conversations')


def get_context_path(slug: str) -> str:
    """获取用户背景文件路径"""
    return os.path.join('sessions', slug, 'context.md')


def list_sessions(slug: str):
    """列出所有会话"""
    session_dir = get_session_dir(slug)

    if not os.path.isdir(session_dir):
        print(f"还没有任何倾诉会话。")
        return

    sessions = []
    for fname in sorted(os.listdir(session_dir)):
        if fname.endswith('.md'):
            path = os.path.join(session_dir, fname)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # 读取前500字符作为预览
            sessions.append({
                'file': fname,
                'path': path,
                'preview': content[:200]
            })

    if not sessions:
        print(f"还没有任何倾诉会话。")
        return

    print(f"共 {len(sessions)} 个倾诉会话：\n")
    for s in sessions:
        print(f"**{s['file']}**")
        print(f"{s['preview']}...\n")


def log_session(slug: str, content: str, analysis: str = '', advice: str = ''):
    """记录一次倾诉会话"""
    session_dir = get_session_dir(slug)
    os.makedirs(session_dir, exist_ok=True)

    timestamp = datetime.now()
    session_id = timestamp.strftime('%Y%m%d_%H%M%S')
    session_file = os.path.join(session_dir, f'{session_id}.md')

    with open(session_file, 'w', encoding='utf-8') as f:
        f.write(f"# 倾诉会话记录\n\n")
        f.write(f"**时间**：{timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**会话ID**：{session_id}\n\n")

        f.write("## 用户倾诉内容\n\n")
        f.write(f"{content}\n\n")

        if analysis:
            f.write("## 分析结果\n\n")
            f.write(f"{analysis}\n\n")

        if advice:
            f.write("## 建议\n\n")
            f.write(f"{advice}\n\n")

    # 更新会话索引
    update_session_index(slug, session_id, content[:50] if content else '')

    print(f"会话已记录：{session_file}")


def update_session_index(slug: str, session_id: str, summary: str):
    """更新会话索引"""
    index_file = os.path.join(get_session_dir(slug), 'INDEX.md')

    entry = f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {session_id} | {summary} |\n"

    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 在表格最后一行前插入
        if '|----' in content:
            lines = content.split('\n')
            insert_idx = len(lines) - 1
            for i, line in enumerate(lines):
                if line.startswith('|----'):
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, entry.rstrip('\n'))
            content = '\n'.join(lines)
        else:
            content += '\n' + entry
    else:
        content = f"# 会话历史索引\n\n"
        content += f"| 时间 | 会话ID | 摘要 |\n"
        content += f"|------|--------|------|\n"
        content += entry

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)


def get_session(slug: str, session_id: str):
    """获取指定会话"""
    session_file = os.path.join(get_session_dir(slug), f'{session_id}.md')

    if not os.path.exists(session_file):
        print(f"会话不存在：{session_id}")
        return

    with open(session_file, 'r', encoding='utf-8') as f:
        print(f.read())


def update_context(slug: str, updates: dict):
    """更新用户背景"""
    context_file = get_context_path(slug)

    if not os.path.exists(context_file):
        # 创建新的背景文件
        content = "# 用户背景\n\n"
        content += "## 关系时间线\n\n"
        content += "## 核心困惑\n\n"
        content += "## 期望结果\n\n"
        content += "## 已尝试行动\n\n"
        content += "## 主观感受\n\n"
        content += "## 倾诉记录摘要\n\n"

        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"用户背景文件：{context_file}")


def main():
    parser = argparse.ArgumentParser(description='倾听会话记录器')
    parser.add_argument('--action', required=True, choices=['list', 'log', 'get', 'init'])
    parser.add_argument('--slug', required=True, help='军师代号')
    parser.add_argument('--content', help='倾诉内容')
    parser.add_argument('--analysis', help='分析结果')
    parser.add_argument('--advice', help='建议内容')
    parser.add_argument('--session-id', help='会话ID')

    args = parser.parse_args()

    if args.action == 'list':
        list_sessions(args.slug)
    elif args.action == 'log':
        if not args.content:
            print("错误：log 需要 --content 参数", file=sys.stderr)
            sys.exit(1)
        log_session(args.slug, args.content, args.analysis or '', args.advice or '')
    elif args.action == 'get':
        if not args.session_id:
            print("错误：get 需要 --session-id 参数", file=sys.stderr)
            sys.exit(1)
        get_session(args.slug, args.session_id)
    elif args.action == 'init':
        update_context(args.slug, {})


if __name__ == '__main__':
    main()