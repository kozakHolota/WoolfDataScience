import os
from pathlib import Path

from home_works.ai_agentic_systems.homework_2.openai_client import OpenAIClient


def main():
    tasks = 3

    for i in range(1, tasks + 1):
        print(f"{10*'='}Завдання №{i}{10*'='}")
        result_template_json = Path(f"json_data/task_{i}.json").read_text()
        examples = Path(f"examples/task_{i}.txt").read_text()
        api_key = os.environ.get("OPENROUTER")
        texts = Path(f"test_data/task_{i}.txt").read_text().splitlines()

        openai_client = OpenAIClient(api_key, result_template_json, examples)

        for text in texts:
            print(f"Текст: {text}")
            print("Аналіз моделі")
            print(openai_client.get_response(text))


if __name__ == "__main__":
    main()
