import json
from typing import Any, Dict, Optional, Union
from langdetect import detect
import re


def load_config(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


config = load_config('./spider/spider.json')


class GeneralPipeline:
    def process_item(self, item: Dict[str, str], spider: Any) -> Dict[str, str]:
        lines = [re.sub(r'\s+', ' ', line.strip()) for line in item['text'].split('\n') if line.strip()]
        item['text'] = '\n'.join(lines)
        return item


def get_language(text: str) -> Optional[str]:
    try:
        return detect(text)
    except Exception:
        return None


def get_text_length(text: str) -> int:
    language = get_language(text)
    if language == 'en':
        return len(text.split())
    elif language in ['zh', 'ja']:
        return len(text)
    else:
        return len(text.split())


class ConfiguredPipeline:
    def should_remove_line(self, line: str, path_config: Dict[str, Any]) -> bool:
        line_length = get_text_length(line)
        if any(keyword in line for keyword in path_config.get('rm_line_keywords', [])):
            return True
        if line_length < path_config.get('min_line_len', 0):
            return True
        if line_length > path_config.get('max_line_len', float('inf')):
            return True
        return False

    def substitute_keywords(self, line: str, path_config: Dict[str, Any]) -> str:
        for keyword, replacement in path_config.get('sub_keywords', {}).items():
            if keyword in line:
                line = line.replace(keyword, replacement)
        return line

    def process_item(self, item: Dict[str, str], spider: Any) -> Optional[Dict[str, str]]:
        text = item['text'].split('\n')
        url_paths = item['url'].split('/')

        processed_text = []
        for line in text:
            should_append = True
            for path in url_paths:
                path_config = config.get(path, {})
                if any(keyword in line for keyword in path_config.get('rm_page_keywords', [])):
                    return None
                if self.should_remove_line(line, path_config):
                    should_append = False
                    break
                line = self.substitute_keywords(line, path_config)
            if should_append and line.strip():
                processed_text.append(line)

        item['text'] = '\n'.join(processed_text)
        return item
