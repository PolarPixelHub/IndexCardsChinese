import tkinter as tk
from tkinter import messagebox
from flashcard_manager import FlashcardManager

class FlashcardApp:
    def __init__(self, root, manager):
        self.manager = manager
        self.current_index = -1
        self.root = root
        root.title("Flashcard App")
        root.geometry("400x300")

        self.show_start_options(root)

    def show_start_options(self, root):
        start_frame = tk.Frame(root)
        start_frame.pack(pady=50)

        add_card_button = tk.Button(start_frame, text="Add Card", command=self.show_add_card_window)
        add_card_button.pack(pady=10)

        learn_button = tk.Button(start_frame, text="Learn", command=self.show_learn_window)
        learn_button.pack(pady=10)

    def show_add_card_window(self):
        add_window = tk.Toplevel()
        add_window.title("Add Card")
        add_window.geometry("400x300")

        self.input_side1 = tk.Entry(add_window, width=40)
        self.input_side1.pack(pady=5)
        self.input_side1.insert(0, "Enter Chinese Character + Pinyin")

        self.input_side2 = tk.Entry(add_window, width=40)
        self.input_side2.pack(pady=5)
        self.input_side2.insert(0, "Enter English Translation")

        add_button = tk.Button(add_window, text="Add Card", command=self.add_card)
        add_button.pack(pady=5)

    def show_learn_window(self):
        learn_window = tk.Toplevel()
        learn_window.title("Learn")
        learn_window.geometry("400x300")

        self.card_label = tk.Label(learn_window, text="", font=("Arial", 16), wraplength=350)
        self.card_label.pack(pady=20)

        self.flip_button = tk.Button(learn_window, text="Flip Card", command=self.flip_card)
        self.flip_button.pack(pady=5)

        self.correct_button = tk.Button(learn_window, text="Mark Correct", command=self.mark_correct)
        self.correct_button.pack(pady=5)

        self.incorrect_button = tk.Button(learn_window, text="Mark Incorrect", command=self.mark_incorrect)
        self.incorrect_button.pack(pady=5)

        self.show_button = tk.Button(learn_window, text="Show Next Card", command=self.show_next_card)
        self.show_button.pack(pady=5)

        self.delete_window_button = tk.Button(learn_window, text="Manage Cards", command=self.open_delete_window)
        self.delete_window_button.pack(pady=5)

        self.current_index = -1
        self.show_next_card()

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
        filtered_cards = [card for card in self.manager.cards if card["correct_count"] < 10]

        if not filtered_cards:
            messagebox.showinfo("No Cards", "All cards have been guessed correctly 10 times or more!")
            return

        self.current_index = (self.current_index + 1) % len(filtered_cards)
        card = filtered_cards[self.current_index]
        self.card_label.config(text=f"{card['side1']} ({card['difficulty_level']})")

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
            self.manager.mark_correct(self.current_index)
            self.show_next_card()

    def mark_incorrect(self):
        if self.current_index == -1:
            messagebox.showerror("Error", "No card selected.")
        else:
            self.manager.mark_incorrect(self.current_index)
            self.show_next_card()

    def open_delete_window(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete a Card")
        delete_window.geometry("1000x600")

        card_listbox = tk.Listbox(delete_window, width=100, height=25)
        card_listbox.pack(pady=10)

        for i, card in enumerate(self.manager.cards):
            card_listbox.insert(tk.END, f"{i + 1}: {card['side1']} - {card['side2']} (Count: {card['correct_count']}, Difficulty: {card['difficulty_level']})")

        def delete_selected():
            selected_index = card_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                self.manager.delete_card(index)
                delete_window.destroy()
                messagebox.showinfo("Deleted", "Card deleted successfully.")
            else:
                messagebox.showerror("Error", "No card selected.")

        delete_button = tk.Button(delete_window, text="Delete Selected Card", command=delete_selected)
        delete_button.pack(pady=5)