import tkinter as tk # python 3
from database import Database
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from user_meal_activity_weight import *
from tkinter.scrolledtext import ScrolledText
import os.path

class Startview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Database Connection
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, 'fitness_tracker.db')
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.title = "Fit4Fun"

        # Labels für User, Weight
        self.create_user_button = tk.Button(self, text="User erstellen", command=lambda: controller.show_frame("uv"))
        self.record_weight_button = tk.Button(self, text="Gewicht aufzeichnen")
        self.show_weight_button = tk.Button(self, text="Gewichtsverlauf anzeigen")

        # Mahlzeit Area
        self.record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")
        self.meals_label = tk.Label(self, text="letzte Mahlzeiten", font=('Helvetica', 14, 'bold'))
        self.show_meal_button = tk.Button(self, text="Alle Mahlzeiten anzeigen")

        # Trainings Area
        self.record_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")
        self.workout_label = tk.Label(self, text="letzte Trainingsaktivitäten", font=('Helvetica', 14, 'bold'))
        self.show_workout_button = tk.Button(self, text="Alle Trainingsaktivitäten anzeigen")

        # Labels der Erstansicht
        self.name_label = tk.Label(self)
        self.weight_label = tk.Label(self, text="Aktuelles Gewicht (kg):")
        self.message_Label = tk.Label(self, text="")
        self.target_weight_label = tk.Label(self, text="Zielgewicht")
        self.separator_hor = ttk.Separator(self, orient='horizontal')
        self.separator_ver = ttk.Separator(self, orient='vertical')

        #Labels der Anzeige der letzten Daten
        self.show_meals = []
        self.show_meal_dates = []

        self.show_weight_label = self.show_target_weight_label = tk.Label(self, text="")
        self.show_target_weight_label = tk.Label(self, text="")

        self.show_meal_label_1 = tk.Label(self, text="")
        self.show_meal_date_label_1 = tk.Label(self, text="")

        self.show_meal_label_2 = tk.Label(self, text="")
        self.show_meal_date_label_2 = tk.Label(self, text="")

        self.show_meal_label_3 = tk.Label(self, text="")
        self.show_meal_date_label_3 = tk.Label(self, text="")

        for i in self.show_meal_label_1, self.show_meal_label_2, self.show_meal_label_3:
            self.show_meals.append(i)

        for i in self.show_meal_date_label_1, self.show_meal_date_label_2, self.show_meal_date_label_3:
            self.show_meal_dates.append(i)

        self.show_workouts = []
        self.show_workout_dates = []

        self.show_workout_label_1 = tk.Label(self, text="")
        self.show_workout_date_label_1 = tk.Label(self, text="")

        self.show_workout_label_2 = tk.Label(self, text="")
        self.show_workout_date_label_2 = tk.Label(self, text="")

        self.show_workout_label_3 = tk.Label(self, text="")
        self.show_workout_date_label_3 = tk.Label(self, text="")

        for i in self.show_workout_label_1, self.show_workout_label_2, self.show_workout_label_3:
            self.show_workouts.append(i)

        for i in self.show_workout_date_label_1, self.show_workout_date_label_2, self.show_workout_date_label_3:
            self.show_workout_dates.append(i)


    def show(self):

        # Anpassung Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Grid Positionierungen

        with sqlite3.connect(self.db_path) as db:
            self.cursor.execute("SELECT name FROM user")
            names = self.cursor.fetchall()
            print('Alle User: ' + str(names))

            if len(names) == 0:
                self.create_user_button.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
            else:
                self.create_user_button.grid_forget()
                self.name_label.configure(text=names[0], font=('Helvetica', 18, 'bold'))
                self.name_label.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

            # Label für Gewichtsverlauf
            self.weight_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
            self.show_weight_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            self.record_weight_button.grid(row=1, column=3, columnspan=2, padx=10, pady=20)
            self.show_weight_button.grid(row=2, column=3, columnspan=2, padx=10, pady=20)

            self.cursor.execute("SELECT weight FROM weight_logs ORDER BY date DESC ")
            weights = self.cursor.fetchall()
            print('Alle Weights' + str(weights))

            if len(weights)!=0:
                self.show_weight_label.configure(text=weights[0])

            # Labels für Trainingsaktivitäten
            self.record_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
            self.show_workout_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)
            self.workout_label.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

            self.cursor.execute("SELECT date, activity FROM workouts ORDER BY date DESC")
            workouts = self.cursor.fetchall()
            print('Alle Workouts' + str(workouts))

            if len(workouts) > 3:
                objects = workouts[:3]
                for index, object in enumerate(objects, start=0):
                    self.show_workout_dates[index].configure(text=object[0])
                    self.show_workout_dates[index].grid(row=index + 7, column=0, padx=5, pady=5)
                    self.show_workouts[index].configure(text=object[1])
                    self.show_workouts[index].grid(row=index + 7, column=1, padx=5, pady=5)
                    ttk.Separator(self, orient='vertical').grid(row=index + 7, column=2, rowspan=2, sticky='ns')

            else:
                for index, workout in enumerate(workouts, start=0):
                    self.show_workout_dates[index].configure(text=workout[0])
                    self.show_workout_dates[index].grid(row=index+7, column=0, padx=5, pady=5)
                    self.show_workouts[index].configure(text=workout[1])
                    self.show_workouts[index].grid(row=index+7, column=1, padx=5, pady=5)
                    ttk.Separator(self, orient='vertical').grid(row=index + 7, column=2, rowspan=2, sticky='ns')

            # Labels für Mahlzeiten
            self.record_meal_button.grid(row=4, column=3, columnspan=2, padx=10, pady=20)
            self.show_meal_button.grid(row=5, column=3, columnspan=2, padx=10, pady=20)
            self.meals_label.grid(row=6, column=3, columnspan=2, padx=10, pady=20)

            self.cursor.execute("SELECT date, meal_name FROM meals ORDER BY date DESC")
            meals = self.cursor.fetchall()
            print('Alle Meals' + str(meals))

            if len(meals)>3:
                objects = meals[:3]
                for index, object in enumerate(objects, start=0):
                    self.show_meals[index].configure(text=object[1])
                    self.show_meals[index].grid(row=index + 7, column=3, padx=5, pady=5)
                    self.show_meal_dates[index].configure(text=object[0])
                    self.show_meal_dates[index].grid(row=index + 7, column=4, padx=5, pady=5)
                    ttk.Separator(self, orient='vertical').grid(row=index + 7, column=2, rowspan=2, sticky='ns')
            else:
                for index, meal in enumerate(meals, start=0):
                    self.show_meals[index].configure(text = meal[1])
                    self.show_meals[index].grid(row=index + 7, column=3, padx=5, pady=5)
                    self.show_meal_dates[index].configure(text=meal[0])
                    self.show_meal_dates[index].grid(row=index + 7, column=4, padx=5, pady=5)
                    ttk.Separator(self, orient='vertical').grid(row=index + 7, column=2, rowspan=2, sticky='ns')

            # Message Label
            self.message_Label.grid(row=21, column=0, columnspan=5, pady=20)
            # Styling
            self.separator_hor.grid(row=3, column=0, columnspan=5, sticky='ew')
            self.separator_ver.grid(row=3, column=2, rowspan=10, sticky='ns')




