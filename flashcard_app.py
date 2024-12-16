import tkinter as tk
from ui import FlashcardApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)  # No manager passed; it initializes dynamically in the app
    root.mainloop()

