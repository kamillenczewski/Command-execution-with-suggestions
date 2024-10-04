from suggestionswindow import ListWidget
from utils import CommandsExecutor, DataInterpreter, KeyboardDataCollector, command_to_command_name, find_similar_command_to_precommand, remove_entered_command_from_screen
from typing import Callable, Any
from time import sleep
from keyboard import write, send

class MainLoop:
    def __init__(self, 
            interpreter: DataInterpreter, 
            collector: KeyboardDataCollector, 
            executor: CommandsExecutor, 
            list_widget: ListWidget, 
            commands_and_methods: dict[str, Callable[[Any], Any]],
            delay: float):
        
        self.interpreter = interpreter
        self.collector = collector
        self.executor = executor
        self.list_widget = list_widget
        self.delay = delay
        self.commands_and_methods = commands_and_methods
        self.command_names = list(self.commands_and_methods.keys())

        self.current_precommand = None

    def interprete(self):
        self.interpreter.put(self.collector.get_all()).interprate()

    def start(self):
        while True:
            self.interprete()
            
            commands = self.interpreter.get_commands()
            keys_amount_history = self.interpreter.get_keys_amount_hisotry() 
            precommand = self.interpreter.get_precommand()
            
            self.handle_precommand(precommand)

            if self.interpreter.enter_pressed:
                self.interpreter.enter_pressed = False
                best_suggestion_command = self.list_widget.item(self.list_widget.currentRow()).text()
                send('backspace')
                write(best_suggestion_command.removeprefix(command_to_command_name(precommand)))

            self.execute_commands(commands, keys_amount_history)
                
            sleep(self.delay)

    def handle_precommand(self, precommand):
        if precommand != self.current_precommand:
            self.list_widget.clearItems()

            self.current_precommand = precommand

            similiar_commands = find_similar_command_to_precommand(
                self.command_names, 
                command_to_command_name(precommand)
            )

            self.list_widget.addItems(similiar_commands)
            self.list_widget.setCurrentRow(0)

    def execute_commands(self, commands, keys_amount_history):
        for command, keys_amount in zip(commands, keys_amount_history):
            remove_entered_command_from_screen(keys_amount)
            self.executor.execute(command)
            