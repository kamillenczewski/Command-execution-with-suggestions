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

        self.current_key = None

    def put_data_generator(self, keyboard_data_generator):
        self.keyboard_data_generator = keyboard_data_generator

    def interprate(self):
        for key in self.keyboard_data_generator:
            # variable 'added' is really ugly here
            # but I tried to solve problem with inserting index

            self.current_key = key
            added = False

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
                        # print('len:', len(self.command_chars), 'index:', self.inserting_index)
                        self.command_chars.pop(self.inserting_index - 1)
                        self.decrease_inserting_index()
                        self.keys_amount_after_command_start -= 1

                    case self.RIGHT if self.inserting_index + 1 <= len(self.command_chars):
                        self.increase_inserting_index()
                        
                    case self.LEFT if self.inserting_index - 1 >= -1:
                        if self.inserting_index - 1 == -1:
                            self.collecting_activity = False
                            self.reset_inserting_index()
                        else:
                            self.decrease_inserting_index()

                            self.add_key(key)
                            self.update_keys_amount(key)
                            added = True
                            
                            self.increase_inserting_index()

                            # print('LEFT')

                if not added:
                    self.add_key(key)
                    self.update_keys_amount(key)

    def increase_inserting_index(self):
        self.inserting_index += 1
        # print('increase', 'index:', self.inserting_index, 'key:', self.current_key, 'chars', self.command_chars)

    def decrease_inserting_index(self):
        self.inserting_index -= 1
        # print('decrease', 'index:', self.inserting_index, 'key:', self.current_key)

    def reset_inserting_index(self):
        self.inserting_index = 0
        # print('reset', 'index:', self.inserting_index, 'key:', self.current_key)

    def add_keys_and_update_keys_amount(self, keys):
        for key in keys:
            self.add_key(key)
            self.update_keys_amount(key)

    def update_keys_amount(self, key):
        if (len(key) == 1 and key != self.COMMAND_START_CHAR) or key in {self.ENTER, self.SPACE}:
            self.keys_amount_after_command_start += 1

    def add_key(self, key):
        if key == self.COMMAND_START_CHAR:
            return

        if key == self.SPACE:
            key = ' '

        if len(key) == 1:
            self.current_key = key
            self.increase_inserting_index()
            self.command_chars.insert(self.inserting_index, key) 

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