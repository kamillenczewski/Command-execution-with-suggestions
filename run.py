try:
    from pathlib import Path
    from sys import path
    from os.path import join as combine_path

    path_to_current_dir = str(Path(__file__).parent.resolve())

    path_to_libs = combine_path(path_to_current_dir, 'venv', 'Lib', 'site-packages')

    path.insert(0, path_to_libs)

except Exception as e:
    input(str(e))

from mainloop import MainLoop
from suggestionswindow import MainWindow, ListWidget
from utils import KeyboardDataCollector, DataInterpreter, CommandsExecutor, StorageHandler

from keyboard import write, on_press
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

def show_window(window: MainWindow):
    window.addWindowAction('show')

def hide_window(window: MainWindow):
    window.addWindowAction('hide')

def start_press_event_catcher(method):
    on_press(method)

def start_scroll_event_catcher(method):
    Listener(on_scroll=method).start()

app = QApplication([])
suggestions_window = MainWindow()
list_widget = suggestions_window.getListWidget()

collector = KeyboardDataCollector()
interpreter = DataInterpreter()

storage_handler = StorageHandler()

COMMANDS_AND_METHODS = {
    'get': storage_handler.get,
    'set': storage_handler.set,
    'getall': storage_handler.getall,
    'show': partial(show_window, suggestions_window),
    'hide': partial(hide_window, suggestions_window)
}

MAIN_LOOP_DELAY = 0.1

executor = CommandsExecutor(commands_and_methods=COMMANDS_AND_METHODS)

start_scroll_event_catcher(partial(on_scroll, list_widget))
start_press_event_catcher(collector.collect)

mainLoop = MainLoop(interpreter, collector, executor, list_widget, COMMANDS_AND_METHODS, MAIN_LOOP_DELAY)
loop_thread = Thread(target=mainLoop.start)
loop_thread.start()

suggestions_window.show()
app.exec()
loop_thread.join()