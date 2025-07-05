from gemini import Gemini
from rich.markdown import Markdown
from rich.console import Console
from config import AI_MODEL, AI_TOKEN
import json
import subprocess

banner = "   _____                _        _            _____ \n  / ____|              | |      | |     /\\   |_   _|\n | |     _ __ _   _ ___| |_ __ _| |    /  \\    | |  \n | |    | '__| | | / __| __/ _` | |   / /\\ \\   | |  \n | |____| |  | |_| \\__ \\ || (_| | |  / ____ \\ _| |_ \n  \\_____|_|   \\__, |___/\\__\\__,_|_| /_/    \\_\\_____|\n               __/ |                                \n              |___/                                 "
print(banner)

context = []
console = Console()
gemini = Gemini(AI_TOKEN, AI_MODEL)

def gen(userText):
    context.append({"role": "user", "content": userText})
    AI_response = gemini.generate(json.dumps(context))
    text = AI_response['text']
    context.append({"role": "assistant", "content": AI_response["text"]})
    if AI_response["command"]: text += f"\n\nВнимание, Нейронная сеть отправила команду:\n```{AI_response['command']}```\nКоманда выполнится автоматический!"
    md = Markdown("\n"+text+"\n")
    # print()
    console.print(md)
    if AI_response['command']:
        try:
            stdout = subprocess.check_output(AI_response['command'], shell=True, text=True, stderr=subprocess.STDOUT)
            print(f"Вывод команды {AI_response['command']}: {stdout}")
            print("Отправка вывода нейронной сети...")
            gen(f"Вывод команды {AI_response['command']}: ```Вывод: {stdout}``` ")
        except subprocess.CalledProcessError as e:
            print(f"Вывод команды {AI_response['command']}: Ошибка: {e.output}")
            print("Отправка вывода нейронной сети...")
            gen(f"Вывод команды {AI_response['command']}: ```Ошибка: {e.output}``` ")

while True:
    try:
        userText = input("Введите запрос к нейросети: ")
        gen(userText)
    except Exception as e:
        print(f"Ошибка: {repr(e)}")