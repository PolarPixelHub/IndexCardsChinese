import json
import os


class FlashcardManager:
    def __init__(self, file_name="flashcards.json", app=None):
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
        self.cards.append(
            {"side1": side1, "side2": side2, "correct_count": 0, "incorrect_count": 0, "difficulty_level": "normal"})
        self.save_cards()

    def mark_correct(self, index):
        if 0 <= index < len(self.cards):
            self.cards[index]["correct_count"] += 1
            self.cards[index]["incorrect_count"] = 0
            self.update_difficulty(index)
            self.save_cards()

    def mark_incorrect(self, index):
        if 0 <= index < len(self.cards):
            self.cards[index]["incorrect_count"] += 1
            self.cards[index]["correct_count"] = 0
            self.update_difficulty(index)
            self.save_cards()

    def update_difficulty(self, index):
        incorrect_count = self.cards[index]["incorrect_count"]
        if incorrect_count >= 10:
            self.cards[index]["difficulty_level"] = "relearn"
        elif incorrect_count >= 5:
            self.cards[index]["difficulty_level"] = "difficult"
        elif incorrect_count >= 3:
            self.cards[index]["difficulty_level"] = "mistakes"
        else:
            self.cards[index]["difficulty_level"] = "normal"

    def delete_card(self, index):
        if 0 <= index < len(self.cards):
            del self.cards[index]
            self.save_cards()
