import tkinter as tk
from models.database import Database

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trainings- und Ernährungs-Tracker")
        self.geometry("800x600")

        self.database = Database()

        # GUI-Elemente hier erstellen und verknüpfen
