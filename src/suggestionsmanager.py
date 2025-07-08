class SuggestionsManager:
    def __init__(self, commands_and_methods) -> None:
        self.commands_and_methods = commands_and_methods
        self.suggestions = []
        self.precommand = None

    def set_precommand(self, precommand):
        self.precommand = precommand
        self.update_suggestions()

    def update_suggestions(self):
        self.suggestions = list(self.find_similar_command_to_precommand())

    def find_similar_command_to_precommand(self):
        for command_name in self.get_possible_commands():
            if command_name.startswith(self.precommand) or self.precommand.startswith(command_name):
                yield command_name

    def get_possible_commands(self):
        return self.commands_and_methods.keys()

    def best(self):
        if self.suggestions:
            return self.suggestions[0]

    def all(self):
        if self.suggestions:
            return self.suggestions