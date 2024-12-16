import tkinter as tk
from flashcard_manager import FlashcardManager
from ui import FlashcardApp

if __name__ == "__main__":
    manager = FlashcardManager()  # Initialize the manager
    root = tk.Tk()
    app = FlashcardApp(root, manager)
    root.mainloop()