class Userview(tk.Frame):

    # Funktion zur Validierung
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        is_number = (self.register(self.callback))
        self.title = "User erstellen"

        # Eingabefelder
        self.name_entry = tk.Entry(self)
        self.age_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.weight_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.fl_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))

        # Labels für die Eingabefelder
        self.name_label = tk.Label(self, text="Name:")
        self.age_Label = tk.Label(self, text="Alter:")
        self.weight_label = tk.Label(self, text="Gewicht (kg):")
        self.fl_label = tk.Label(self, text="Fitnesslevel:")

        self.create_user_button = tk.Button(self, text="Speichern")
        self.message_Label = tk.Label(self, text="")

        self.separator = ttk.Separator(self, orient='horizontal')


    def show(self):
        # Anpassung Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Positionierung im Grid
        self.name_label.grid(row=2, column=0, padx=10, pady=10)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10)

        self.age_Label.grid(row=3, column=0, padx=10, pady=10)
        self.age_entry.grid(row=3, column=1, padx=10, pady=10)

        self.weight_label.grid(row=4, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=4, column=1, padx=10, pady=10)

        self.fl_label.grid(row=5, column=0, padx=10, pady=10)
        self.fl_entry.grid(row=5, column=1, padx=10, pady=10)

        # Button zum Speichern von Daten
        self.create_user_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)


