from dataclasses import dataclass, asdict
import requests
import json


@dataclass
class CompletionOptions:
    stream: bool = False
    temperature: float = 0.6
    maxTokens: int = 1000


@dataclass
class Message:
    role: str
    text: str


@dataclass
class Prompt:
    modelUri: str
    completionOptions: CompletionOptions
    messages: list[Message]


class YandexGPT:
    def __init__(self, token: str, catalog: str, system=None):
        self.token = token
        self.catalog = catalog
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.user_messages = []
        self.assistent_messages = []
        self.system_messages = []
        if system:
            self.system_messages.append(Message('system', system))

    def get_answer(self, question: str, tokens: int = 1000) -> str:
        self.user_messages.append(Message('user', question))

        prompt = Prompt(
            modelUri=f"gpt://{self.catalog}/yandexgpt-lite",
            completionOptions=CompletionOptions(maxTokens=tokens),
            messages=self.user_messages + self.system_messages + self.assistent_messages
        )
     
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        # Преобразование dataclass в словарь, а затем в JSON
        payload = json.loads(json.dumps(asdict(prompt)))
        response = requests.post(self.url, headers=headers, json=payload)
        result = response.json()['result']['alternatives'][0]['message']['text']

        self.user_messages.append(Message('assistant', result))
        return result
