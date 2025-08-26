import random

from service.service import Service
from ui.console_ui import ConsoleUi
from ui.graphic_ui import GraphicUi


def read_settings(file_name):
    settings = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                settings[key.strip()] = value.strip()
    return settings

def start():
    settings = read_settings('settings.properties')
    difficulty = settings['difficulty'].lower()
    ui = settings['ui'].lower()

    print('Welcome to Reversi Game!')
    human_player = 'X' if random.choice([True, False]) else 'O'
    if human_player == 'X':
        computer_player = 'O'
        print("You are Black ('X'). You go first.")
    else:
        computer_player = 'X'
        print("You are White ('O'). The computer goes first.")

    if difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid difficulty level. Please check the settings.properties file.")
        return
    if ui not in ['console', 'graphic']:
        print("Invalid UI. Please check the settings.properties file.")
        return

    service = Service(human_player, difficulty)
    if ui == 'console':
        ui = ConsoleUi(service)
        ui.play()
    else:
        ui = GraphicUi(service)
        ui.play()

if __name__ == '__main__':
    start()