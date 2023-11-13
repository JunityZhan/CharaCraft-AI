from chara_craft import CharaCraft
import concurrent.futures
import gradio as gr
import re
from openai import OpenAI
from langdetect import detect
import time
import json

client = OpenAI()
characraft = CharaCraft()
args = {}
assistant_id = ''
thread_id = ''

with open('CharaCraft/prompt/vision_prompt.txt', 'r', encoding='utf8') as f:
    vision_prompt = f.read()
with open('CharaCraft/prompt/text_prompt.txt', 'r', encoding='utf8') as f:
    text_prompt = f.read()


def getRolePrompt(attributes):
    with open('CharaCraft/prompt/character_card.txt', 'r', encoding='utf8') as f:
        template = f.read()
    attributes.update({
        "me": args['me'],
    })
    prompt = template.format_map(attributes)

    return prompt


def safe_filename(filename):
    """Return a safe version of the filename by replacing non-alphanumeric characters."""
    disallowed_characters = '<>:"/\\|?*\0'
    return re.sub('[{}]'.format(re.escape(disallowed_characters)), '_', filename)


def crawl(plot_urls, plot_depths, character_urls, character_depths, dynamic):
    plot_urls = plot_urls.split('\n')
    plot_depths = [int(depth) for depth in plot_depths.split('\n')]
    character_urls = character_urls.split('\n')
    character_depths = [int(depth) for depth in character_depths.split('\n')]
    args.update({
        "plot_urls": plot_urls,
        "plot_depths": plot_depths,
        "character_urls": character_urls,
        "character_depths": character_depths,
        "dynamic": dynamic,
        "urls": plot_urls + character_urls,
        "depths": plot_depths + character_depths,
    })
    print(args)
    characraft.update(**args)
    characraft.spider("run")
    plot_files = gr.Textbox(label="Plot Files",
                            value='\n'.join(safe_filename(url.split('/')[-1]) for url in plot_urls), lines=2,
                            interactive=True)
    character_files = gr.Textbox(label="Character Files",
                                 value='\n'.join(safe_filename(url.split('/')[-1]) for url in character_urls), lines=2,
                                 interactive=True)
    return plot_files, character_files


def create_pair_dialogues(name, me):
    with open(f'CharaCraft/text/{name}/dialogues.txt', 'r', encoding='utf8') as f:
        dialogues = f.read()
    dialogues = dialogues.split('\n')
    result = []
    for dialogue in dialogues:
        if me in dialogue or name in dialogue:
            result.append(dialogue)
    with open(f'CharaCraft/text/{name}/pair_dialogues.txt', 'w', encoding='utf8') as f:
        f.write('\n'.join(result))


def ask_text_prompt(name, me):
    text_function = {
        "name": "getRolePrompt",
        "description": "Get the prompt of specific role by attributes",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of this character."},
                "gender": {"type": "string", "description": "The gender of this character."},
                "species": {"type": "string", "description": "The species of this character."},
                "age": {"type": "string", "description": "The age of this character."},
                "occupation": {"type": "string", "description": "The occupation of this character"},
                "traits": {"type": "string", "description": "The Personality Traits of this character"},
                "relation": {"type": "string", "description": f"The relation of this character and {me}"},
                "thoughts": {"type": "string", "description": "The inner thoughts of this character"},
                "secret": {"type": "string", "description": "The secret of this character"},
                "like": {"type": "string", "description": "What this character likes"},
                "hate": {"type": "string", "description": "What this character hates"},
                "sexuality": {"type": "string", "description": "The sexuality of this character"},
                "description": {"type": "string", "description": "The description of this character"},
                "styles": {"type": "string", "description": "The speaking styles of this character"},
            },
            "required": ["name", "gender", "species", "age", "occupation", "traits", "relation", "thoughts", "secret",
                         "like", "hate", "sexuality", "description", "styles"]
        }
    }
    files = [client.files.create(
        file=open(f"CharaCraft/text/{name}/pair_dialogues.txt", "rb"),
        purpose='assistants'
    ), client.files.create(
        file=open(f"CharaCraft/text/{name}/keywords.txt", "rb"),
        purpose='assistants'
    )]
    with open(f'CharaCraft/text/{name}/pair_dialogues.txt', 'r', encoding='utf8') as f:
        content = f.read()
    text_assistant = client.beta.assistants.create(
        instructions=text_prompt,
        model="gpt-4-1106-preview",
        tools=[
            {
                "type": "function",
                "function": text_function
            },
            {"type": "retrieval"}],
        file_ids=[files[0].id, files[1].id],
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Here, I provides two text files. One is the information and story of {name}, the other "
                           f"is the words {name} once said. You can use them to make the character card. Remember: "
                           f"Your language should be {detect(content)}."
            },
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=text_assistant.id,
    )
    while True:
        runs = client.beta.threads.runs.list(thread.id)
        latest_run = runs.data[0]
        print("Current text assistant status:", latest_run.status)
        if latest_run.status in "requires_action":
            print("response from text assistant")
            break
        elif latest_run.status in "failed":
            raise Exception("Run failed")
        time.sleep(2)
    return json.loads(latest_run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)


