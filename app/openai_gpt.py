import requests
from dotenv import load_dotenv
import os
import re
from bitrix import notification
import json


load_dotenv()

texts_somnenia = [r"сомнева(?:юсь|емся)"]
texts_menedger = [r"менеджер(?:|а|ом|ы|у|е|ов)"]
texts_payd = [r"оплат(?:а|е|у|ы)"]

def sync_generate_text(user_name, text):
    if any(re.search(pattern, text) for pattern in texts_somnenia):
        return "Видео если человек сомневается"
    elif any(re.search(pattern, text) for pattern in texts_menedger):
        notification(f'{user_name} ожидает менеджера')
        return "Ожидайте! В скором времени менеджер свяжется с вами"
    elif any(re.search(pattern, text) for pattern in texts_payd):
        return "Ссылка на оплату"
    elif text == "Задать дополнительный вопрос":
        return "Я вас слушаю!"
    else:
        """Это версия c использование openAi ,но оно требует пополнения баланса для запуска"""
        # try:
        #     client = openai.OpenAI(api_key="API KEY")
        #     completion = client.chat.completions.create(
        #         model="gpt-4o-mini",
        #         store=True,
        #         messages=[
        #             {"role": "user", "content": text}
        #         ]
        #     )
        #
        #     print(completion.choices[0].message);
        # except Exception as e:
        #     print(f"Error: {e}")
        #     return "Извините, произошла ошибка. Попробуйте позже."


        api_key = os.getenv("COHERE_API_KEY")
        url = 'https://api.cohere.ai/generate'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'command-xlarge-nightly',
            'prompt': text,
            'max_tokens': 100,
            'temperature': 0.5
        }

        try:
            # Отправка POST запроса
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Проверка на успешный ответ
            if response.status_code != 200:
                return f"Ошибка API: {response.status_code}, {response.text}"

            # Парсинг ответа
            result = response.json()

            # Проверка на наличие текста в ответе
            if 'text' in result:
                return result['text'].strip()
            else:
                return "Нет ответа от модели."

        except Exception as e:
            return f"Ошибка запроса: {str(e)}"