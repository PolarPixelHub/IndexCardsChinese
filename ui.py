import tkinter as tk
from tkinter import messagebox


class FlashcardApp:
    def __init__(self, root, manager):
        self.manager = manager
        self.current_index = -1

        root.title("Flashcard App")
        root.geometry("400x300")

        self.input_side1 = tk.Entry(root, width=40)
        self.input_side1.pack(pady=5)
        self.input_side1.insert(0, "Enter Chinese Character + Pinyin")

        self.input_side2 = tk.Entry(root, width=40)
        self.input_side2.pack(pady=5)
        self.input_side2.insert(0, "Enter English Translation")

        self.add_button = tk.Button(root, text="Add Card", command=self.add_card)
        self.add_button.pack(pady=5)

        self.show_button = tk.Button(root, text="Show Next Card", command=self.show_next_card)
        self.show_button.pack(pady=5)

        self.card_label = tk.Label(root, text="", font=("Arial", 16), wraplength=350)
        self.card_label.pack(pady=20)

        self.flip_button = tk.Button(root, text="Flip Card", command=self.flip_card)
        self.flip_button.pack(pady=5)

        # Add this button to your __init__ method
        self.correct_button = tk.Button(root, text="Mark Correct", command=self.mark_correct)
        self.correct_button.pack(pady=5)

    def add_card(self):
        side1 = self.input_side1.get()
        side2 = self.input_side2.get()
        if side1 and side2:
            self.manager.add_card(side1, side2)
            messagebox.showinfo("Success", "Card Added Successfully!")
            self.input_side1.delete(0, tk.END)
            self.input_side2.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Both fields must be filled.")

    def show_next_card(self):
        # Filter cards where 'correct_count' is less than 10
        filtered_cards = [card for card in self.manager.cards if card["correct_count"] < 10]

        if not filtered_cards:
            messagebox.showinfo("No Cards", "All cards have been guessed correctly 10 times or more!")
            return

        # Cycle through filtered cards
        self.current_index = (self.current_index + 1) % len(filtered_cards)
        self.card_label.config(text=filtered_cards[self.current_index]["side1"])

        # Keep track of the index within the original cards
        self.original_index = self.manager.cards.index(filtered_cards[self.current_index])

    def flip_card(self):
        if self.current_index == -1 or not self.manager.cards:
            messagebox.showerror("Error", "No cards to flip.")
        else:
            card = self.manager.cards[self.current_index]
            current_text = self.card_label.cget("text")
            if current_text == card["side1"]:
                self.card_label.config(text=card["side2"])
            else:
                self.card_label.config(text=card["side1"])

    def mark_correct(self):
        if self.current_index == -1:
            messagebox.showerror("Error", "No card selected.")
        else:
            self.manager.mark_correct(self.original_index)
            count = self.manager.cards[self.original_index]["correct_count"]
            messagebox.showinfo("Correct Guess", f"Correct count: {count}")
