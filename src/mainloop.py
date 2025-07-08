from listwidget import ListWidget
from mainwindow import MainWindow
from commandsexecutor import CommandsExecutor
from datainterpreter import DataInterpreter
from keyboarddatacollector import KeyboardDataCollector

from typing import Callable, Any
from time import sleep
from keyboard import write, hook_key, unhook, send
from pynput.mouse import Listener

def remove_entered_keys_from_screen(keys_amount):
    string = ','.join(['backspace'] * keys_amount)
    send(string)   

def on_up_arrow_click(list_widget, event):
    list_widget.goUp()

def on_down_arrow_click(list_widget, event):
    list_widget.goDown()

class UpDownIterator:
    def __init__(self, list_widget: ListWidget):
        self.do_execute = False
        self.list_widget = list_widget

    def up(self):
        if self.do_execute:
            self.list_widget.goUp()
            self.do_execute = False
        else:
            self.do_execute = True

    def down(self):
        if self.do_execute:
            self.list_widget.goDown()
            self.do_execute = False
        else:
            self.do_execute = True

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

        self.scroll_listener = Listener(on_scroll=self.on_scroll)
        self.start_scroll_listener()
        self.hook_and_supress_up_arrow()
        self.hook_and_supress_down_arrow()
        self.are_up_down_keys_hooked = True

        self.current_precommand = None

        self.up_down_iterator = UpDownIterator(self.list_widget)

        self.is_active = False

    def start(self):
        self.activate()

        while self.is_active:
            data = self.collector.get_all()
            self.interpreter.put_data_generator(data)
            self.interpreter.interprate()
            
            self.new_precommand = self.interpreter.get_precommand()
            self.keys_amount = self.interpreter.get_keys_amount_after_command_start() 
            self.is_enter_pressed = self.interpreter.is_enter_pressed()
            self.is_tab_pressed = self.interpreter.is_tab_pressed()
            self.collecting_activity = self.interpreter.is_collecting_active()

            self.handle_precommand()

            self.write_suggestion()

            self.try_execute_command_and_remove_from_screen()
     
            self.try_show_window()
            self.try_hook_methods()
            
            self.try_hide_window()
            self.try_unhook_methods()

            sleep(self.delay)

    def try_execute_command_and_remove_from_screen(self):
        if self.is_enter_pressed and (')' in self.new_precommand or '(' in self.new_precommand):
            remove_entered_keys_from_screen(self.keys_amount)
            self.executor.execute(self.new_precommand)
            self.interpreter.reset()  

    def try_show_window(self):
        if self.collecting_activity and not self.main_window.isVisible():
            self.main_window.show() 
    
    def try_hook_methods(self):
        if self.collecting_activity and not self.main_window.isVisible() and not self.are_up_down_keys_hooked:
            # self.start_scroll_listener()
            self.hook_and_supress_up_arrow()
            self.hook_and_supress_down_arrow()
            self.are_up_down_keys_hooked = True

    def try_hide_window(self):
        if not self.collecting_activity and self.main_window.isVisible():
            self.main_window.hide()
    
    def try_unhook_methods(self):
        if not self.collecting_activity and self.main_window.isVisible() and self.are_up_down_keys_hooked:
            self.unhook_and_unblock_up_arrow()
            self.unhook_and_unblock_down_arrow()
            self.are_up_down_keys_hooked = False



    def hook_and_supress_up_arrow(self):
        hook_key('up', self.on_up_arrow_click, suppress=True)

    def hook_and_supress_down_arrow(self):
        hook_key('down', self.on_down_arrow_click, suppress=True)

    def unhook_and_unblock_up_arrow(self):
        unhook(self.on_up_arrow_click)

    def unhook_and_unblock_down_arrow(self):
        unhook(self.on_down_arrow_click)

    def start_scroll_listener(self):
        self.scroll_listener.start()


    def on_up_arrow_click(self, _):
        #self.list_widget.goUp()
        self.up_down_iterator.up()

    def on_down_arrow_click(self, _):
        #self.list_widget.goDown()
        self.up_down_iterator.down()

    def on_scroll(self, _1, _2, _3, dy):
        if not self.collecting_activity:
            return

        match(dy):
            case 1:
                self.list_widget.goUp()
            case -1:
                self.list_widget.goDown()


    def handle_precommand(self):
        if self.new_precommand != self.current_precommand:
            self.current_precommand = self.new_precommand

            self.list_widget.setPrecommand(self.new_precommand)
            self.list_widget.updateSuggestions()    

    def write_suggestion(self):
        if (self.is_enter_pressed or self.is_tab_pressed) and (')' not in self.new_precommand or '(' not in self.new_precommand):
            remove_entered_keys_from_screen(1)

            best_suggestion_item = self.list_widget.item(self.list_widget.currentRow())

            if best_suggestion_item == None:
                return
            
            best_suggestion = best_suggestion_item.text()
            text_to_add = best_suggestion.removeprefix(self.new_precommand.replace(' ', '')) + '()'

            write(text_to_add)
            self.interpreter.add_keys_and_update_keys_amount(text_to_add)
            
    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False