class Trainingview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.title = "Trainingsaktivitäten"
        self.activity_label = tk.Label(self, text="Aktivität", font=('Helvetica', 14, 'bold'))
        self.date_label = tk.Label(self, text="Datum", font=('Helvetica', 14, 'bold'))
        self.calories_label = tk.Label(self, text="Kalorien", font=('Helvetica', 14, 'bold'))

        self.separator = ttk.Separator(self, orient='horizontal')

    def show(self):

        # Zeilen löschen
        for i in self.grid_slaves():
            i.grid_forget()

        # Anpassung Grid

        self.grid_rowconfigure(0, minsize=40)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.separator.grid(row=1, columnspan=3, sticky="ew")

        # Labels für die Spaltenüberschriften
        self.activity_label.grid(row=0, column=0, padx=5, pady=5)
        self.calories_label.grid(row=0, column=1, padx=5, pady=5)
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT activity, calories, date FROM workouts ORDER BY date DESC")
            workouts = cursor.fetchall()
            print('Workouts' + str(workouts))

        # ScrolledText-Widget für Trainingsaktivitäten mit doppelter Höhe und Helvetica 14
        text_widget = ScrolledText(self, wrap=tk.WORD, width=40, height=20, font=('Helvetica', 10))
        text_widget.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Trainingsaktivitäten im Text-Widget anzeigen
        for workout in workouts:
            text_widget.insert(tk.END, f" \t\t{workout[0]}\t\t\t\t\t\t\tKalorien: {workout[1]}\t\t\t\t\t\tDatum: {workout[2]}\n")

class Trainingrecordview(tk.Frame):

    # Funktion zur Nummer-Validierung
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()
        is_number = (self.register(self.callback))

        # Optionen für Dropdown Menü
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

        self.title = "Training speichern"

        # Labels initialisieren
        self.training_label = tk.Label(self, text="Trainingsaktivität:")
        self.workout_entry = ttk.Combobox(self, state="readonly", values=OPTIONS)
        self.duration_label = tk.Label(self, text="Minuten:")
        self.duration_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.message_Label = tk.Label(self, text="")
        self.safe_workout_button = tk.Button(self, text="Speichern")

    def show(self):
        # Eingabefelder zurücksetzen
        self.reset()

        # Anpassung Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Positionierung im Grid

        self.training_label.grid(row=2, column=0, padx=10, pady=10)
        self.workout_entry.grid(row=2, column=1, padx=10, pady=10)
        self.duration_label.grid(row=3, column=0, padx=10, pady=10)
        self.duration_entry.grid(row=3, column=1, padx=10, pady=10)
        self.safe_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=5, column=0, columnspan=2, pady=10)
        self.message_Label.configure(text="")
        self.duration_entry.delete(0, 'end')
        self.workout_entry.set('')

    def reset(self):

        self.duration_entry.delete(0, 100)

        self.workout_entry.current(0)

        self.message_Label.configure(text='')

class Mealview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.title = "Mahlzeiten"
        self.separator = ttk.Separator(self, orient='horizontal')

        # Ein Label für die Spaltenüberschriften
        self.meal_label = tk.Label(self, text="Mahlzeit", font=('Helvetica', 14, 'bold'))
        self.calory_label = tk.Label(self, text="Kalorien", font=('Helvetica', 14, 'bold'))
        self.date_label = tk.Label(self, text="Datum", font=('Helvetica', 14, 'bold'))

    def show(self):

        # Zeilen löschen
        for i in self.grid_slaves():
            i.grid_forget()

        # Anpassung Grid

        self.grid_rowconfigure(0, minsize=40)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.separator.grid(row=1, columnspan=3, sticky="ew")

        # Labels für die Spaltenüberschriften
        self.meal_label.grid(row=0, column=0, padx=5, pady=5)
        self.calory_label.grid(row=0, column=1, padx=5, pady=5)
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
            meals = cursor.fetchall()
            print('Meals ' + str(meals))

        # ScrolledText-Widget für Mahlzeiten mit doppelter Höhe
        text_widget = ScrolledText(self, wrap=tk.WORD, width=40, height=20, font=('Helvetica', 10))
        text_widget.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Mahlzeiten im Text-Widget anzeigen
        for meal in meals:
            text_widget.insert(tk.END, f"\t\t {meal[0]} \t\t\t\t\t\t\t\t {meal[1]} \t\t\t\t\t {meal[2]}\n")

