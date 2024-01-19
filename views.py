import tkinter
import tkinter as tk # python 3
from database import Database
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from user_meal_activity_weight import *
from PIL import Image, ImageTk



class Startview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

        # self.weight_entry = tk.Entry(self)

        # Button um User zu erstellen
        self.create_user_button = tk.Button(self, text="User erstellen", command=lambda: controller.show_frame("uv"))

        # Buttons um Werte einzutragen und zu speichern
        self.record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")
        self.record_weight_button = tk.Button(self, text="Gewicht aufzeichnen")

        # Buttons um Werte anzuzeigen
        self.record_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")
        self.workout_label = tk.Label(self, text="Letzte Trainingsaktivitäten")
        self.show_workout_button = tk.Button(self, text="Alle Trainingsaktivitäten anzeigen")
        self.meals_label = tk.Label(self, text="Letzte Mahlzeiten")
        self.show_meal_button = tk.Button(self, text="Alle Mahlzeiten anzeigen")
        self.show_weight_button = tk.Button(self, text="Gewichtsverlauf anzeigen")

        # Labels der Erstansicht

        self.name_label = tk.Label(self)
        self.weight_label = tk.Label(self, text="Aktuelles Gewicht (kg):")
        self.target_weight_label = tk.Label(self, text="Zielgewicht")
        self.message_Label = tk.Label(self, text="lalala")
        self.separator = ttk.Separator(self, orient='horizontal')

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

        self.cursor.execute("SELECT name FROM user WHERE ID = 1 ")
        name = self.cursor.fetchone()
        print('Name: ' + str(name))

        if not name:
            self.create_user_button.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        else:
            self.create_user_button.grid_forget()
            self.name_label.configure(text=name , font=('Helvetica', 18, 'bold'))
            self.name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.separator.grid(row=1, columnspan=3, sticky="ew")


        # Label für Gewichtsverlauf
        self.weight_label.grid(row=2, column=0, padx=10, pady=10)
        self.target_weight_label.grid(row=2, column=2, padx=10, pady=10)

        for i, m in enumerate(self.show_workouts, start=0):
            m.grid(row=i + 6, column=1, padx=5, pady=5)

        for i, m in enumerate(self.show_workout_dates, start=0) :
            m.grid(row=i + 6, column=0, padx=5, pady=5)

        self.cursor.execute("SELECT date, activity FROM workouts ORDER BY date DESC")
        workouts = self.cursor.fetchall()
        print('Workouts' + str(workouts))

        if len(workouts) > 3:
            objects = workouts[:3]
            for index, object in enumerate(objects, start=0):
                self.show_workout_dates[index].configure(text=object[0])
                self.show_workouts[index].configure(text=object[1])

        else:
            for index, workout in enumerate(workouts, start=0):
                self.show_workout_dates[index].configure(text=workout[0])
                self.show_workouts[index].configure(text=workout[1])

        # Buttons zum Recorden platzieren
        self.record_weight_button.grid(row=3, column=0,padx=10, pady=10)
        self.show_weight_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        self.workout_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)


        self.record_workout_button.grid(row=5, column=0, padx=10, pady=10)
        self.show_workout_button.grid(row=5, column=1, padx=10, pady=10)


        self.meals_label.grid(row=10, column=0, columnspan=3, padx=10, pady=10)
        self.record_meal_button.grid(row=11, column=0, padx=10, pady=10)
        self.show_meal_button.grid(row=11, column=1, padx=10, pady=10)

        for i, m in enumerate(self.show_meals, start=0):
            m.grid(row=i + 12, column=1, padx=5, pady=5)

        for i, m in enumerate(self.show_meal_dates, start=0) :
            m.grid(row=i + 12, column=0, padx=5, pady=5)

        self.cursor.execute("SELECT date, meal_name FROM meals ORDER BY date DESC")
        meals = self.cursor.fetchall()
        print('Meals' + str(len(meals)))

        if len(meals)>3:
            objects = meals[:3]
            for index, object in enumerate(objects, start=0):
                self.show_meals[index].configure(text=object[1])
                self.show_meal_dates[index].configure(text=object[0])
        else:
            for index, meal in enumerate(meals, start=0):
                self.show_meals[index].configure(text = meal[1])
                self.show_meal_dates[index].configure(text=meal[0])

                # Buttons zum Anzeigen von Daten platzieren

        self.message_Label.grid(row=20, column=0, columnspan=2, pady=10)


