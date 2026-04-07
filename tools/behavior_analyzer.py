#!/usr/bin/env python3
"""行为模式分析器

分析对方的行为模式，生成结构化的行为画像。

Usage:
    python3 behavior_analyzer.py --input <parsed_data> --output <output_path> --target <name>
"""

import argparse
import os
import sys
import json
import re
from datetime import datetime


def analyze_reply_pattern(messages: list) -> dict:
    """分析回复模式"""
    if not messages:
        return {'pattern': 'unknown', 'description': '数据不足'}

    # 简化分析：根据消息数量和分布判断
    total = len(messages)

    return {
        'pattern': 'analyzed',
        'message_count': total,
        'description': f'共{total}条消息'
    }


def analyze_initiative(messages: list, target_name: str) -> dict:
    """分析主动性"""
    target_msgs = [m for m in messages if target_name in m.get('sender', '')]
    user_msgs = [m for m in messages if target_name not in m.get('sender', '')]

    if not user_msgs:
        return {'initiative': 'unknown', 'description': '数据不足'}

    ratio = len(target_msgs) / len(user_msgs) if user_msgs else 0

    if ratio > 1.2:
        level = 'high'
        desc = '对方比你活跃，主动性强'
    elif ratio < 0.8:
        level = 'low'
        desc = '你比对方活跃，对方较被动'
    else:
        level = 'balanced'
        desc = '互动基本平衡'

    return {
        'initiative': level,
        'ratio': round(ratio, 2),
        'description': desc
    }


def analyze_emotion_expression(text: str) -> dict:
    """分析情绪表达"""
    # 高兴/激动
    happy_words = ['哈哈', '嘻嘻', '哈哈', '好开心', '太棒了', '喜欢', '爱']
    happy_count = sum(text.count(w) for w in happy_words)

    # 消极
    negative_words = ['唉', '烦', '累', '无语', '郁闷', '难过']
    negative_count = sum(text.count(w) for w in negative_words)

    # 语气词
    particles = re.findall(r'[哈嗯哦噢嘿唉呜啊呀吧嘛呢吗么]+', text)

    return {
        'happy_expressions': happy_count,
        'negative_expressions': negative_count,
        'particle_usage': len(particles),
        'emotional_tone': 'positive' if happy_count > negative_count else 'neutral' if happy_count == negative_count else 'negative'
    }


def analyze_content_topics(messages: list, target_name: str) -> dict:
    """分析话题偏好"""
    target_text = ' '.join([m.get('content', '') for m in messages if target_name in m.get('sender', '')])

    topics = {
        '日常分享': 0,
        '工作相关': 0,
        '情感话题': 0,
        '娱乐兴趣': 0,
    }

    # 简化的话题识别
    daily_keywords = ['今天', '昨天', '明天', '早上', '晚上', '吃', '睡', '天气']
    work_keywords = ['工作', '公司', '项目', '会议', '加班', '领导']
    emotion_keywords = ['心情', '感觉', '想', '喜欢', '讨厌', '开心', '难过']
    entertainment_keywords = ['电影', '音乐', '游戏', '综艺', '追剧', '旅游']

    for kw in daily_keywords:
        topics['日常分享'] += target_text.count(kw)
    for kw in work_keywords:
        topics['工作相关'] += target_text.count(kw)
    for kw in emotion_keywords:
        topics['情感话题'] += target_text.count(kw)
    for kw in entertainment_keywords:
        topics['娱乐兴趣'] += target_text.count(kw)

    # 找出主要话题
    main_topic = max(topics, key=topics.get) if max(topics.values()) > 0 else '未知'

    return {
        'topics': topics,
        'main_topic': main_topic
    }


