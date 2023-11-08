import argparse
import openai
import os
import time
from openai._client import Client


def ask(prompt_text, client, file, content):
    assistant = client.beta.assistants.create(
        instructions=prompt_text,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id]
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while True:
        runs = client.beta.threads.runs.list(thread.id)
        latest_run = runs.data[0]
        if latest_run.status in "completed":
            break
        elif latest_run.status in "failed":
            raise Exception("Run failed")
        time.sleep(2)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    response = messages.data[0].content[0].text.value
    with open('temp.txt', 'w', encoding='utf-8') as file:
        file.write(response)
    return response


def generate_prompt(name):
    return (
        f"You will generate a json that include information of {name} based on the file.\n"
        f"You should retrieve the specific text to generate the json.\n"
        f"Your response should be as detailed as possible.\n"
    )


def main(args):
    if not args.name:
        print('Name of target character is required.')
        return
    name = args.name
    attributes = args.attributes
    content = "Your json should include the following attributes:\n"
    content += "{\n"
    for attribute in attributes:
        content += f"    {attribute}: \n"
    content += "}\n"
    content += "Your response should be the same language as the language of the attributes above.\n"
    content += "When you found some information is missing, make a guess from the context.\n"
    content += "Your response should be strictly in json format.\n Starting from '{' and ending with '}'.\n"
    directory_path = os.path.join('CharaCraft', 'text', name)
    file_path = os.path.join(directory_path, 'keywords.txt')
    client = Client()
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )
    prompt = generate_prompt(name)
    return ask(prompt, client, file, content)