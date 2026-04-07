<div align="center">

# 恋爱军师.skill

> _"所有的爱都值得被看见，所有的犹豫都值得被理解。"_

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

**暗恋时，猜不透那个人的心意**<br>
**暧昧时，迈不出那一步的距离**<br>
**分手后，走不出那故去的回忆**<br>
**相亲后，读不懂那眼神的秘密**<br>

**别怕，把你的故事讲给我听，我们一起找到爱的勇气。**

<br>

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例)

</div>

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/zesion21/cupid-skill .claude/skills/create-cupid

# 或安装到全局（所有项目都能用）
git clone https://github.com/zesion21/cupid-skill ~/.claude/skills/create-cupid
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

- `/create-cupid`
- "帮我创建一个恋爱军师"
- "我想分析一下ta"

### 创建流程

1. **对方视角（3问）**：ta的代号、基本信息、性格画像
2. **用户视角（2问）**：关系状态、当前困惑
3. **原材料导入**：聊天记录、社交媒体（可选）
4. **分析生成**：对方画像 + 用户背景 + 军师框架
5. **倾诉测试**：像军师一样帮你分析并给建议

### 管理命令

| 命令                   | 说明                       |
| ---------------------- | -------------------------- |
| `/list-cupid`          | 列出所有军师               |
| `/{slug}`              | 倾诉模式（倾听+分析+建议） |
| `/{slug}-analyze`      | 仅分析（不给建议）         |
| `/{slug}-advice`       | 仅建议（不分析）           |
| `/delete-cupid {slug}` | 删除                       |

---

## 效果示例

### 创建时

```
用户：帮我创建一个恋爱军师

我：先给ta起个代号吧。

用户：就叫ta小明吧

我：一句话介绍ta？

用户：程序员 北京 28岁

我：ta的性格？

用户：INTJ 摩羯座 高冷 但偶尔会主动找我

我：你们现在的关系状态？

用户：暗恋三个月了 还没表白

我：你现在最困惑什么？

用户：ta到底喜不喜欢我
```

### 倾诉时

```
用户：/xiaoming

小明军师：好的，说说你最近的情况？

用户：昨晚我主动找ta聊天，ta回复挺快的，但聊了十分钟就说要睡了

小明军师：从ta的行为来看：
         1. 回复快 — 说明ta对你的消息是有响应的
         2. 但时间短 — 可能当天确实累了，也可能是习惯早睡

         结合ta的画像（INTJ高冷但偶尔主动），ta的回复态度是积极的。

         建议：可以观察几天，看ta主动找你的频率。
         如果一周内有主动找你，说明ta对你有一定关注度。
```

---

## 支持的场景

- **暗恋推进** — 分析ta的态度信号，建议如何接近
- **暧昧突破** — 分析关系定位，建议如何确认或推进
- **分手处理** — 分析分手原因，建议如何面对或挽回
- **相亲分析** — 分析对方意图，建议如何判断匹配度
- **冷淡应对** — 分析冷淡原因，建议如何调整心态

---

## 安全边界

1. **健康边界** — 不鼓励纠缠、跟踪或侵犯隐私
2. **理性分析** — 不过度脑补，不给虚假希望
3. **用户主权** — 给建议不替决定，你做最终选择
4. **隐私保护** — 所有数据仅本地存储
5. **情感健康** — 如果有不健康执念，会提醒寻求专业帮助

---

## 项目结构

```
cupid-skills/
├── SKILL.md                    # 主技能文件（创建器）
├── README.md                   # 项目说明
├── prompts/
│   ├── intake.md              # 双视角信息录入
│   ├── target_analyzer.md     # 对方行为分析器
│   ├── user_context_builder.md# 用户背景构建器
│   ├── advisor_framework.md   # 军师分析框架
│   ├── listener.md            # 倾听记录模板
│   ├── merger.md              # 增量合并逻辑
│   └── correction_handler.md  # 对话纠正处理器
├── tools/
│   ├── wechat_parser.py       # 微信聊天记录解析
│   ├── qq_parser.py           # QQ聊天记录解析
│   ├── social_parser.py       # 社交媒体内容解析
│   ├── photo_analyzer.py      # 照片EXIF分析
│   ├── behavior_analyzer.py   # 行为模式分析
│   ├── session_logger.py      # 倾听记录管理
│   ├── version_manager.py     # 版本管理/回滚
│   └── skill_writer.py        # Skill文件管理
├── .claude/skills/{slug}/     # 生成的军师（SKILL.md + 所有数据）
└── requirements.txt
```

> **重要**：所有生成的文件都放在 `.claude/skills/{slug}/` 目录下，包括 SKILL.md、对方画像、会话记录等。这样 `/{slug}` 命令才能被 Claude Code 识别。

---

## 致谢

本项目架构灵感来源于：

- **[同事.skill](https://github.com/titanwings/colleague-skill)**（by titanwings）— 首创"把人蒸馏成 AI Skill"的双层架构
- **[暗恋对象.skill](https://github.com/xiaoheizi8/crush-skills)**（by xiaoheizi8）— 将双层架构迁移到亲密关系场景

恋爱军师.skill 在此基础上，将视角从"模拟对方"转向"分析对方+给建议"，更适合情感咨询场景。

本项目遵循 [AgentSkills](https://agentskills.io/) 开放标准，兼容 Claude Code 和 OpenClaw。

---

## 💘 致正在看文档的你

传说中，丘比特并不是随意射出金箭，他只是轻轻拨动弓弦，为那些已经准备好去爱的人，送去一份“刚刚好”的勇气。

而你，就是那个值得被爱箭射中的人。

恋爱军师能帮你分析局面、拆解心结，但真正走到对方面前、说出那句藏在心里很久的话——那个人，只能是你自己。

请相信：你不是不够好，你只是太习惯把自己放在“被选择”的位置。从今天起，试着做一个主动去爱的人吧。

哪怕声音在发抖，哪怕结局不确定。

犹豫一年，不如行动一晚。

错过一次勇敢，远比被拒绝一次更让人遗憾。

愿你在每一次心动里，都不再躲闪；

愿你的喜欢，不再是深夜对话框里的心事，而是阳光下的一句“我其实很喜欢你”。

愿你的爱，被珍视、被回应、被稳稳接住。

愿你的幸福，不必远求，就在你伸手可及的地方。

**有情人终成眷属，而你，也值得拥有那个对的人**