def detect_signals(messages: list, target_name: str) -> dict:
    """检测关系信号"""
    signals = {
        'friendly': [],  # 友善信号
        'ambiguous': [],  # 暧昧信号
        'avoidant': [],  # 回避信号
        'uncertain': []  # 不确定信号
    }

    target_msgs = [m for m in messages if target_name in m.get('sender', '')]

    # 简化信号检测
    for msg in target_msgs:
        content = msg.get('content', '').lower()

        # 友善信号
        if any(kw in content for kw in ['关心', '怎么样', '还好吗', '注意']):
            signals['friendly'].append('表达关心')
        if '分享' in content or '给你看' in content:
            signals['friendly'].append('主动分享')

        # 暧昧信号
        if any(kw in content for kw in ['想你', '喜欢', '特别', '只对你']):
            signals['ambiguous'].append('暧昧表达')

        # 回避信号
        if any(kw in content for kw in ['忙', '没空', '再说', '看情况']):
            signals['avoidant'].append('推脱/回避')

    # 去重
    for key in signals:
        signals[key] = list(set(signals[key]))

    return signals


def generate_profile(messages: list, target_name: str) -> dict:
    """生成完整的行为画像"""
    profile = {
        'target_name': target_name,
        'generated_at': datetime.now().isoformat(),
        'reply_pattern': analyze_reply_pattern(messages),
        'initiative': analyze_initiative(messages, target_name),
        'emotion': analyze_emotion_expression(
            ' '.join([m.get('content', '') for m in messages if target_name in m.get('sender', '')])
        ),
        'topics': analyze_content_topics(messages, target_name),
        'signals': detect_signals(messages, target_name),
    }

    # 综合判断
    signals = profile['signals']
    friendly_count = len(signals['friendly'])
    ambiguous_count = len(signals['ambiguous'])
    avoidant_count = len(signals['avoidant'])

    if friendly_count > avoidant_count and ambiguous_count > 0:
        profile['overall_assessment'] = '积极信号偏多，可能有好感'
    elif avoidant_count > friendly_count:
        profile['overall_assessment'] = '回避信号偏多，建议保持距离'
    elif friendly_count > 0:
        profile['overall_assessment'] = '友善信号，但关系定位不明确'
    else:
        profile['overall_assessment'] = '信号不明显，需要更多观察'

    return profile


def main():
    parser = argparse.ArgumentParser(description='行为模式分析器')
    parser.add_argument('--input', help='已解析的消息数据（JSON）')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--target', required=True, help='对方名字')
    parser.add_argument('--text', help='原始文本（如果没有JSON）')

    args = parser.parse_args()

    messages = []

    if args.input and os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            messages = data.get('messages', data if isinstance(data, list) else [])

    if not messages and args.text and os.path.exists(args.text):
        # 从文本文件简单解析
        with open(args.text, 'r', encoding='utf-8') as f:
            content = f.read()
        # 简化：把每行当作一条消息
        for line in content.split('\n'):
            if line.strip():
                messages.append({'sender': args.target, 'content': line})

    profile = generate_profile(messages, args.target)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# 行为模式分析 — {args.target}\n\n")
        f.write(f"**生成时间**：{profile['generated_at']}\n\n")

        f.write("## 回复模式\n")
        f.write(f"- {profile['reply_pattern'].get('description', '数据不足')}\n\n")

        f.write("## 主动性分析\n")
        f.write(f"- **主动性**：{profile['initiative'].get('initiative', 'unknown')}\n")
        f.write(f"- **描述**：{profile['initiative'].get('description', '')}\n\n")

        f.write("## 情绪表达\n")
        f.write(f"- **情绪基调**：{profile['emotion'].get('emotional_tone', 'neutral')}\n\n")

        f.write("## 话题偏好\n")
        f.write(f"- **主要话题**：{profile['topics'].get('main_topic', '未知')}\n")
        topics = profile['topics'].get('topics', {})
        for t, count in topics.items():
            if count > 0:
                f.write(f"  - {t}：{count}次\n")
        f.write("\n")

        f.write("## 关系信号\n")
        for signal_type, items in profile['signals'].items():
            if items:
                f.write(f"- **{signal_type}**：{', '.join(items)}\n")
        f.write("\n")

        f.write("## 综合判断\n")
        f.write(f"{profile['overall_assessment']}\n")

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()