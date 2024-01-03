import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from views import *
from database import Database


class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")

        # SQLite-Datenbankverbindung herstellen
        self.dbcon = Database()
        # self.conn = sqlite3.connect('fitness_tracker.db')
        self.dbcon.create_tables()

        # Views Klasse erstellen
        self.startview = Startview(root)

        # GUI-Elemente erstellen
        self.startview.show()

        # funktionen mappen
        self.map_button_functions()


    def record_workout(self):
        # Eingabewerte vom Benutzer abrufen
        activity = self.startview.workout_entry.get()

        print(activity)

        # Überprüfen, ob die Eingabe nicht leer ist
        if activity == "":
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.startview.message_Label.configure(text='Bitte Training eingeben', foreground='red')
            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Trainingsaktivität in die Datenbank einfügen

        self.dbcon.cursor.execute("INSERT INTO workouts (activity, date) VALUES (?, ?)", (activity, current_date))

        # Meldung anzeigen, dass die Trainingsaktivität erfolgreich aufgezeichnet wurde
        self.startview.message_Label.configure(text=f"Trainingsaktivität '{activity}' erfolgreich aufgezeichnet.",
                                           foreground="green")

        # Eingabefelder leeren
        self.startview.workout_entry.delete(0, tk.END)

    def record_meal(self):
        # Eingabewerte vom Benutzer abrufen
        meal_name = self.startview.meal_entry.get()
        print(meal_name)

        # Überprüfen, ob die Eingabe nicht leer ist
        if not meal_name:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.startview.message_Label.configure(text="Bitte geben Sie den Mahlzeitennamen ein.", foreground="red")

            return

        # Eingabewerte vom Benutzer abrufen
        # calories = self.calories_entry.get()
        calories = 100

        # Überprüfen, ob die Eingabe eine positive Zahl ist
        try:
            calories = int(calories)
            if calories <= 0:
                raise ValueError("Die Kalorienanzahl muss eine positive Zahl sein.")
        except ValueError:
            ttk.Label(self.root, text="Bitte geben Sie eine gültige Kalorienanzahl ein.", foreground="red").grid(row=10,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 pady=10)
            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Mahlzeit in die Datenbank einfügen
        self.dbcon.cursor.execute("INSERT INTO meals (meal_name, calories, date) VALUES (?, ?, ?)",
                           (meal_name, calories, current_date))

        # Meldung anzeigen, dass die Mahlzeit erfolgreich aufgezeichnet wurde
        self.startview.message_Label.configure(
            text=f"Mahlzeit '{meal_name}' mit {calories} Kalorien erfolgreich aufgezeichnet.",
            foreground="green")

        # Eingabefelder leeren
        self.startview.meal_entry.delete(0, tk.END)
        # self.calories_entry.delete(0, tk.END)

    def record_weight(self):
        # Eingabewerte vom Benutzer abrufen
        weight = self.startview.weight_entry.get()

        print(weight)
        # Überprüfen, ob die Eingabe eine positive Zahl ist
        try:
            weight = float(weight)
            if weight <= 0:
                raise ValueError("Das Gewicht muss eine positive Zahl sein.")
        except ValueError:
            self.startview.message_Label.configure(text="Bitte geben Sie eine gültige Gewichtsangabe ein.",
                                               foreground="red")

            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gewichtsverlauf in die Datenbank einfügen
        self.dbcon.cursor.execute("INSERT INTO weight_logs (weight, date) VALUES (?, ?)", (weight, current_date))

        # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
        self.startview.message_Label.configure(text=f"Gewicht {weight} kg erfolgreich aufgezeichnet.", foreground="green")

        # Eingabefelder leeren
        self.startview.weight_entry.delete(0, tk.END)

    def show_workouts(self):
        # Ein Frame erstellen, um Trainingsaktivitäten anzuzeigen
        workouts_frame = ttk.Frame(self.root)
        workouts_frame.grid(row=14, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        ttk.Label(workouts_frame, text="Aktivität").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(workouts_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        # Trainingsaktivitäten aus der Datenbank abrufen
        self.dbcon.cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = self.dbcon.cursor.fetchall()

        # Trainingsaktivitäten im Frame anzeigen
        for index, workout in enumerate(workouts, start=1):
            ttk.Label(workouts_frame, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
            ttk.Label(workouts_frame, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)

    def show_meals(self):
        # Ein Frame erstellen, um Mahlzeiten anzuzeigen
        meals_frame = ttk.Frame(self.root)
        meals_frame.grid(row=15, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        ttk.Label(meals_frame, text="Mahlzeit").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(meals_frame, text="Kalorien").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(meals_frame, text="Datum").grid(row=0, column=2, padx=5, pady=5)

        # Mahlzeiten aus der Datenbank abrufen
        self.dbcon.cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
        meals = self.dbcon.cursor.fetchall()

        # Mahlzeiten im Frame anzeigen
        for index, meal in enumerate(meals, start=1):
            ttk.Label(meals_frame, text=meal[0]).grid(row=index, column=0, padx=5, pady=5)
            ttk.Label(meals_frame, text=meal[1]).grid(row=index, column=1, padx=5, pady=5)
            ttk.Label(meals_frame, text=meal[2]).grid(row=index, column=2, padx=5, pady=5)

    def show_weight_logs(self):
        # Ein Frame erstellen, um den Gewichtsverlauf anzuzeigen
        weight_logs_frame = ttk.Frame(self.root)
        weight_logs_frame.grid(row=16, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        ttk.Label(weight_logs_frame, text="Gewicht (kg)").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(weight_logs_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        # Gewichtsverlauf aus der Datenbank abrufen
        self.dbcon.cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
        weight_logs = self.dbcon.cursor.fetchall()

        # Gewichtsverlauf im Frame anzeigen
        for index, log in enumerate(weight_logs, start=1):
            ttk.Label(weight_logs_frame, text=log[0]).grid(row=index, column=0, padx=5, pady=5)
            ttk.Label(weight_logs_frame, text=log[1]).grid(row=index, column=1, padx=5, pady=5)

    def map_button_functions(self):

        self.startview.show_workout_button.configure(command=self.show_workouts)
        self.startview.show_meal_button.configure(command=self.show_meals)
        self.startview.show_weight_button.configure(command=self.show_weight_logs)

        self.startview.record_workout_button.configure(command=self.record_workout)
        self.startview.record_meal_button.configure(command=self.record_meal)
        self.startview.record_weight_button.configure(command=self.record_weight)


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
