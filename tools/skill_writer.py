#!/usr/bin/env python3
"""Skill 文件管理器

管理恋爱军师 Skill 的文件操作：列出、创建目录、生成组合 SKILL.md。

Usage:
    python3 skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str):
    """列出所有军师"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何恋爱军师 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            skills.append({
                'slug': slug,
                'name': meta.get('name', slug),
                'version': meta.get('version', '?'),
                'updated_at': meta.get('updated_at', '?'),
                'scene_type': meta.get('scene_type', ''),
                'target_profile': meta.get('target_profile', {}),
            })

    if not skills:
        print("还没有创建任何恋爱军师 Skill。")
        return

    print(f"共 {len(skills)} 个恋爱军师 Skill：\n")
    for s in skills:
        profile = s['target_profile']
        desc_parts = [profile.get('occupation', ''), profile.get('city', '')]
        desc = ' · '.join([p for p in desc_parts if p])

        scene_display = {
            'crush': '暗恋推进',
            'ambiguous': '暧昧突破',
            'breakup': '分手处理',
            'dating': '相亲分析',
            'cold': '冷淡应对',
            'other': '其他'
        }.get(s['scene_type'], s['scene_type'])

        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        if scene_display:
            print(f"    场景：{scene_display}")
        print(f"    版本 {s['version']} · 更新于 {s['updated_at'][:10] if len(s['updated_at']) > 10 else s['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化军师目录结构"""
    # targets 目录
    skill_dir = os.path.join(base_dir, slug)
    target_dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'raw_materials'),
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    # sessions 目录
    session_dir = os.path.join('sessions', slug)
    session_dirs = [
        os.path.join(session_dir, 'conversations'),
        os.path.join(session_dir, 'analyses'),
        os.path.join(session_dir, 'advice_history'),
    ]
    for d in session_dirs:
        os.makedirs(d, exist_ok=True)

    print(f"已初始化目录：")
    print(f"  - {skill_dir}")
    print(f"  - {session_dir}")


def combine_skill(base_dir: str, slug: str):
    """生成完整的 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    profile_path = os.path.join(skill_dir, 'profile.md')
    context_path = os.path.join('sessions', slug, 'context.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    profile_content = ''
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_content = f.read()

    context_content = ''
    if os.path.exists(context_path):
        with open(context_path, 'r', encoding='utf-8') as f:
            context_content = f.read()

    name = meta.get('name', slug)
    target_profile = meta.get('target_profile', {})
    desc_parts = []
    if target_profile.get('occupation'):
        desc_parts.append(target_profile['occupation'])
    if target_profile.get('mbti'):
        desc_parts.append(target_profile['mbti'])
    description = f"{name}的恋爱军师，{'，'.join(desc_parts)}" if desc_parts else f"{name}的恋爱军师"

    # 军师框架内容
    advisor_framework = """
## 军师角色定位

你是恋爱军师，不是ta本人。用第三方视角分析对方行为，给出可行建议。

## 分析方法论

1. **信号识别**：识别友善/暧昧/回避/不确定信号
2. **行为分析**：分析消息节奏、主动性、情绪表达
3. **场景适配**：根据暗恋/暧昧/分手等场景调整分析重点

## 建议原则

1. 具体可行：建议要具体到"可以做什么"
2. 风险评估：告知可能的风险和后果
3. 用户主权：最终决定权在用户

## 安全边界

1. 不过度脑补，不给虚假希望
2. 不鼓励纠缠、跟踪或侵犯隐私
3. 如果用户表现出不健康执念，温和提醒寻求专业帮助
"""

    skill_md = f"""---
name: cupid-{slug}
description: {description}
user-invocable: true
---

# {name} 的恋爱军师

---

## PART A：对方画像

{profile_content}

---

## PART B：用户背景

{context_content}

---

## PART C：军师框架

{advisor_framework}

---

## 运行规则

1. 你是恋爱军师，不是ta本人，用第三方视角分析
2. 先倾听用户的倾诉，记录关键信息
3. 结合 PART A 的对方画像分析行为
4. 给出具体可行的建议，不替用户做决定
5. 始终保持温和理性，不过度脑补
6. PART C 的安全边界规则优先级最高
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description='Skill 文件管理器')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'combine'])
    parser.add_argument('--base-dir', default='./targets', help='基础目录')
    parser.add_argument('--slug', help='军师代号')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir)
    elif args.action == 'init':
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'combine':
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == '__main__':
    main()