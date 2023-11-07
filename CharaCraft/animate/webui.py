import sys
import os
import argparse
import gradio as gr

current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from chatharuhi import ChatHaruhi
def main(args):
    prompt, name, me, first_response = args.prompt, args.name, args.me, args.first_response
    db_folder = os.path.join('CharaCraft\\text', name)
    prompt_path = os.path.join('CharaCraft\\prompt', prompt+'.txt')
    print(db_folder, prompt_path)
    with open(prompt_path, 'r', encoding='utf8') as f:
        system_prompt = f.read().replace('{role_name}', name).replace('character', me)

    chatbot = ChatHaruhi(
        system_prompt=system_prompt,
        llm='openai',
        story_text_folder=db_folder,
        max_len_story=1000,
        role_name=name,
        first_response=first_response
    )

    def respond(message, history):
        chatbot.dialogue_history = [tuple(dialogue) for dialogue in history]
        print(chatbot.dialogue_history)

        response = chatbot.chat(text=message, role=me)

        print(chatbot.llm.print_prompt())
        return response

    with gr.Blocks() as demo:
        gr.ChatInterface(fn=respond, examples=["Nice to meet you."], title="CharaCraft")
    demo.launch(debug=True, share=True)