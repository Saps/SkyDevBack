import sys,requests
import pandas as pd
# sys.path.append('/Users/aelitta/Documents/salute-speech') #путь к функциям похожести
from deepseek_python_similarity_metrics import TextNormalizer, TextSimilarityCalculator
from dotenv import load_dotenv
import os

#load_dotenv()

#OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')


def extract_txt_file(file_path):
    # Чтение TXT файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Обрезаем текст если слишком длинный (ограничение контекста)
    max_length = 10000  # подстройте под вашу модель
    if len(text_content) > max_length:
        text_content = text_content[:max_length]

    return text_content

#def get_similarity_by_hard_skills(folder_path, skills):
def get_similarity_by_hard_skills(file_text):
    calculator = TextSimilarityCalculator()
    sim_dict = {}

        # Запрос к OpenRouter
    API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
    API_URL = 'https://openrouter.ai/api/v1/chat/completions'
    headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    data = {
            "model": "deepseek/deepseek-chat-v3.1:free",
            "max_tokens" : 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Проанализируй этот документ и выдели hard skills, опыт и образование кандидатов:\n\n{file_text}, выведи только hard skills, опыт и образование"
                }
            ]
        }
    response = requests.post(API_URL, json=data, headers=headers)

        # Check if the request was successful
    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print("Failed to fetch data from API. Status Code:", response.status_code)

    result = response.json()

        #similarity = calculator.calculate_similarity_text(skills, result['choices'][0]['message']['content'])
        #sim_dict[res] = similarity

    return result