class Userview(tk.Frame):
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        is_number = (self.register(self.callback))

        self.title_label = tk.Label(self, text="User erstellen", font=('Helvetica', 18, 'bold'))

        self.name_entry = tk.Entry(self)
        self.age_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.weight_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.fl_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))

        # Labels der Erstansicht
        self.name_label = tk.Label(self, text="Name:")
        self.age_Label = tk.Label(self, text="Alter:")
        self.weight_label = tk.Label(self, text="Gewicht (kg):")
        self.fl_label = tk.Label(self, text="Fitnesslevel:")
        self.create_user_button = tk.Button(self, text="Speichern")

        self.message_Label = tk.Label(self, text="lalala")

        self.separator = ttk.Separator(self, orient='horizontal')


    def show(self):
        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")

        self.name_label.grid(row=2, column=0, padx=10, pady=10)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label für Mahlzeiten
        self.age_Label.grid(row=3, column=0, padx=10, pady=10)
        self.age_entry.grid(row=3, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.weight_label.grid(row=4, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=4, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.fl_label.grid(row=5, column=0, padx=10, pady=10)
        self.fl_entry.grid(row=5, column=1, padx=10, pady=10)

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

        self.title_label = tk.Label(self, text="Trainingsaktivitäten", font=('Helvetica', 18, 'bold'))

        self.activity_label = tk.Label(self, text="Aktivität")
        self.date_label = tk.Label(self, text="Datum")
        self.calories_label = tk.Label(self, text="Kalorien")

        self.separator = ttk.Separator(self, orient='horizontal')


    def show(self):

        for i in self.grid_slaves():
            i.grid_forget()

        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")


        # Ein Label für die Spaltenüberschriften
        self.activity_label.grid(row=2, column=0, padx=5, pady=5)
        self.calories_label.grid(row=2, column=1, padx=5, pady=5)
        self.date_label.grid(row=2, column=2, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT activity, calories, date FROM workouts ORDER BY date DESC")
            workouts = cursor.fetchall()
            print('Workouts' + str(workouts))

        for index, workout in enumerate(workouts, start=1):
            tk.Label(self, text=workout[0]).grid(row=index + 5, column=0, padx=5, pady=5)
            tk.Label(self, text=workout[1]).grid(row=index + 5, column=1, padx=5, pady=5)
            tk.Label(self, text=workout[2]).grid(row=index + 5, column=2, padx=5, pady=5)



class Trainingrecordview(tk.Frame):

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

        is_number = (self.register(self.callback))

        self.title_label = tk.Label(self, text="Training speichern", font=('Helvetica', 18, 'bold'))
        self.training_label = tk.Label(self, text="Trainingsaktivität:")
        self.workout_entry = ttk.Combobox(self, state="readonly", values=OPTIONS)
        self.duration_label = tk.Label(self, text="Minuten:")
        self.duration_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.message_Label = tk.Label(self, text="")
        self.safe_workout_button = tk.Button(self, text="Speichern")
        self.separator = ttk.Separator(self, orient='horizontal')

    def show(self):
        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")
        self.training_label.grid(row=2, column=1, padx=10, pady=10)
        self.workout_entry.grid(row=2, column=2, padx=10, pady=10)
        self.duration_label.grid(row=3, column=1, padx=10, pady=10)
        self.duration_entry.grid(row=3, column=2, padx=10, pady=10)
        self.safe_workout_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=5, column=0, columnspan=3, pady=10)
        self.message_Label.configure(text="")
        self.duration_entry.delete(0, 'end')
        self.workout_entry.set('')


class Mealview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.title_label = tk.Label(self, text="Mahlzeiten", font=('Helvetica', 18, 'bold'))
        self.separator = ttk.Separator(self, orient='horizontal')

        # Ein Label für die Spaltenüberschriften
        self.meal_label = tk.Label( self, text="Mahlzeit")
        self.calory_label = tk.Label(self,text="Kalorien")
        self.date_label = tk.Label(self, text="Datum")

    def show(self):
        # Label für Mahlzeiten
        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")

        self.meal_label.grid(row=2, column=0, padx=5, pady=5)
        self.calory_label.grid(row=2, column=1, padx=5, pady=5)
        self.date_label.grid(row=2, column=2, padx=5, pady=5)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
            meals = cursor.fetchall()
            print('Meals ' + str(meals))

        # Mahlzeiten im Frame anzeigen
        for index, meal in enumerate(meals, start=1):
            tk.Label(self, text='').grid(row=index + 5, column=0, padx=5, pady=5)
            tk.Label(self, text='').grid(row=index + 5, column=1, padx=5, pady=5)
            tk.Label(self, text='').grid(row=index + 5, column=2, padx=5, pady=5)

            tk.Label(self, text=meal[0]).grid(row=index+5, column=0, padx=5, pady=5)
            tk.Label(self, text=meal[1]).grid(row=index+5, column=1, padx=5, pady=5)
            tk.Label(self, text=meal[2]).grid(row=index+5, column=2, padx=5, pady=5)

class Mealrecordview(tk.Frame):
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

        self.title_label = tk.Label(self, text="Mahlzeit speichern", font=('Helvetica', 18, 'bold'))
        self.separator = ttk.Separator(self, orient='horizontal')

        self.first_label = tk.Label(self, text="Hauptgericht:")
        self.second_label = tk.Label(self, text="Beilage:")
        self.drink_label = tk.Label(self, text="Getränk:")

        # Dropdown-Menü erstellen

        self.first_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.first], state="readonly")
        self.first_combo.current(0)
        # self.first_combo.bind("<<ComboboxSelected>>", self.calc_cal)

        self.second_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.second], state="readonly")
        self.second_combo.current(0)
        # self.second_combo.bind("<<ComboboxSelected>>", self.calc_cal)

        self.drink_combo = ttk.Combobox(self, values=[element["name"] for element in Meal.drink], state="readonly")
        self.drink_combo.current(0)
        # self.drink_combo.bind("<<ComboboxSelected>>", self.calc_cal)

        # # scaled_images = [self.scale_image(element["pic"], 50, 50) for element in Meal.first]
        # scaled_images = ['img/meal/0.png','img/meal/0.png','img/meal/0.png','img/meal/0.png','img/meal/0.png','img/meal/0.png','img/meal/0.png']
        # self.first_combo["image"] = scaled_images

        self.first_x_label = tk.Label(self, text="Menge (in g):")
        self.second_x_label = tk.Label(self, text="Menge (in g):")
        self.drink_x_label = tk.Label(self, text="Menge(in g):")

        self.first_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.first_x_entry.insert(0, '0')

        self.second_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.second_x_entry.insert(0, '0')

        self.drink_x_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.drink_x_entry.insert(0, '0')

        self.message_Label = tk.Label(self, text="lalala")
        self.record_meal_button = tk.Button(self, text="Speichern")

    # def on_select(self, combo):
    #     selected_item = combo.get()
    #     print(f"Ausgewählt: " + str(selected_item))

    def show(self):

        for i in self.grid_slaves():
            i.grid_forget()

        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        self.separator.grid(row=1, columnspan=4, sticky="ew")

        self.first_label.grid(row=2, column=1, padx=10, pady=10)
        self.first_combo.grid(row=2, column=2, padx=10, pady=10)
        self.first_x_label.grid(row=3, column=1, padx=10, pady=10)
        self.first_x_entry.grid(row=3, column=2, padx=10, pady=10)

        self.second_label.grid(row=4, column=1, padx=10, pady=10)
        self.second_combo.grid(row=4, column=2, padx=10, pady=10)
        self.second_x_label.grid(row=5, column=1, padx=10, pady=10)
        self.second_x_entry.grid(row=5, column=2, padx=10, pady=10)

        self.drink_label.grid(row=6, column=1, padx=10, pady=10)
        self.drink_combo.grid(row=6, column=2, padx=10, pady=10)
        self.drink_x_label.grid(row=7, column=1, padx=10, pady=10)
        self.drink_x_entry.grid(row=7, column=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=1, columnspan=2, pady=10)
        self.record_meal_button.grid(row=8, column=1, columnspan=2, padx=10, pady=10)
        self.message_Label.configure(text="")

    def reset(self):

        y = tk.StringVar()
        y.set('0')

        for x in self.drink_x_entry, self.first_x_entry, self.second_x_entry:
            x.configure(textvariable=y)

        for x in self.first_combo, self.second_combo, self.drink_combo:
            x.current(0)

        self.message_Label.configure(text='')

        self.controller.show_frame("sv")


