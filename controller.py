import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from logic import QuizLogic


class QuizController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = QuizLogic()

        # Top frame: label + image
        top_frame = ttk.Frame(root, padding=(10, 10))
        top_frame.pack(side="top", fill="both", expand=False)

        self.item_lbl = ttk.Label(top_frame, text="Item Name", font=("Segoe UI", 18))
        self.item_lbl.pack(side="top", pady=(0, 8))

        # Image placeholder label
        self.item_img_lbl = ttk.Label(top_frame)
        self.item_img_lbl.pack(side="top")

        # Bottom frame: create 4 vertical areas (button over label) arranged horizontally
        bottom_frame = ttk.Frame(root, padding=(10, 10))
        bottom_frame.pack(side="top", fill="x")

        # Store per-button widgets and text variables
        self.button_frames = []
        self.buttons = []
        self.btn_text_vars = []
        self.btn_labels = []  # labels that reveal item names after press
        self.default_btn_bg = tk.Button().cget("bg")  # store default system bg

        for i in range(4):
            frame = ttk.Frame(bottom_frame)
            frame.pack(side="left", padx=8, pady=6)
            var = tk.StringVar(value=f"Option {i+1}")
            btn = tk.Button(frame, textvariable=var, width=14, command=lambda idx=i: self.on_button_click(idx))
            btn.pack(side="top")
            lbl = ttk.Label(frame, text="", font=("Segoe UI", 9))
            lbl.pack(side="top", pady=(6, 0))  # initially empty/invisible
            self.button_frames.append(frame)
            self.buttons.append(btn)
            self.btn_text_vars.append(var)
            self.btn_labels.append(lbl)

        # Internal state
        self.current_correct_value = None
        self.current_correct_key = None
        self.current_photo = None  # keep reference to avoid GC
        self.current_options = []  # list of tuples (value_str, key)
        self.loading_new = False

        # Start first question
        self.new_question()

    def new_question(self):
        """Load a new randomized question and update the GUI."""
        try:
            key, correct_value, options, pil_img = self.logic.randomize_quiz()
        except Exception as e:
            self.item_lbl.config(text="Error: " + str(e))
            return

        self.current_correct_key = key
        self.current_correct_value = correct_value
        self.current_options = options  # list of (value_str, key)

        # Update label
        self.item_lbl.config(text=key.title())

        # Convert PIL image to PhotoImage and attach:
        self.current_photo = ImageTk.PhotoImage(pil_img)
        self.item_img_lbl.config(image=self.current_photo)

        # Update buttons and hide per-button labels
        for i, (val, k) in enumerate(self.current_options):
            self.btn_text_vars[i].set(str(val))
            self.buttons[i].config(bg=self.default_btn_bg, state="normal")
            self.btn_labels[i].config(text="")  # hide text until button pressed

        self.loading_new = False

    def on_button_click(self, index: int):
        """Handle when a choice button is pressed."""
        if self.loading_new:
            return  # ignore clicks while transition

        selected_value = self.btn_text_vars[index].get()
        button = self.buttons[index]
        # reveal this button's label (the item name for that value)
        try:
            corresponding_key = self.current_options[index][1]
        except Exception:
            corresponding_key = ""
        self.btn_labels[index].config(text=corresponding_key.title())

        if self.logic.is_correct(self.current_correct_value, selected_value):
            # Correct: green, disable all, then after delay -> next question
            button.config(bg="green")
            for b in self.buttons:
                b.config(state="disabled")
            self.loading_new = True
            # after 1200ms, reset and load next
            self.root.after(1200, self.new_question)
        else:
            # Wrong: mark this button red and disable it (user must find correct)
            button.config(bg="red", state="disabled")
            # keep others enabled so user can try again
