from google import genai
from google.genai import types
import subprocess
from systemInforamtion import getFullData
import json

systemInfo = getFullData()
system_prompt = "Ты CrystalAI - Виртуальный помощник человека. Ты должна помогать пользователю с разными вопросами. У пользователя в системе что то может не работать и ты должна помогать с этим. Система пользователяB {system} Например, пользователь скажет прибавь громкость на 5, то у тебя есть функция run_command, которая запускает команду в командной строке системы пользователя. На основе вывода этой команды, ты должна определить, сработала ли команда или нет. Если да, то напиши что все хорошо, а если нет, то напиши что ошибка и попытайся исправить её. Также пользователь может спрашивать тебя о чём угодно. Например, какой диаметр планеты Земли и ты должна ответить ему.".format(system=json.dumps(systemInfo))

def run_command(command: str) -> str:
    """
    Функция для запуска команды в командной строке системы пользователя

    Args:
        command (str): Команда для запуска

    Returns:
        str: Вывод команды
    """
    command_output = ""
    
    try:
        command_output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        command_output = f"Ошибка: {e.output}"
    finally:
        return command_output

class Gemini:
    def __init__(self, token, model="gemini-2.5-flash"):
        client = genai.Client(api_key=token)
        self.chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                tools=[run_command],
                system_instruction=system_prompt,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
        )
    
    def send_message(self, message):
        if not message: raise ValueError("Укажите текст!")
        response = self.chat.send_message_stream(message)
        for i in response:
            if i.automatic_function_calling_history:
                yield {"text": i.text, "cmd": {"command": i.automatic_function_calling_history[-2].parts[-1].function_call.args["command"], "command_output": i.automatic_function_calling_history[-1].parts[0].function_response.response["result"]}}
            else:
                yield {"text": i.text, "cmd": {}}
        #return {"text": response.text, "cmd": {"command": response.automatic_function_calling_history[-2].parts[-1].function_call.args["command"], "command_output": response.automatic_function_calling_history[-1].parts[0].function_response.response["result"]}}
        #return {"text": response.text, "cmd": None}