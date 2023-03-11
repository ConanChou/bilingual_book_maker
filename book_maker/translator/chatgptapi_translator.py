import time

import openai

from .base_translator import Base


class ChatGPTAPI(Base):
    def __init__(self, key, language, api_base=None):
        super().__init__(key, language)
        self.key_len = len(key.split(","))
        if api_base:
            openai.api_base = api_base

    def rotate_key(self):
        openai.api_key = next(self.keys)

    def translate(self, text, prompt_template):
        prompt_template = prompt_template or "Please help me to translate, `{text}` to {language}, please return only translated content not include the origin text"
        print("\n" + text.strip())
        self.rotate_key()
        try:
            t_text = self._call_completion(text, prompt_template)
        except Exception as e:
            # TIME LIMIT for open api please pay
            sleep_time = int(60 / self.key_len)
            time.sleep(sleep_time)
            print(e, f"will sleep {sleep_time} seconds")
            self.rotate_key()
            t_text = self._call_completion(text, prompt_template)
        print(t_text.strip())
        return t_text

    def _call_completion(self, text, prompt_template):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.4,
            messages=[
                {
                    "role": "user",
                    "content": prompt_template.format(text=text, language=self.language),
                }
            ],
        )
        return (
            completion["choices"][0]
            .get("message")
            .get("content")
            .encode("utf8")
            .decode()
        )
