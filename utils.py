from time import sleep
# from pyperclip import paste as paste_from_clipboard
# copying to clipboard - putting data in collector and execution
from collections import deque
from keyboard import send, write

class KeyboardDataCollector:
    def __init__(self) -> None:
        self.keys = deque()

    def collect(self, event):
        key = event.name
        self.keys.append(key)

    def get_all(self):
        while self.keys:
            yield self.keys.popleft()

class DataInterpreter:
    def __init__(self):
        self.COMMAND_START_CHAR = '@'
        self.ENTER = 'enter'
        self.TAB = 'tab'
        self.BACKSPACE = 'backspace'
        self.SPACE = 'space'
        self.RIGHT = 'right'
        self.LEFT = 'left'

        self.keyboard_data_generator = None

        self.collecting_activity = False
        self.command_chars = []
        self.keys_amount_after_command_start = 1
        self.inserting_index = 0

        self.enter_pressed = False
        self.tab_pressed = False

    def put_data_generator(self, keyboard_data_generator):
        self.keyboard_data_generator = keyboard_data_generator

    def interprate(self):
        for key in self.keyboard_data_generator:
            if key == self.COMMAND_START_CHAR:
                self.reset() 
                self.collecting_activity = True
            
            if self.collecting_activity:
                match(key):
                    case self.ENTER:
                        self.enter_pressed = True

                    case self.TAB:
                        self.tab_pressed = True

                    case self.BACKSPACE if self.command_chars:
                        # while self.inserting_index + 1 >= len(self.command_chars):
                        #     self.inserting_index -= 1
                        print('len:', len(self.command_chars), 'index:', self.inserting_index)
                        self.command_chars.pop(self.inserting_index)
                        self.keys_amount_after_command_start -= 1

                    case self.RIGHT if self.inserting_index + 1 <= len(self.command_chars):
                        self.increase_inserting_index()
                        
                    case self.LEFT if self.inserting_index - 1 >= -1:
                        if self.inserting_index - 1 == -1:
                            self.collecting_activity = False
                            self.inserting_index = 0
                        else:
                            self.inserting_index -= 1

                        
                self.add_key(key)
                self.update_keys_amount(key)

    def add_keys_and_update_keys_amount(self, keys):
        for key in keys:
            self.add_key(key)
            self.update_keys_amount(key)

        self.inserting_index -= 1

    def update_keys_amount(self, key):
        if (len(key) == 1 and key != self.COMMAND_START_CHAR) or key in {self.ENTER, self.SPACE}:
            self.keys_amount_after_command_start += 1

    def add_key(self, key):
        if key == self.COMMAND_START_CHAR:
            return

        if key == self.SPACE:
            key = ' '

        if len(key) == 1:
            self.increase_inserting_index()
            self.command_chars.insert(self.inserting_index, key) 

    def increase_inserting_index(self):
        # print('len:', len(self.command_chars), 'index:', self.inserting_index)

        self.inserting_index += 1

    def reset(self):
        self.reset_command_chars()
        self.reset_keys_amount()
        self.collecting_activity = False
        self.inserting_index = 0

    def get_keys_amount_after_command_start(self):
        return self.keys_amount_after_command_start


    def get_precommand(self):
        return self.create_command()

    def create_command(self):
        return ''.join(self.command_chars)
    
    def reset_command_chars(self):
        self.command_chars.clear()


    def reset_keys_amount(self):
        self.keys_amount_after_command_start = 1

    
    def is_enter_pressed(self):
        if self.enter_pressed:
            self.enter_pressed = False
            return True
        else:
            return False
        
    def is_tab_pressed(self):
        if self.tab_pressed:
            self.tab_pressed = False
            return True
        else:
            return False
    
    def is_collecting_active(self):
        return self.collecting_activity

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
            input(str(_))
        
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
        print('xdddd dd')

class SuggestionsManager:
    def __init__(self, possible_commands) -> None:
        self.possible_commands = possible_commands
        self.suggestions = []
        self.precommand = None

    def set_precommand(self, precommand):
        self.precommand = precommand
        self.update_suggestions()

    def update_suggestions(self):
        self.suggestions = list(self.find_similar_command_to_precommand())

    def find_similar_command_to_precommand(self):
        for command_name in self.possible_commands:
            if command_name.startswith(self.precommand) or self.precommand.startswith(command_name):
                yield command_name

    def best(self):
        if self.suggestions:
            return self.suggestions[0]

    def all(self):
        if self.suggestions:
            return self.suggestions

def remove_entered_keys_from_screen(keys_amount):
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
        return command.replace(' ', ''), None
    
    if abs(start_bracket_index - end_bracket_index) == 1:
        return command[:start_bracket_index].replace(' ', ''), None
    
    name = command[:start_bracket_index].replace(' ', '')

    args_string = command[start_bracket_index + 1:end_bracket_index]

    args = [arg_str.rstrip().lstrip() for arg_str in args_string.split(',')]

    return name, args