class Mealrecordview(tk.Frame):

    # Funktion zur Nummer-Validierung
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()
        self.title = "Mahlzeit speichern"

        is_number = (self.register(self.callback))
        self.separator = ttk.Separator(self, orient='horizontal')

        self.first_label = tk.Label(self, text="Hauptgericht:")
        self.second_label = tk.Label(self, text="Beilage:")
        self.drink_label = tk.Label(self, text="Getränk:")

        # Dropdown-Menü erstellen

        self.first_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.first], state="readonly")
        self.first_combo.current(0)

        self.second_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.second], state="readonly")
        self.second_combo.current(0)

        self.drink_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.drink], state="readonly")
        self.drink_combo.current(0)

        self.first_x_label = tk.Label(self, text="Menge (in g):")
        self.second_x_label = tk.Label(self, text="Menge (in g):")
        self.drink_x_label = tk.Label(self, text="Menge(in g):")

        self.first_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.first_x_entry.insert(0, '0')

        self.second_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.second_x_entry.insert(0, '0')

        self.drink_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.drink_x_entry.insert(0, '0')

        self.message_Label = tk.Label(self, text="")
        self.record_meal_button = tk.Button(self, text="Speichern")

    def show(self):
        # Eingabefelder zurücksetzen
        self.reset()

        # Anpassung Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Positionierung im Grid

        self.first_label.grid(row=2, column=0, padx=10, pady=10)
        self.first_combo.grid(row=2, column=1, padx=10, pady=10)
        self.first_x_label.grid(row=3, column=0, padx=10, pady=10)
        self.first_x_entry.grid(row=3, column=1, padx=10, pady=10)

        self.second_label.grid(row=4, column=0, padx=10, pady=10)
        self.second_combo.grid(row=4, column=1, padx=10, pady=10)
        self.second_x_label.grid(row=5, column=0, padx=10, pady=10)
        self.second_x_entry.grid(row=5, column=1, padx=10, pady=10)

        self.drink_label.grid(row=6, column=0, padx=10, pady=10)
        self.drink_combo.grid(row=6, column=1, padx=10, pady=10)
        self.drink_x_label.grid(row=7, column=0, padx=10, pady=10)
        self.drink_x_entry.grid(row=7, column=1, padx=10, pady=10)

        self.record_meal_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)

    def reset(self):

        for x in self.drink_x_entry, self.first_x_entry, self.second_x_entry:
            x.delete(0, 'end')
            x.insert(0, '0')

        for x in self.first_combo, self.second_combo, self.drink_combo:
            x.current(0)

        self.message_Label.configure(text='')

class Weightview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Gewichtsverlauf"
        self.separator = ttk.Separator(self, orient='horizontal')

        self.controller = controller
        self.zielgewicht = 70  # Hier das gewünschte Zielgewicht eintragen

    def show(self):
        # Zeilen löschen
        for i in self.grid_slaves():
            i.grid_forget()

        # Anpassung Grid
        self.grid_rowconfigure(0, minsize=40)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Labels für die Spaltenüberschriften
        tk.Label(self, text="Gewicht (kg)", font=('Helvetica', 14, 'bold')).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self, text="Datum", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            weight_logs = cursor.fetchall()
            print('Gewichtsverlauf' + str(weight_logs))

        # ScrolledText-Widget für den Gewichtsverlauf
        text_widget = ScrolledText(self, wrap=tk.WORD, width=40, height=20, font=('Helvetica', 10))
        text_widget.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Gewichtsverlauf im Text-Widget anzeigen
        for log in weight_logs:
            text_widget.insert(tk.END, f" {log[1]} \t\t\t\t\t {log[0]} \n")

        # Zielgewichtslinie hinzufügen
        plt.axhline(y=self.zielgewicht, color='green', linestyle='--', label='Zielgewicht')

        # Gewichtsverlauf als roten Graphen anzeigen
        weights = [log[0] for log in weight_logs]
        dates = [log[1] for log in weight_logs]

        # using the variable ax for single a Axes
        fig, ax = plt.subplots()
        ax.plot(dates, weights, color='red', marker='o', label='Werte')
        ax.set_title('Gewichtsverlauf')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Gewicht (kg)')
        ax.legend()

        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(mdates.MonthLocator())

        ax.autoscale()
        ax.margins(x=0.1)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=3, rowspan=10, padx=10, pady=10, sticky='n')

        canvas.draw()

class Weightrecordview(tk.Frame):

    # Funktion zur Nummer-Validierung
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        self.title = "Gewicht speichern"

        is_number = (self.register(self.callback))

        self.weight_label = tk.Label(self, text="Gewicht in kg:")
        self.weight_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.message_Label = tk.Label(self, text="")
        self.safe_weight_button = tk.Button(self, text="Speichern")
        self.separator = ttk.Separator(self, orient='horizontal')

    def show(self):
        # Anpassung Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.weight_label.grid(row=2, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10)
        self.safe_weight_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=4, column=0, columnspan=2, pady=10)
        self.message_Label.configure(text="")
