import tkinter as tk # python 3
from database import Database
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Startview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.weight_entry = tk.Entry(self)


        # Button um User zu erstellen
        self.create_user_button = tk.Button(self, text="User erstellen", command=lambda: controller.show_frame("uv"))

        # Buttons um Werte einzutragen und zu speichern
        self.record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")
        self.record_weight_button = tk.Button(self, text="Gewicht aufzeichnen")

        # Buttons um Werte anzuzeigen
        self.record_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")
        self.show_workout_button = tk.Button(self, text="Trainingsaktivitäten anzeigen")
        self.show_meal_button = tk.Button(self, text="Mahlzeiten anzeigen")
        self.show_weight_button = tk.Button(self, text="Gewichtsverlauf anzeigen")

        # Labels der Erstansicht

        self.name_label = tk.Label(self)

        self.weight_label = tk.Label(self, text="Gewicht (kg):")
        self.message_Label = tk.Label(self, text="lalala")



    def show(self):

        self.cursor.execute("SELECT name FROM user WHERE ID = 1 ")
        name = self.cursor.fetchone()
        print('Name: ' + str(name))

        if not name:
            self.create_user_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        else:
            self.create_user_button.grid_forget()
            self.name_label.configure(text=name)
            self.name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


        # Label für Gewichtsverlauf
        self.weight_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons zum Recorden platzieren
        self.record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.record_weight_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Buttons zum Anzeigen von Daten platzieren
        self.show_workout_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.show_meal_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.show_weight_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)
        self.record_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


class Userview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_entry = tk.Entry(self)
        self.age_entry = tk.Entry(self)
        self.weight_entry = tk.Entry(self)
        self.fl_entry = tk.Entry(self)

        # Labels der Erstansicht
        self.name_label = tk.Label(self, text="Name:")
        self.age_Label = tk.Label(self, text="Alter:")
        self.weight_label = tk.Label(self, text="Gewicht (kg):")
        self.fl_label = tk.Label(self, text="Fitnesslevel:")
        self.create_user_button = tk.Button(self, text="User speichern")

        self.message_Label = tk.Label(self, text="lalala")


    def show(self):
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label für Mahlzeiten
        self.age_Label.grid(row=2, column=0, padx=10, pady=10)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.weight_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.fl_label.grid(row=4, column=0, padx=10, pady=10)
        self.fl_entry.grid(row=4, column=1, padx=10, pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

        # Buttons zum Aufzeichnen von Daten
        self.create_user_button.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)



class Trainingview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.activity_label = tk.Label(self, text="Aktivität")
        self.date_label = tk.Label(self, text="Datum")
        self.calories_label = tk.Label(self, text="Kalorien")


    def show(self):
        # Ein Label für die Spaltenüberschriften
        self.activity_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_label.grid(row=0, column=1, padx=5, pady=5)
        self.calories_label.grid(row=0, column=2, padx=5, pady=5)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
            workouts = cursor.fetchall()
            print('Workouts' + str(workouts))

        for index, workout in enumerate(workouts, start=1):
            tk.Label(self, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
            tk.Label(self, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)
            tk.Label(self, text=workout[2]).grid(row=index, column=1, padx=5, pady=5)



class Trainingrecordview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        OPTIONS = [
            "Running",
            "Jogging",
            "Walking",
            "Swimming",
            "Cycling",
            "Basketball",
            "Soccer",
            "Tennis",
            "Boxing",
            "Yoga",
            "Pilates",
            "Weightlifting"
        ]

        self.training_label = tk.Label(self, text="Trainingsaktivität:")
        self.workout_entry = ttk.Combobox(self, state="readonly", values=OPTIONS)
        self.message_Label = tk.Label(self, text="lalala")
        self.safe_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")

    def show(self):
        self.training_label.grid(row=1, column=0, padx=10, pady=10)
        self.workout_entry.grid(row=1, column=1, padx=10, pady=10)
        self.safe_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)


class Mealview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Ein Label für die Spaltenüberschriften
        self.meal_label = tk.Label( self, text="Mahlzeit")
        self.calory_label = tk.Label(self,text="Kalorien")
        self.date_label = tk.Label(self, text="Datum")

    def show(self):
        # Label für Mahlzeiten

        self.meal_label.grid(row=0, column=0, padx=5, pady=5)
        self.calory_label.grid(row=0, column=1, padx=5, pady=5)
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
            meals = cursor.fetchall()
            print('Meals ' + str(meals))

        # Mahlzeiten im Frame anzeigen
        for index, meal in enumerate(meals, start=1):
            tk.Label(self, text=meal[0]).grid(row=index, column=0, padx=5, pady=5)
            tk.Label(self, text=meal[1]).grid(row=index, column=1, padx=5, pady=5)
            tk.Label(self, text=meal[2]).grid(row=index, column=2, padx=5, pady=5)


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)



class Mealrecordview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.meal_entry = tk.Entry(self)
        self.meal_Label = tk.Label(self, text="Mahlzeit:")
        self.message_Label = tk.Label(self, text="lalala")
        self.record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")



    def show(self):

        self.meal_Label.grid(row=2, column=0, padx=10, pady=10)
        self.meal_entry.grid(row=2, column=1, padx=10, pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)
        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)
        self.record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


class Weightview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.zielgewicht = 70  # Hier das gewünschte Zielgewicht eintragen

    def show(self):
        # Ein Frame erstellen, um den Gewichtsverlauf anzuzeigen
        # neues_fenster = tk.Toplevel(self.controller.container)
        # weight_logs_frame = tk.Frame(neues_fenster)
        # weight_logs_frame.grid(row=16, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        tk.Label(self, text="Gewicht (kg)").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

        # Gewichtsverlauf aus der Datenbank abrufen
        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            weight_logs = cursor.fetchall()
            print('Gewichtsverlauf' + str(weight_logs))

        # Gewichtsverlauf im Frame anzeigen
        for index, log in enumerate(weight_logs, start=1):
            tk.Label(self, text=log[0]).grid(row=index, column=0, padx=5, pady=5)
            tk.Label(self, text=log[1]).grid(row=index, column=1, padx=5, pady=5)

        # Zielgewichtslinie hinzufügen
        plt.axhline(y=self.zielgewicht, color='green', linestyle='--', label='Zielgewicht')

        # Gewichtsverlauf als roten Graphen anzeigen
        weights = [log[0] for log in weight_logs]
        dates = [log[1] for log in weight_logs]

        fig, ax = plt.subplots()
        ax.plot(dates, weights, color='red', marker='o', label='Werte')
        ax.set_title('Gewichtsverlauf')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Gewicht (kg)')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=16, column=2, padx=10, pady=10)

        canvas.draw()