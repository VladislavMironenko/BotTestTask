import requests
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv('WEBHOOK_URL_BITRIX')

def create_deal(id_user, segment, questions_text):
    # Создание простой сделки
    deal_data = {
        'fields': {
            'TITLE': f'Пользователь: {id_user}',
            'COMMENTS': f'Данные сделки:\n{segment}\n{questions_text}',
        }
    }
    response = requests.post(f'{webhook_url}/crm.deal.add', json=deal_data)
    result = response.json()
    deal_id = result['result']
    return deal_id


def update_deal(deal_id , message , message_ai):
    get_data = {
         'id': str(deal_id)
    }
    get_response = requests.post(f'{webhook_url}/crm.deal.get', json=get_data)
    current_deal = get_response.json()
    current_deal = current_deal.get('result' , {}).get('COMMENTS', '')

    update_data = {
        'id': deal_id,
        'fields': {
            'COMMENTS': f'{current_deal} \n {message} \n {message_ai}',
        }
    }

    response = requests.post(f'{webhook_url}/crm.deal.update', json=update_data)
    return response.status_code


def notification(message):
    payload = {
        'to': '1',
        'message': message
    }

    try:
        response = requests.post(f'{webhook_url}im.notify', json=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Ошибка отправки: {e}")
        return False
