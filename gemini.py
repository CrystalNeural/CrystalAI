import google.generativeai as genai
from systemInforamtion import getFullData
import json
import re

systemInfo = getFullData()
system_prompt = "Ты CrystalAI - Виртуальный помощник человека. Ты должна помогать пользователю с разными вопросами. У пользователя в системе что то может не работать и ты должна помогать с этим. Вот система пользователя: {system}. Например, пользователь скажет прибавь громкость на 5, то ты должна скинуть команду для командной строки в виде <systemCommand>Команда</systemCommand> и он автоматически выполниться (Обязательно пиши в синтаксисе <systemCommand>Команда</systemCommand>). Такой командный блок в тексте должен быть только один и вывод команды будет отправляться тебе и ты должен анализировать вывод и на основе анализа решить, крманда работает или нет. Если да, то напиши что все хорошо, а если не, то напиши что вышла ошибка и отправь команду для решений этой проблемы. Также пользователь может спрашивать тебя о чём угодно. Например, какой диаметр планеты Земли и ты должна ответить ему.".format(system=json.dumps(systemInfo))

class Gemini:
    def __init__(self, token, model="gemini-2.0-flash"):
        genai.configure(api_key=token)
        self.geminiModel = genai.GenerativeModel(
            model_name=model, 
            generation_config={
                "temperature": 0.1,
                "top_p": 1,
                "top_k": 1,
            }, 
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
    
    def generate(self, context):
        if not context: raise ValueError("Укажите контекст!")
        response = self.geminiModel.generate_content(contents=(
            f"Твой системный промпт: {system_prompt}\n"
            f"Твой контекст: {context}\n"
        ))
        match = re.search(r'<systemCommand>(.*?)</systemCommand>', response.text, re.DOTALL)
        command = match.group(1) if match else None
        clean_text = re.sub(r'<systemCommand>.*?</systemCommand>', '', response.text, flags=re.DOTALL)
        return {"text": clean_text, "command": command}