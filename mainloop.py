from suggestionswindow import ListWidget, MainWindow
from utils import (
    CommandsExecutor, DataInterpreter, KeyboardDataCollector,
    remove_entered_keys_from_screen
)
from typing import Callable, Any
from time import sleep
from keyboard import write, hook_key, unhook
from functools import partial

def on_up_arrow_click(list_widget, event):
    list_widget.goUp()

def on_down_arrow_click(list_widget, event):
    list_widget.goDown()

class MainLoop:
    def __init__(self, 
            interpreter: DataInterpreter, 
            collector: KeyboardDataCollector, 
            executor: CommandsExecutor, 
            list_widget: ListWidget,
            main_window: MainWindow,
            commands_and_methods: dict[str, Callable[[Any], Any]],
            delay: float):
        
        self.interpreter = interpreter
        self.collector = collector
        self.executor = executor
        self.list_widget = list_widget
        self.main_window = main_window
        self.delay = delay
        self.commands_and_methods = commands_and_methods
        self.command_names = list(self.commands_and_methods.keys())

        self.up_arrow_method = partial(on_up_arrow_click, list_widget)
        self.down_arrow_method = partial(on_down_arrow_click, list_widget)

        self.current_precommand = None

    def start(self):
        while True:
            data = self.collector.get_all()
            self.interpreter.put_data_generator(data)
            self.interpreter.interprate()
            
            precommand = self.interpreter.get_precommand()
            keys_amount = self.interpreter.get_keys_amount_after_command_start() 
            is_enter_pressed = self.interpreter.is_enter_pressed()
            is_tab_pressed = self.interpreter.is_tab_pressed()
            collecting_activity = self.interpreter.is_collecting_active()

            self.handle_precommand(precommand)
            
            self.write_suggestion(precommand, is_enter_pressed, is_tab_pressed)

            if is_enter_pressed and (')' in precommand or '(' in precommand):
                remove_entered_keys_from_screen(keys_amount)
                self.executor.execute(precommand)
                self.interpreter.reset()     

            if collecting_activity and not self.main_window.isVisible():
                self.main_window.addWindowAction('show')
                self.hook_and_supress_up_arrow()
                self.hook_and_supress_down_arrow()
            
            if self.main_window.isVisible() and not collecting_activity:
                self.main_window.addWindowAction('hide')
                self.unhook_and_unblock_up_arrow()
                self.unhook_and_unblock_down_arrow()

            sleep(self.delay)

    def hook_and_supress_up_arrow(self):
        hook_key('up', self.up_arrow_method, suppress=True)

    def hook_and_supress_down_arrow(self):
        hook_key('down', self.down_arrow_method, suppress=True)

    def unhook_and_unblock_up_arrow(self):
        unhook(self.up_arrow_method)

    def unhook_and_unblock_down_arrow(self):
        unhook(self.down_arrow_method)

    def handle_precommand(self, precommand):
        if precommand != self.current_precommand:
            self.current_precommand = precommand

            self.list_widget.setPrecommand(precommand)
            self.list_widget.updateSuggestions()    

            print("PRE:", precommand)

    def write_suggestion(self, precommand, is_enter_pressed, is_tab_pressed):
        if (is_enter_pressed or is_tab_pressed) and (')' not in precommand or '(' not in precommand):
            remove_entered_keys_from_screen(1)

            best_suggestion_item = self.list_widget.item(self.list_widget.currentRow())

            if best_suggestion_item == None:
                return
            
            best_suggestion = best_suggestion_item.text()
            text_to_add = best_suggestion.removeprefix(precommand.replace(' ', '')) + '()'

            write(text_to_add)
            self.interpreter.add_keys_and_update_keys_amount(text_to_add)