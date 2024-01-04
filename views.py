import tkinter as tk # python 3
from database import Database


class Startview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        self.workout_entry = tk.Entry(self)
        self.weight_entry = tk.Entry(self)
        self.meal_entry = tk.Entry(self)

        # Button um User zu erstellen
        self.create_user_button = tk.Button(self, text="User erstellen", command=lambda: controller.show_frame("uv"))

        # Buttons um Werte einzutragen und zu speichern
        self.record_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")
        self.record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")
        self.record_weight_button = tk.Button(self, text="Gewicht aufzeichnen")

        # Buttons um Werte anzuzeigen
        self.show_workout_button = tk.Button(self, text="Trainingsaktivitäten anzeigen")
        self.show_meal_button = tk.Button(self, text="Mahlzeiten anzeigen")
        self.show_weight_button = tk.Button(self, text="Gewichtsverlauf anzeigen")

        # Labels der Erstansicht
        self.training_label = tk.Label(self, text="Trainingsaktivität:")
        self.meal_Label = tk.Label(self, text="Mahlzeit:")
        self.weight_label = tk.Label(self, text="Gewicht (kg):")

        self.message_Label = tk.Label(self, text="lalala")

        self.create_user_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Label für Trainingsaktivitäten
        self.training_label.grid(row=1, column=0, padx=10, pady=10)
        self.workout_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label für Mahlzeiten
        self.meal_Label.grid(row=2, column=0, padx=10, pady=10)
        self.meal_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.weight_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons zum Recorden platzieren
        self.record_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.record_weight_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Buttons zum Anzeigen von Daten platzieren
        self.show_workout_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.show_meal_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.show_weight_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)



class Userview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.workout_entry = tk.Entry(self)
        self.weight_entry = tk.Entry(self)
        self.meal_entry = tk.Entry(self)
        self.fl_entry = tk.Entry(self)

        # Labels der Erstansicht
        self.name_label = tk.Label(self, text="Trainingsaktivität:")
        self.age_Label = tk.Label(self, text="Mahlzeit:")
        self.weight_label = tk.Label(self, text="Gewicht (kg):")
        self.fl_label = tk.Label(self, text="Gewicht (kg):")

        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.workout_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label für Mahlzeiten
        self.age_Label.grid(row=2, column=0, padx=10, pady=10)
        self.meal_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.weight_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        self.fl_label.grid(row=4, column=0, padx=10, pady=10)
        self.fl_entry.grid(row=4, column=1, padx=10, pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

        # Button um User zu erstellen
        self.create_user_button = tk.Button(self, text="User speichern")

        # Buttons zum Aufzeichnen von Daten
        self.create_user_button.grid(row=11, column=1, columnspan=2, padx=10, pady=10)


class Trainingview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()

        # Ein Label für die Spaltenüberschriften
        tk.Label(self, text="Aktivität").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

    def showtraining(self, parent, controller):

        self.db.cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = self.db.cursor.fetchall()

        print('Workout' + str(workouts))

        for index, workout in enumerate(workouts, start=1):
            tk.Label(self, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
            tk.Label(self, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)

class Mealview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class Weightview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

