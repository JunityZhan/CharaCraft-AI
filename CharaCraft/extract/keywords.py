import argparse
import os
import jsonlines
from langdetect import detect


def find_and_save_dialogues(text, name, num_context):
    lines = text.split('\n')
    found_lines = []
    result = []
    search_term = name

    for i, line in enumerate(lines):
        if search_term in line:
            start = i
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


def main(args):
    keywords = args.keywords
    name = args.name
    num_context = args.num_context
    file_path = './CharaCraft/data/'
    result_folder = f'./CharaCraft/text/{name}/'
    os.makedirs(result_folder, exist_ok=True)


    if args.files:
        file_names = [f'{f}.jsonl' if not f.endswith('.jsonl') else f for f in args.files]
    else:
        file_names = [f for f in os.listdir(file_path) if f.endswith('.jsonl')]

    dialogue_counter = 1
    for name in keywords:
        for file_name in file_names:
            with jsonlines.open(os.path.join(file_path, file_name)) as reader:
                for obj in reader:
                    text = obj['text']
                    dialogues = find_and_save_dialogues(text, name, num_context)
                    for dialogue in dialogues:
                        with open(os.path.join(result_folder, f'{dialogue_counter}.txt'), 'w', encoding='utf-8') as f:
                            f.write(dialogue)
                        dialogue_counter += 1
