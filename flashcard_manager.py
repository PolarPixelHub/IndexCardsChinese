import json
import os
from datetime import datetime, timedelta


class FlashcardManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cards = self.load_cards()

    def load_cards(self):
        """Load cards from the JSON file or initialize an empty list if invalid."""
        if not os.path.exists(self.file_name):
            return []  # If file does not exist, return an empty list

        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                if file.read(1):  # Check if the file has content
                    file.seek(0)  # Reset file pointer to the start
                    return json.load(file)
                else:
                    return []  # Empty file, return an empty list
        except (json.JSONDecodeError, IOError):
            # If file is invalid JSON or unreadable, return empty list
            return []

    def save_cards(self):
        """Save cards to the specified file."""
        with open(self.file_name, "w") as file:
            json.dump(self.cards, file, indent=4)

    def add_card(self, side1, side2):
        """Add a new card."""
        self.cards.append({
            "side1": side1,
            "side2": side2,
            "correct_count": 0,
            "incorrect_count": 0,
            "difficulty_level": "normal",
            "last_correct_time": None,
            "time_periods": 1
        })
        self.save_cards()

    def mark_correct(self, index):
        """Mark card as correct."""
        if 0 <= index < len(self.cards):
            self.cards[index]["correct_count"] += 1
            self.cards[index]["incorrect_count"] = 0
            self.cards[index]["last_correct_time"] = datetime.now().isoformat()
            self.update_difficulty(index)
            self.save_cards()

    def mark_incorrect(self, index):
        """Mark card as incorrect."""
        if 0 <= index < len(self.cards):
            self.cards[index]["incorrect_count"] += 1
            self.cards[index]["correct_count"] = 0
            self.update_difficulty(index)
            self.save_cards()

    def reset_card(self, index):
        self.cards[index]["incorrect_count"] = 0
        self.cards[index]["correct_count"] = 0
        self.update_difficulty(index)
        self.save_cards()

    def update_difficulty(self, index):
        """Update difficulty level based on incorrect count."""
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
        """Delete card."""
        if 0 <= index < len(self.cards):
            del self.cards[index]
            self.save_cards()

