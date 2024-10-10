try:
    from pathlib import Path
    from sys import path
    from os.path import join as combine_path

    path_to_current_file = Path(__file__)
    path_to_current_folder = path_to_current_file.parent
    path_to_main_folder = path_to_current_folder.parent

    path_to_libs = combine_path(path_to_main_folder, 'venv', 'Lib', 'site-packages')

    path.insert(0, path_to_libs)
    
except Exception as e:
    input(e)


from mainloop import MainLoop
from listwidget import ListWidget
from mainwindow import MainWindow
from keyboarddatacollector import KeyboardDataCollector
from datainterpreter import DataInterpreter
from commandsexecutor import CommandsExecutor
from storagehandler import StorageHandler
from suggestionsmanager import SuggestionsManager

from keyboard import on_press
from threading import Thread
from PyQt6.QtWidgets import QApplication
from pynput.mouse import Listener
from functools import partial

def on_scroll(list_widget: ListWidget, _1, _2, _3, dy):
    match(dy):
        case 1:
            list_widget.goUp()
        case -1:
            list_widget.goDown()

def activate_window(window: MainWindow):
    window.activate()

def deactivate_window(window: MainWindow):
    window.deactivate()

def start_press_event_catcher(method):
    on_press(method)

def start_scroll_event_catcher(method):
    Listener(on_scroll=method).start()

app = QApplication([])
list_widget = ListWidget()
suggestions_window = MainWindow(list_widget)
list_widget = suggestions_window.getListWidget()

collector = KeyboardDataCollector()
interpreter = DataInterpreter()

storage_handler = StorageHandler()

COMMANDS_AND_METHODS = {
    'get': storage_handler.get,
    'set': storage_handler.set,
    'getall': storage_handler.getall,
    'activate': partial(activate_window, suggestions_window),
    'deactivate': partial(deactivate_window, suggestions_window)
}

MAIN_LOOP_DELAY = 0.1

suggestions_manager = SuggestionsManager(list(COMMANDS_AND_METHODS.keys()))
executor = CommandsExecutor(commands_and_methods=COMMANDS_AND_METHODS)

list_widget.setSuggestionsManager(suggestions_manager)

# start_scroll_event_catcher(partial(on_scroll, list_widget))
start_press_event_catcher(collector.collect)

mainLoop = MainLoop(interpreter, collector, executor, list_widget, suggestions_window, COMMANDS_AND_METHODS, MAIN_LOOP_DELAY)
loop_thread = Thread(target=mainLoop.start)
loop_thread.start()

app.exec()
loop_thread.join()