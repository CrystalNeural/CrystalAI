from gemini import Gemini
from rich.markdown import Markdown
from rich.console import Console
from config import AI_MODEL, AI_TOKEN
import json

banner = "   _____                _        _            _____ \n  / ____|              | |      | |     /\\   |_   _|\n | |     _ __ _   _ ___| |_ __ _| |    /  \\    | |  \n | |    | '__| | | / __| __/ _` | |   / /\\ \\   | |  \n | |____| |  | |_| \\__ \\ || (_| | |  / ____ \\ _| |_ \n  \\_____|_|   \\__, |___/\\__\\__,_|_| /_/    \\_\\_____|\n               __/ |                                \n              |___/                                 "
print(banner, "\n")

context = []
console = Console()
gemini = Gemini(AI_TOKEN, AI_MODEL)

while True:
    try:
        userText = input("Введите запрос к нейросети: ")
        print()
        response = gemini.send_message(userText)
        if response["cmd"]:
            console.print(Markdown("\n" + f"Вывод команды {response['cmd']['command']}:\n\n```\n{response['cmd']['command_output']}```"))
            print()
        console.print(Markdown(response["text"]))
        print()
    except KeyboardInterrupt:
        print("\nЗавершение...")
        exit(0)
    except Exception as e:
        print(f"Ошибка: {repr(e)}")