from suggestionswindow import ListWidget
from utils import (
    CommandsExecutor, DataInterpreter, KeyboardDataCollector,
    remove_entered_keys_from_screen, SuggestionsManager
)
from typing import Callable, Any
from time import sleep
from keyboard import write, send

class MainLoop:
    def __init__(self, 
            interpreter: DataInterpreter, 
            collector: KeyboardDataCollector, 
            executor: CommandsExecutor, 
            list_widget: ListWidget, 
            suggestions_manager: SuggestionsManager,
            commands_and_methods: dict[str, Callable[[Any], Any]],
            delay: float):
        
        self.interpreter = interpreter
        self.collector = collector
        self.executor = executor
        self.list_widget = list_widget
        self.delay = delay
        self.commands_and_methods = commands_and_methods
        self.suggestions_manager = suggestions_manager
        self.command_names = list(self.commands_and_methods.keys())

        self.current_precommand = None

    def start(self):
        while True:
            self.interpreter.put_data_generator(self.collector.get_all())
            self.interpreter.interprate()
            
            precommand = self.interpreter.get_precommand()
            keys_amount = self.interpreter.get_keys_amount_after_command_start() 
            is_enter_pressed = self.interpreter.is_enter_pressed()

            self.handle_precommand(precommand)
            
            self.write_suggestion(precommand, is_enter_pressed)

            if is_enter_pressed and (')' in precommand or '(' in precommand):
                remove_entered_keys_from_screen(keys_amount)
                self.executor.execute(precommand)
                self.interpreter.reset()     

            sleep(self.delay)

    def handle_precommand(self, precommand):
        if precommand != self.current_precommand:
            self.current_precommand = precommand

            self.suggestions_manager.set_precommand(precommand)
            self.list_widget.updateSuggestions()    

            print("PRE:", precommand)

    def write_suggestion(self, precommand, is_enter_pressed):
        if is_enter_pressed and (')' not in precommand or '(' not in precommand):
            remove_entered_keys_from_screen(1)

            best_suggestion_item = self.list_widget.item(self.list_widget.currentRow())

            if best_suggestion_item == None:
                return
            
            best_suggestion = best_suggestion_item.text()
            text_to_add = best_suggestion.removeprefix(precommand.replace(' ', '')) + '()'

            print('TExt to add:', text_to_add)

            write(text_to_add)
            self.interpreter.add_keys_and_update_keys_amount(text_to_add)