class Weightview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title_label = tk.Label(self, text="Gewichtsverlauf", font=('Helvetica', 18, 'bold'))
        self.separator = ttk.Separator(self, orient='horizontal')

        self.controller = controller
        self.zielgewicht = 70  # Hier das gewünschte Zielgewicht eintragen

    def show(self):

        for i in self.grid_slaves():
            i.grid_forget()

        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")

        # Ein Label für die Spaltenüberschriften
        tk.Label(self, text="Gewicht (kg)").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self, text="Datum").grid(row=2, column=1, padx=5, pady=5)

        # Gewichtsverlauf aus der Datenbank abrufen
        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            weight_logs = cursor.fetchall()
            print('Gewichtsverlauf' + str(weight_logs))

        # Gewichtsverlauf im Frame anzeigen
        for index, log in enumerate(weight_logs, start=1):
            tk.Label(self, text=log[0]).grid(row=index+5, column=0, padx=5, pady=5)
            tk.Label(self, text=log[1]).grid(row=index+5, column=1, padx=5, pady=5)

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
        canvas_widget.grid(row=100, column=0, columnspan=2, padx=10, pady=10)

        canvas.draw()

class Weightrecordview(tk.Frame):

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

        self.title_label = tk.Label(self, text="Gewicht speichern", font=('Helvetica', 18, 'bold'))
        self.weight_label = tk.Label(self, text="Gewicht in kg:")
        self.weight_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.message_Label = tk.Label(self, text="")
        self.safe_weight_button = tk.Button(self, text="Speichern")
        self.separator = ttk.Separator(self, orient='horizontal')

    def show(self):
        button = tk.Button(self, text="←", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.separator.grid(row=1, columnspan=3, sticky="ew")

        self.weight_label.grid(row=2, column=1, padx=10, pady=10)
        self.weight_entry.grid(row=2, column=2, padx=10, pady=10)
        self.safe_weight_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=4, column=0, columnspan=3, pady=10)
        self.message_Label.configure(text="")
