import json
import os


class FlashcardManager:
    def __init__(self, file_name="flashcards.json"):
        self.file_name = file_name
        self.cards = self.load_cards()

    def load_cards(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file)
        return []

    def save_cards(self):
        with open(self.file_name, "w") as file:
            json.dump(self.cards, file)

    def add_card(self, side1, side2):
        self.cards.append({"side1": side1, "side2": side2})
        self.save_cards()
