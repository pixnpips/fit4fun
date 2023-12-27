import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")

        # SQLite-Datenbankverbindung herstellen
        self.conn = sqlite3.connect('fitness_tracker.db')
        self.create_tables()

        # GUI-Elemente erstellen
        self.create_widgets()

    def create_tables(self):
        # Erstellen von Tabellen, falls noch nicht existieren
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT,
                    duration INTEGER,
                    date TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_name TEXT,
                    calories INTEGER,
                    date TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weight_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weight REAL,
                    date TEXT
                )
            ''')

    def create_widgets(self):
    # Label für Trainingsaktivitäten
    ttk.Label(self.root, text="Trainingsaktivität:").grid(row=0, column=0, padx=10, pady=10)
    self.workout_entry = ttk.Entry(self.root)
    self.workout_entry.grid(row=0, column=1, padx=10, pady=10)

    # Label für Mahlzeiten
    ttk.Label(self.root, text="Mahlzeit:").grid(row=1, column=0, padx=10, pady=10)
    self.meal_entry = ttk.Entry(self.root)
    self.meal_entry.grid(row=1, column=1, padx=10, pady=10)

    # Label für Gewichtsverlauf
    ttk.Label(self.root, text="Gewicht (kg):").grid(row=2, column=0, padx=10, pady=10)
    self.weight_entry = ttk.Entry(self.root)
    self.weight_entry.grid(row=2, column=1, padx=10, pady=10)

    # Buttons zum Aufzeichnen von Daten
    ttk.Button(self.root, text="Trainingsaktivität aufzeichnen", command=self.record_workout).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(self.root, text="Mahlzeit aufzeichnen", command=self.record_meal).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(self.root, text="Gewicht aufzeichnen", command=self.record_weight).grid(row=5, column=0, columnspan=2, pady=10)

    # Buttons zum Anzeigen von Daten
    ttk.Button(self.root, text="Trainingsaktivitäten anzeigen", command=self.show_workouts).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(self.root, text="Mahlzeiten anzeigen", command=self.show_meals).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(self.root, text="Gewichtsverlauf anzeigen", command=self.show_weight_logs).grid(row=8, column=0, columnspan=2, pady=10)


    def record_workout(self):
    # Eingabewerte vom Benutzer abrufen
    activity = self.workout_entry.get()

    # Überprüfen, ob die Eingabe nicht leer ist
    if not activity:
        # Zeige eine Meldung an, dass das Feld nicht leer sein darf
        ttk.Label(self.root, text="Bitte geben Sie die Trainingsaktivität ein.", foreground="red").grid(row=9, column=0, columnspan=2, pady=10)
        return

    # Aktuelles Datum und Uhrzeit abrufen
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Trainingsaktivität in die Datenbank einfügen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO workouts (activity, date) VALUES (?, ?)", (activity, current_date))

    # Meldung anzeigen, dass die Trainingsaktivität erfolgreich aufgezeichnet wurde
    ttk.Label(self.root, text=f"Trainingsaktivität '{activity}' erfolgreich aufgezeichnet.", foreground="green").grid(row=9, column=0, columnspan=2, pady=10)

    # Eingabefelder leeren
    self.workout_entry.delete(0, tk.END)


 def record_meal(self):
    # Eingabewerte vom Benutzer abrufen
    meal_name = self.meal_entry.get()

    # Überprüfen, ob die Eingabe nicht leer ist
    if not meal_name:
        # Zeige eine Meldung an, dass das Feld nicht leer sein darf
        ttk.Label(self.root, text="Bitte geben Sie den Mahlzeitennamen ein.", foreground="red").grid(row=10, column=0, columnspan=2, pady=10)
        return

    # Eingabewerte vom Benutzer abrufen
    calories = self.calories_entry.get()

    # Überprüfen, ob die Eingabe eine positive Zahl ist
    try:
        calories = float(calories)
        if calories <= 0:
            raise ValueError("Die Kalorienanzahl muss eine positive Zahl sein.")
    except ValueError:
        ttk.Label(self.root, text="Bitte geben Sie eine gültige Kalorienanzahl ein.", foreground="red").grid(row=11, column=0, columnspan=2, pady=10)
        return

    # Aktuelles Datum und Uhrzeit abrufen
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Mahlzeit in die Datenbank einfügen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO meals (meal_name, calories, date) VALUES (?, ?, ?)", (meal_name, calories, current_date))

    # Meldung anzeigen, dass die Mahlzeit erfolgreich aufgezeichnet wurde
    ttk.Label(self.root, text=f"Mahlzeit '{meal_name}' mit {calories} Kalorien erfolgreich aufgezeichnet.", foreground="green").grid(row=11, column=0, columnspan=2, pady=10)

    # Eingabefelder leeren
    self.meal_entry.delete(0, tk.END)
    self.calories_entry.delete(0, tk.END)

   def record_weight(self):
    # Eingabewerte vom Benutzer abrufen
    weight = self.weight_entry.get()

    # Überprüfen, ob die Eingabe eine positive Zahl ist
    try:
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Das Gewicht muss eine positive Zahl sein.")
    except ValueError:
        ttk.Label(self.root, text="Bitte geben Sie eine gültige Gewichtsangabe ein.", foreground="red").grid(row=12, column=0, columnspan=2, pady=10)
        return

    # Aktuelles Datum und Uhrzeit abrufen
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Gewichtsverlauf in die Datenbank einfügen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO weight_logs (weight, date) VALUES (?, ?)", (weight, current_date))

    # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
    ttk.Label(self.root, text=f"Gewicht {weight} kg erfolgreich aufgezeichnet.", foreground="green").grid(row=12, column=0, columnspan=2, pady=10)

    # Eingabefelder leeren
    self.weight_entry.delete(0, tk.END)


    def show_workouts(self):
    # Ein Frame erstellen, um Trainingsaktivitäten anzuzeigen
    workouts_frame = ttk.Frame(self.root)
    workouts_frame.grid(row=13, column=0, columnspan=2, pady=10)

    # Ein Label für die Spaltenüberschriften
    ttk.Label(workouts_frame, text="Aktivität").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(workouts_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

    # Trainingsaktivitäten aus der Datenbank abrufen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = cursor.fetchall()

    # Trainingsaktivitäten im Frame anzeigen
    for index, workout in enumerate(workouts, start=1):
        ttk.Label(workouts_frame, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
        ttk.Label(workouts_frame, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)


    def show_meals(self):
    # Ein Frame erstellen, um Mahlzeiten anzuzeigen
    meals_frame = ttk.Frame(self.root)
    meals_frame.grid(row=14, column=0, columnspan=2, pady=10)

    # Ein Label für die Spaltenüberschriften
    ttk.Label(meals_frame, text="Mahlzeit").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(meals_frame, text="Kalorien").grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(meals_frame, text="Datum").grid(row=0, column=2, padx=5, pady=5)

    # Mahlzeiten aus der Datenbank abrufen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
        meals = cursor.fetchall()

    # Mahlzeiten im Frame anzeigen
    for index, meal in enumerate(meals, start=1):
        ttk.Label(meals_frame, text=meal[0]).grid(row=index, column=0, padx=5, pady=5)
        ttk.Label(meals_frame, text=meal[1]).grid(row=index, column=1, padx=5, pady=5)
        ttk.Label(meals_frame, text=meal[2]).grid(row=index, column=2, padx=5, pady=5)


    def show_weight_logs(self):
    # Ein Frame erstellen, um den Gewichtsverlauf anzuzeigen
    weight_logs_frame = ttk.Frame(self.root)
    weight_logs_frame.grid(row=15, column=0, columnspan=2, pady=10)

    # Ein Label für die Spaltenüberschriften
    ttk.Label(weight_logs_frame, text="Gewicht (kg)").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(weight_logs_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

    # Gewichtsverlauf aus der Datenbank abrufen
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
        weight_logs = cursor.fetchall()

    # Gewichtsverlauf im Frame anzeigen
    for index, log in enumerate(weight_logs, start=1):
        ttk.Label(weight_logs_frame, text=log[0]).grid(row=index, column=0, padx=5, pady=5)
        ttk.Label(weight_logs_frame, text=log[1]).grid(row=index, column=1, padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
