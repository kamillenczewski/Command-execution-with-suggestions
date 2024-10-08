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