def ask_vision_prompt(name, picture):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture.
Knowledge cutoff: 2023-04
Current date: 2023-11-12

Image input capabilities: Enabled""",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": vision_prompt.replace('{name}', name)},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": picture,
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
    )
    return {"appearance": response.choices[0].message.content}


def extract_prompt(name, me, plot_files, character_files, dialogues, keywords, picture):
    args.update({
        "name": name,
        "me": me,
        "dialogues": dialogues,
        "keywords": keywords.split(','),
        "num_context": 2,
    })
    # Plot Files
    args.update({
        "files": plot_files.split('\n'),
    })
    characraft.update(**args)
    characraft.extract("dialogues")
    # Character Files
    args.update({
        "files": character_files.split('\n'),
    })
    args.update({
        "num_context": 5,
    })
    characraft.update(**args)
    characraft.extract("keywords")
    with open('CharaCraft/prompt/system_prompt.txt', 'r', encoding='utf8') as f:
        system_prompt = f.read()
    system_prompt = system_prompt.replace('{name}', name).replace('{me}', me)

    create_pair_dialogues(name, me)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 并行执行两个函数
        text_future = executor.submit(ask_text_prompt, name, me)
        vision_future = executor.submit(ask_vision_prompt, name, picture)

        # 等待结果
        text_result = text_future.result()
        vision_result = vision_future.result()

        # 合并两个字典
        combined_result = {**text_result, **vision_result}

    character_card = getRolePrompt(combined_result)
    system_prompt = gr.Textbox(label="System Prompt", placeholder="Enter one attribute per line",
                               value=system_prompt, lines=7, interactive=True)
    character_card = gr.Textbox(label="Character Card", placeholder="Enter one attribute per line",
                                value=character_card, lines=7, interactive=True)
    context_files = gr.Textbox(label="Context Files",
                               placeholder="Enter one file name per line. Automatically generated by extract.",
                               value=f'{name}/dialogues.txt', lines=2, interactive=True)
    return system_prompt, character_card, context_files


def respond(message, history):
    client.beta.threads.messages.create(thread_id=thread_id, role='user', content=message)
    client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    while True:
        runs = client.beta.threads.runs.list(thread_id)
        latest_run = runs.data[0]
        if latest_run.status in "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            response = messages.data[0].content[0].text.value
            print(response)
            break
        elif latest_run.status in "failed":
            raise Exception("Run failed")
        time.sleep(2)
    return response

def create_chatbot(system_prompt, character_card, context_files, first_response):
    global assistant_id, thread_id
    context_files = context_files.split('\n')
    files = [client.files.create(
        file=open(f"CharaCraft/text/{file}", "rb"),
        purpose='assistants'
    ) for file in context_files]
    assistant = client.beta.assistants.create(
        instructions=system_prompt,
        model="gpt-4-1106-preview",
        tools=[
            {"type": "retrieval"}],
        file_ids=[file.id for file in files],
    )
    character_card += f'\n Your first response should be "{first_response}"'
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": character_card,
            }
        ]
    )
    assistant_id = assistant.id
    thread_id = thread.id
    client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while True:
        runs = client.beta.threads.runs.list(thread.id)
        latest_run = runs.data[0]
        print("Current assistant status:", latest_run.status)
        if latest_run.status in "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            print(response)
            break
        elif latest_run.status in "failed":
            raise Exception("Run failed")
        time.sleep(2)
    return gr.Chatbot(value=[['Hi', response]])


with gr.Blocks(theme='soft') as demo:
    gr.Markdown("## [CharaCraft](https://github.com/JunityZhan/CharaCraft-AI)", elem_id="title")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                plot_urls = gr.Textbox(label="Plot Urls",
                                       placeholder="Enter one URL per line. This url is used for extracting plot.",
                                       lines=2, interactive=True)
                character_urls = gr.Textbox(label="Character Urls",
                                            placeholder="Enter one URL per line. This url should be the information "
                                                        "of the character. An example is "
                                                        "https://genshin-impact.fandom.com/wiki/Nahida",
                                            lines=2, interactive=True)
            with gr.Column():
                with gr.Row():
                    plot_depths = gr.Textbox(label="Plot Depths", placeholder="Enter one depth per line per url.",
                                             lines=2,
                                             interactive=True)
                    character_depths = gr.Textbox(label="Character Depths", placeholder="Enter one depth per line per "
                                                                                        "url.",
                                                  lines=2, interactive=True)
    dynamic = gr.Checkbox(label="Dynamic")
    with gr.Row():
        crawl_button = gr.Button("Start Crawl", elem_id="crawl_button", variant="secondary")

    with gr.Column():
        with gr.Row():
            with gr.Column():
                plot_files = gr.Textbox(label="Plot Files",
                                        placeholder="Enter one file name per line. Automatically generated by crawl.",
                                        lines=2, interactive=True)
                dialogues = gr.Checkbox(label="Dialogues", value=True)
            character_files = gr.Textbox(label="Character Files",
                                         placeholder="Enter one file name per line. Automatically generated by crawl.",
                                         lines=2, interactive=True)
        with gr.Row():
            me = gr.Textbox(label="Your Name", placeholder="The name should be in the plot, but not your real name.",
                            lines=1, interactive=True)
            name = gr.Textbox(label="Name of the Character", placeholder="The name of the character", lines=1,
                              interactive=True)
        with gr.Row():
            with gr.Column():
                picture = gr.Textbox(label="Picture", placeholder="Enter the url of the picture", lines=1,
                                     interactive=True)

            keywords = gr.Textbox(label="Keywords", placeholder="Enter keywords when extract. Matching two lines "
                                                                "after keywords. Use ',' to split different keywords.",
                                  lines=1, interactive=True)
    with gr.Row():
        extract_button = gr.Button("Generate Prompt", elem_id="extract_button", variant="secondary")

    with gr.Row():
        system_prompt = gr.Textbox(label="System Prompt", placeholder="Enter one attribute per line", lines=7,
                                   interactive=True)
        character_card = gr.Textbox(label="Character Card", placeholder="Enter one attribute per line", lines=7,
                                    interactive=True)
    context_files = gr.Textbox(label="Context Files",
                               placeholder="Enter one file name per line. Automatically generated by extract.",
                               lines=2, interactive=True)
    with gr.Row():
        first_response = gr.Textbox(label="First Response", placeholder="Enter one attribute per line", lines=3,
                                    interactive=True)
    create_button = gr.Button("Create", elem_id="create_button", variant="primary")
    bot = gr.Chatbot(value=[['Chatbot is not loaded', 'Chatbot is not loaded']], render=False)
    chatbot = gr.ChatInterface(fn=respond, chatbot=bot)
    crawl_button.click(fn=crawl,
                       inputs=[plot_urls, plot_depths, character_urls, character_depths, dynamic],
                       outputs=[plot_files, character_files])

    extract_button.click(fn=extract_prompt,
                         inputs=[name, me, plot_files, character_files, dialogues, keywords, picture],
                         outputs=[system_prompt, character_card, context_files])
    create_button.click(fn=create_chatbot,
                        inputs=[system_prompt, character_card, context_files, first_response],
                        outputs=[bot])
demo.launch()
