[English](README.md)

# DeepWisdom-Character-SOP

本项目旨在帮助用户创建或微调自定义的角色扮演大语言模型，提供一种新颖且互动的聊天体验。

## 快速开始指南

遵循以下简单步骤，您将能够快速启动并运行CharaCraft-AI项目。

### 1. 获取项目代码

克隆项目到本地环境：

```bash
git clone https://github.com/JunityZhan/CharaCraft-AI.git
cd CharaCraft-AI
```

### 2. 环境准备

切换到项目目录：

```bash
cd CharaCraft
```

### 3. 数据处理

#### 3.1 数据爬取

以《原神》游戏中的中文数据为例，数据来源于[魔神任务](https://wiki.biligame.com/ys/魔神任务)，执行以下命令进行数据爬取：

```bash
python spider/run_spider.py --urls https://wiki.biligame.com/ys/魔神任务  --depths 1
```

爬取的数据将被保存为JSONL格式，存放于`/CharaCraft/data`目录下。

#### 3.2 数据提取

提取特定角色（如：派蒙）的对话数据：

```bash
python extract/extract.py --name 派蒙 --dialogues
```

提取的文本将被保存在`/CharaCraft/text`目录下。

### 4. 启动聊天机器人

启动与派蒙的聊天会话，以旅行者的身份进行互动：

```bash
python animate/animate.py --role_name 派蒙 --name 旅行者
```

启动后，通过访问`localhost:7860`，您可以开始与派蒙进行聊天。

样例对话
```
旅行者: 派蒙是应急食品!


派蒙：完全不对！怎么还不如吉祥物啊！我可是你的最好的伙伴，不是应急食品！
```
---

通过以上步骤，您应已成功启动CharaCraft-AI项目，并能与系统中的角色进行互动。希望您有一个愉快的体验！
