from gemini import Gemini
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from config import AI_MODEL, AI_TOKEN
import warnings
warnings.filterwarnings("ignore", message=".*non-text parts in the response.*")
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
        current_command = {"command": "", "command_output": ""}
        response_buffer = ""
        with Live(console=console, auto_refresh=False, vertical_overflow="visible") as live:
            for response_part in response:
                if response_part["cmd"] and response_part["cmd"]["command"] != current_command["command"]:
                    current_command = response_part["cmd"]
                    response_buffer += "\n" + f"Вывод команды {response_part['cmd']['command']}:\n\n```\n{response_part['cmd']['command_output']}```\n"
                if response_part["text"]: response_buffer += response_part["text"]
                markdown = Markdown(response_buffer)
                live.update(markdown, refresh=True)
        print()
    except KeyboardInterrupt:
        print("\nЗавершение...")
        exit(0)
    except Exception as e:
        print(f"Ошибка: {repr(e)}")