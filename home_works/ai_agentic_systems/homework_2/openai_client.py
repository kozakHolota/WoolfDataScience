import json
from json import JSONDecodeError

from openai import APIError, OpenAI


class OpenAIClient:
    def __init__(
        self,
        api_key: str,
        result_template_json: str,
        examples: str,
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0.0,
    ):
        self.result_template_json = result_template_json
        self.model = model
        self.temperature = temperature
        self.examples = examples
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def get_response(self, text: str) -> dict:
        developer_prompt = f"""
        Повертай мені відповідь типу JSON наступного формату:
        {self.result_template_json}
        Повертай мені виключно поля, перераховані у шаблоні JSON і нічого більше за це.
        Не повертай мені жодного тексту, окрім JSON.
        """

        user_prompt = f"""
        Дано повідомлення: {text}
        Поверни мені JSON, з полями згідно поданого формату. Візьми за основу наступні приклади:
        {self.examples}
        """

        try:
            content = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": developer_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
            ).choices[0].message.content
        except APIError as e:
            return {"error": f"API error: {e}"}

        if content is None:
            return {"error": "Empty response from model"}

        try:
            return json.loads(content)
        except JSONDecodeError:
            return {"error": "Invalid JSON response"}
