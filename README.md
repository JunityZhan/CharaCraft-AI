[中文](README_zh.md)


# DeepWisdom-Character-SOP

This project aims to help users create or fine-tune their own role-playing large language models, providing a novel and interactive chat experience.

## Quick Start Guide

Follow these simple steps to quickly set up and run the CharaCraft-AI project.

### 1. Obtain the Project Code

Clone the project to your local environment:

```bash
git clone https://github.com/JunityZhan/CharaCraft-AI.git
cd CharaCraft-AI
```

### 2. Prepare the Environment

Switch to the project directory:

```bash
cd CharaCraft
```

### 3. Data Processing

#### 3.1 Data Crawling

Taking the Chinese data from the game "Genshin Impact" as an example, with the data sourced from [Demon God Quest](https://wiki.biligame.com/ys/魔神任务), execute the following command to crawl the data:

```bash
python spider/run_spider.py --urls https://wiki.biligame.com/ys/魔神任务  --depths 1
```

The crawled data will be saved in JSONL format and stored in the `/CharaCraft/data` directory.

#### 3.2 Data Extraction

Extract the dialogue data for a specific character (e.g., Paimon):

```bash
python extract/extract.py --name 派蒙 --dialogues
```

The extracted text will be saved in the `/CharaCraft/text` directory.

### 4. Start the ChatBot

Start a chat session with Paimon, interacting as the Traveler:

```bash
python animate/animate.py --role_name 派蒙 --name 旅行者
```

After starting, visit `localhost:7860` to chat with Paimon.

---

By following these steps, you should have successfully started the CharaCraft-AI project and be able to interact with the characters in the system. Enjoy your experience!
