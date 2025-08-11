import tkinter as tk
from controller import QuizController

def main():
    root = tk.Tk()
    root.title("Loblaws PLU Quiz")
    root.geometry("520x420")  # width x height
    root.resizable(False, False)

    app = QuizController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
