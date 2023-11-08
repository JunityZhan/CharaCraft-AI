from CharaCraft import generate, extract, animate, spider
from chara_craft import CharaCraft

characraft = CharaCraft()

args = {
    "name": "胡桃",
    "num_context": 5,
    "keywords": ['堂主', '称号', '介绍', '故事', '神之眼'],
    "file": ['胡桃'],
    "urls": ['https://wiki.biligame.com/ys/胡桃'],
    "depths": [0],
    "attributes": ["名字", "年龄（一个数字）", "属性（例如：火）", "称号", "性别", "性格（详细）", "职业", "重要故事", "外表"],
}
characraft.update(**args)



characraft.spider("run")
characraft.extract("keywords")

attributes = characraft.generate("prompt")
print(attributes)