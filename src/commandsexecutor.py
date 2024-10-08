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