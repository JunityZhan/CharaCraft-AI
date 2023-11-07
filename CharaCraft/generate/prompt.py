import argparse
import openai
import os
import time


def ask(prompt_text, name):
    while True:
        try:
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "user", "content": prompt_text},
                ],
                temperature=0.1
            )
            break
        except Exception as e:
            print("An error occurred: ", e)
            time.sleep(5)

    response = result['choices'][0]['message']['content']
    print(response)


    os.makedirs(f'text/{name}', exist_ok=True)
    # 命名为a1.txt, a2.txt, a3.txt, ...
    with open(f'text/{name}/answer{len(os.listdir(f"text/{name}")) + 1}.txt', 'w', encoding='utf-8') as file:
        file.write(prompt_text + response)


def generate_prompt(text, name):
    return (
        f"你将要根据文本来回答问题。\n"
        f"以下是文本\n\n===\n\n{text}\n\n===\n\n"
        f"问题如下:\n\n"
        f"文中是否有提到或者能推测出{name}的性格特点？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"文中是否有提到或者能推测出{name}的种族？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"文中是否有提到或者能推测出{name}的外表？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"文中是否有提到或者能推测出{name}的性别？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"文中是否有提到或者能推测出{name}的故事？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"文中是否有提到或者能推测出{name}的职业？如果有，是什么？如果没有，回答“没有”。\n\n"
        f"根据回复，最终总结描述{name}。\n\n"
    )

def main(args):
    if not args.name:
        print('Name of target character is required.')
        return
    name = args.name
    directory_path = os.path.join('text', name)
    text_content = ""

    # 遍历文件夹text/{name}/里的所有txt文件。
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.txt'):
            print(file_name)
            with open(os.path.join(directory_path, file_name), 'r', encoding='utf-8') as file:
                temp = file.read()
                text_content += temp
                if len(text_content) > 3000:
                    prompt = generate_prompt(text_content, name)
                    print(prompt + '\n')
                    ask(prompt, name)
                    text_content = ""

    if text_content:
        prompt = generate_prompt(text_content, name)
        print(prompt + '\n')
        ask(prompt, name)
