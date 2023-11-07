import argparse
import os
import jsonlines
from langdetect import detect

COLON_MAPPING = {
    'zh-cn': '：',  # Simplified Chinese
    'zh-tw': '：',  # Traditional Chinese
    'ja': '：',     # Japanese
    'ko': '：',     # Korean
}


def merge_continuous_dialogues(dialogues, colon='：'):
    # 将输入字符串按换行符分割成对话列表
    dialogues = dialogues.split('\n')

    # 初始化列表存储处理后的对话
    merged_dialogues = []

    # 遍历对话列表
    for dialogue in dialogues:
        # 使用冒号分割字符串，得到角色名和对话内容
        if colon in dialogue:
            name, content = dialogue.split(colon, 1)
            # 如果列表为空或当前角色名与列表中最后一条对话的角色名不同，直接添加
            if not merged_dialogues or f"{name}{colon}" not in merged_dialogues[-1]:
                merged_dialogues.append(dialogue)
            # 如果当前角色名与列表中最后一条对话的角色名相同，合并对话内容
            else:
                merged_dialogues[-1] = f"{merged_dialogues[-1]}{content}"
        else:
            # 如果没有冒号，直接将对话作为一个独立的条目添加到列表中
            merged_dialogues.append(dialogue)

    # 将处理后的对话列表转换为字符串，并在每条对话之间添加换行符
    merged_dialogues_str = '\n'.join(merged_dialogues)
    return merged_dialogues_str
def parse_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description='Extract specific character from data.')
    parser.add_argument('--files', nargs='+',
                        help='File names of target character in data folder. If not provided, all files will be used.')
    parser.add_argument('--name', type=str, required=True,
                        help='Name of target character. You should only provide one character once.')
    parser.add_argument('--dialogues', action='store_true', help='Whether only extract dialogues. Defaults to False.')
    parser.add_argument('--num_context', type=int, default=2,
                        help='Number of context lines to include before and after the target character lines. Defaults to 2.')

    args = parser.parse_args()
    return args


def determine_colon(name):
    try:
        lang = detect(name)
    except:
        return ':'
    return COLON_MAPPING.get(lang, ': ')


def find_and_save_dialogues(text, name, num_context, colon, dialogues):
    lines = text.split('\n')
    found_lines = []
    result = []
    search_term = f"{name}{colon}" if dialogues else name

    for i, line in enumerate(lines):
        if search_term in line:
            start = max(0, i - num_context)
            end = min(len(lines), i + num_context + 1)
            found_lines.append((start, end))
    if found_lines:
        for i, (start, end) in enumerate(found_lines):
            if i == 0:
                continue
            else:
                if start < found_lines[i - 1][1]:
                    found_lines[i] = (found_lines[i - 1][0], end)
                else:
                    result.append('\n'.join(lines[found_lines[i - 1][0]:found_lines[i - 1][1]]))

        result.append('\n'.join(lines[found_lines[-1][0]:found_lines[-1][1]]))
    return result


def main():
    args = parse_arguments()

    name = args.name
    num_context = args.num_context
    file_path = './data/'
    folder_name = name.replace('"', '')
    result_folder = f'./text/{folder_name}/'
    os.makedirs(result_folder, exist_ok=True)

    colon = determine_colon(name)

    if args.files:
        file_names = args.files
    else:
        file_names = [f for f in os.listdir(file_path) if f.endswith('.jsonl')]

    dialogue_counter = 1
    for file_name in file_names:
        with jsonlines.open(os.path.join(file_path, file_name)) as reader:
            for obj in reader:
                text = obj['text']
                dialogues = find_and_save_dialogues(text, name, num_context, colon, args.dialogues)
                for dialogue in dialogues:
                    dialogue = merge_continuous_dialogues(dialogue, colon=colon)
                    with open(os.path.join(result_folder, f'{dialogue_counter}.txt'), 'w', encoding='utf-8') as f:
                        f.write(dialogue)
                    dialogue_counter += 1


if __name__ == '__main__':
    main()
