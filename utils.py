from time import sleep
# from pyperclip import paste as paste_from_clipboard
# copying to clipboard - putting data in collector and execution
from collections import deque
from keyboard import send, write

COMMANDS = [
    "Kasia",
    "Antek",
    "Bartek",
    "Ola",
    "Kacper",
    "Dariusz",
    "Ananas",
    "Jablko",
    "Cytryna",
    "Pomidor"
]

class KeyboardDataCollector:
    def __init__(self) -> None:
        self.keys = deque()

    def collect(self, event):
        key = event.name
        self.keys.append(key)

    def get_all(self):
        while self.keys:
            yield self.keys.popleft()

    def get_few(self, amount):
        for _ in range(amount):
            if not self.keys:
                return

            yield self.keys.popleft()

class DataInterpreter:
    def __init__(self) -> None:
        self.COMMAND_START_CHAR = '@'
        self.ENTER = 'enter'
        self.BACKSPACE = 'backspace'
        self.SPACE = 'space'

        self.keyboard_data = []

        self.command_chars = []
        self.is_collecting_active = False

        self.keys_amount_hisotry = []
        self.keys_amount_after_command_start = 1

        self.commands = []

        self.enter_pressed = False

    def put(self, keyboard_data):
        self.keyboard_data = keyboard_data
        return self

    def interprate(self):
        for key in self.keyboard_data:
            match(key):
                case self.COMMAND_START_CHAR:
                    self.is_collecting_active = True

                    self.reset_command_chars()
                    self.reset_keys_amount()

                case self.ENTER if self.is_collecting_active:
                    self.is_collecting_active = False

                    self.update_commands_history()
                    self.update_keys_amount_history()

                case self.BACKSPACE if self.command_chars:
                    self.command_chars.pop()
                    self.keys_amount_after_command_start -= 1
            
            if self.is_collecting_active:
                if len(key) == 1:
                    self.command_chars.append(key)
                elif key == self.SPACE:
                    self.command_chars.append(' ')
                
                if len(key) == 1 or key in {self.ENTER, self.SPACE}:
                    # print(key)
                    self.keys_amount_after_command_start += 1
                
                if key == 'tab':
                    self.enter_pressed = True

        # Reset
        self.keyboard_data = []

    def get_precommand(self):
        # precommand - part of potential command, incomplete command

        return self.create_command()

    def get_commands(self): 
        while self.commands:
            yield self.commands.pop()

    def get_keys_amount_hisotry(self):
        while self.keys_amount_hisotry:
            yield self.keys_amount_hisotry.pop()

    def update_commands_history(self):
        self.commands.append(self.create_command())

    def create_command(self):
        return ''.join(self.command_chars)
    
    def reset_command_chars(self):
        self.command_chars.clear()


    def reset_keys_amount(self):
        self.keys_amount_after_command_start = 1

    def update_keys_amount_history(self):
        self.keys_amount_hisotry.append(self.keys_amount_after_command_start)

class CommandsExecutor:
    def __init__(self, commands_and_methods=None):
        if commands_and_methods == None:
            self.commands_and_methods = {}
        else:
            self.commands_and_methods = commands_and_methods

    def execute(self, command):
        try:
            self.actual_execute(command)
        except Exception as _:
            input(_)
        
    def actual_execute(self, command):
        name, args = command_to_name_and_args(command)

        method = self.get_method(name)

        if method != None:
            if args == None:
                method()
            else:
                method(*args)        
    
    def get_method(self, command_name):
        if command_name in self.commands_and_methods:
            return self.commands_and_methods[command_name]

class StorageHandler:
    def __init__(self, storage=None) -> None:
        if storage == None:
            self.storage = {}
        else:
            self.storage = storage

    def get(self, key):
        if key in self.storage:
            write(self.storage[key])        

    def set(self, key, value):
        self.storage[key] = value

    def getall(self):
        write(str(self.storage))

def remove_entered_command_from_screen(keys_amount):
    string = ','.join(['backspace'] * keys_amount)
    send(string)   

def read_command_args(command: str):
    start_bracket_index = command.find('(')
    end_bracket_index = command.find(')')

    return command[start_bracket_index + 1:end_bracket_index]
    
def command_to_name_and_args(command: str):
    start_bracket_index = command.find('(')
    end_bracket_index = command.find(')')

    if start_bracket_index == -1 or end_bracket_index == -1:
        return command[1:].replace(' ', ''), None

    name = command[1:start_bracket_index].replace(' ', '')

    args_string = command[start_bracket_index + 1:end_bracket_index]

    args = [arg_str.rstrip().lstrip() for arg_str in args_string.split(',')]

    return name, args

def find_similar_command_to_precommand(command_names, precommand_name):
    for command_name in command_names:
        if command_name.startswith(precommand_name):
            yield command_name

def command_to_command_name(command):
    return command[1:]