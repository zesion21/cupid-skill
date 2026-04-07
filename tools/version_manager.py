#!/usr/bin/env python3
"""版本存档与回滚管理器

Usage:
    python3 version_manager.py --action <backup|rollback|list> --slug <slug> [--version <v>]
"""

import argparse
import os
import sys
import shutil
import json
from datetime import datetime


def get_skill_dir(slug: str) -> str:
    """获取军师目录"""
    return os.path.join('.claude', 'skills', slug)


def backup(slug: str):
    """备份当前版本"""
    skill_dir = get_skill_dir(slug)
    versions_dir = os.path.join(skill_dir, 'versions')
    meta_path = os.path.join(skill_dir, 'meta.json')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    current_version = meta.get('version', 'v0')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{current_version}_{timestamp}"
    backup_dir = os.path.join(versions_dir, backup_name)

    os.makedirs(backup_dir, exist_ok=True)

    # 备份所有关键文件
    files_to_backup = [
        'profile.md',
        'meta.json',
        'SKILL.md',
        os.path.join('sessions', 'context.md')
    ]

    for fname in files_to_backup:
        src = os.path.join(skill_dir, fname)
        if os.path.exists(src):
            dst = os.path.join(backup_dir, os.path.basename(fname))
            shutil.copy2(src, dst)

    print(f"✅ 已备份版本 {backup_name}")
    return backup_name


def rollback(slug: str, version: str):
    """回滚到指定版本"""
    skill_dir = get_skill_dir(slug)
    versions_dir = os.path.join(skill_dir, 'versions')

    target_dir = None
    for vname in os.listdir(versions_dir):
        if vname.startswith(version) or vname == version:
            target_dir = os.path.join(versions_dir, vname)
            break

    if not target_dir or not os.path.isdir(target_dir):
        print(f"错误：找不到版本 {version}", file=sys.stderr)
        list_versions(slug)
        sys.exit(1)

    # 先备份当前版本
    backup(slug)

    # 恢复文件
    files_to_restore = [
        ('profile.md', 'profile.md'),
        ('meta.json', 'meta.json'),
        ('SKILL.md', 'SKILL.md'),
        ('context.md', os.path.join('sessions', 'context.md'))
    ]

    for src_name, dst_name in files_to_restore:
        src = os.path.join(target_dir, src_name)
        dst = os.path.join(skill_dir, dst_name)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    print(f"✅ 已回滚到版本 {version}")


def list_versions(slug: str):
    """列出所有历史版本"""
    versions_dir = os.path.join(get_skill_dir(slug), 'versions')

    if not os.path.isdir(versions_dir):
        print("没有历史版本。")
        return

    versions = sorted(os.listdir(versions_dir), reverse=True)
    if not versions:
        print("没有历史版本。")
        return

    print(f"历史版本（共 {len(versions)} 个）：\n")
    for v in versions:
        print(f"  {v}")


def main():
    parser = argparse.ArgumentParser(description='版本管理器')
    parser.add_argument('--action', required=True, choices=['backup', 'rollback', 'list'])
    parser.add_argument('--slug', required=True, help='军师代号')
    parser.add_argument('--version', help='回滚目标版本')

    args = parser.parse_args()

    if args.action == 'backup':
        backup(args.slug)
    elif args.action == 'rollback':
        if not args.version:
            print("错误：rollback 需要 --version 参数", file=sys.stderr)
            sys.exit(1)
        rollback(args.slug, args.version)
    elif args.action == 'list':
        list_versions(args.slug)


if __name__ == '__main__':
    main()