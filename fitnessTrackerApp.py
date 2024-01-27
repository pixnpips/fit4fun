import tkinter as tk

from views import Startview, Userview, Trainingview, Trainingrecordview, Mealview, Mealrecordview, Weightview, Weightrecordview
from tkinter import font as tkfont
from datetime import datetime
from database import Database
from user_meal_activity_weight import *
from tkinter import ttk
from ttkthemes import ThemedStyle


class FitnessTrackerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Titel und Schriftart
        self.title("Fit4Fun")
        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('1080x720')
        self.resizable(False, True)



        # Kopfleiste
        self.button = tk.Button(self, text="←", command=lambda: self.show_frame("sv"))
        # self.button.grid(row=0, column=0)
        self.title_label = tk.Label(self, text="", font=('Helvetica', 18, 'bold'))
        self.placeholder = tk.Label(self, text="")

        self.button.grid(row=0, column=0)
        self.title_label.grid(row=0, column=1)
        self.placeholder.grid(row=0, column=2)

        self.grid_rowconfigure(0, minsize=60)
        self.grid_columnconfigure(0, weight=0, minsize=200)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=0, minsize=200)

        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=1, column=0, columnspan=3, sticky="ew")

        # self.container wird erstellt, der alle Frames beinhaltet
        self.container = tk.Frame(self)
        # self.container.pack(side="top", anchor='center', fill="both", expand=True)
        self.container.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1, minsize=1080)

        # Liste der Frames
        self.frames = {}

        # View Objekte erzeugen und in den Frame packen

        self.Startview = Startview(parent=self.container, controller=self)


        self.Userview = Userview(parent=self.container, controller=self)
        self.Trainingview = Trainingview(parent=self.container, controller=self)
        self.Trainingrecordview = Trainingrecordview(parent=self.container, controller=self)
        self.Mealview = Mealview(parent=self.container, controller=self)
        self.Mealrecordview = Mealrecordview(parent=self.container, controller=self)
        self.Weightview = Weightview(parent=self.container, controller=self)
        self.Weightrecordview = Weightrecordview(parent=self.container, controller=self)

        self.frames['sv'] = self.Startview
        self.frames['uv'] = self.Userview
        self.frames['tv'] = self.Trainingview
        self.frames['trv'] = self.Trainingrecordview
        self.frames['mv'] = self.Mealview
        self.frames['mrv'] = self.Mealrecordview
        self.frames['wv'] = self.Weightview
        self.frames['wrv'] = self.Weightrecordview

        #Styles werden gesetzt
        for x in self.frames:
            style = ThemedStyle(self.frames.get(x))
            style.set_theme("arc")

        self.Startview.grid(row=3, column=0, sticky="nsew")

        self.Userview.grid(row=3, column=0, sticky="nsew")
        self.Trainingview.grid(row=3, column=0, sticky="nsew")
        self.Trainingrecordview.grid(row=3, column=0, sticky="nsew")
        self.Mealview.grid(row=3, column=0, sticky="nsew")
        self.Mealrecordview.grid(row=3, column=0, sticky="nsew")
        self.Weightview.grid(row=3, column=0, sticky="nsew")
        self.Weightrecordview.grid(row=3, column=0, sticky="nsew")

        self.show_frame("sv")
        # SQLite-Datenbankverbindung herstellen
        self.db = Database()
        self.db.create_tables()
        print(vars(self.frames.get('sv')))

        # funktionen mappen
        self.map_button_functions()

    # Funktion, die eine View in einem Frame im Cointainer an die Topo Positioon bringt
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.title_label.config(text= frame.title)
        if page_name=='sv':
            self.button.grid_forget()
        else:
            self.button.grid(row=0, column=0)

        frame.show()
        frame.tkraise()

    def record_user(self):

        name = self.Userview.name_entry.get()
        age = self.Userview.age_entry.get()
        weight = self.Userview.weight_entry.get()
        fl = self.Userview.fl_entry.get()

        connection = self.db.get_connection()
        cursor = connection.cursor()

        print(weight)
        # Überprüfen, ob die Eingabe eine positive Zahl ist
        try:
            weight = float(weight)
            if weight <= 0:
                raise ValueError("Das Gewicht muss eine positive Zahl sein.")
        except ValueError:
            self.Startview.message_Label.configure(text="Bitte geben Sie eine gültige Gewichtsangabe ein.",
                                                   foreground="red")
            return

        # Gewichtsverlauf in die Datenbank einfügen
        cursor.execute("INSERT INTO user (name, age, weight, fl) VALUES (?,?,?,?)", (name, age, weight, fl))

        # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
        self.Userview.message_Label.configure(text=f"Hallo {name}, es kann losgehen",
                                              foreground="green")

        # Eingabefelder leeren
        # self.Startview.weight_entry.delete(0, tki.END)

        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        connection.commit()

        print(users)

    def record_workout(self):

        connection = self.db.get_connection()
        cursor = connection.cursor()

        # Eingabewerte vom Benutzer abrufen
        activity = self.Trainingrecordview.workout_entry.get()
        cal_per_min = 0
        if activity == "Running":
            cal_per_min = 17
        elif activity == "Jogging":
            cal_per_min = 15
        elif activity == "Walking":
            cal_per_min = 8
        elif activity == "Swimming":
            cal_per_min = 8
        elif activity == "Cycling":
            cal_per_min = 7
        elif activity == "Basketball":
            cal_per_min = 10
        elif activity == "Soccer":
            cal_per_min = 10
        elif activity == "Tennis":
            cal_per_min = 10
        elif activity == "Boxing":
            cal_per_min = 8
        elif activity == "Yoga":
            cal_per_min = 4
        elif activity == "Pilates":
            cal_per_min = 6
        elif activity == "Weightlifting":
            cal_per_min = 5
        else:
            cal_per_min = 0

        print(activity)
        print(cal_per_min)

        duration = self.Trainingrecordview.duration_entry.get()

        # Überprüfen, ob die Eingabe nicht leer ist
        if activity == "":
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Trainingrecordview.message_Label.configure(text='Bitte Training eingeben', foreground='red')
            return

        if duration == "":
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Trainingrecordview.message_Label.configure(text='Bitte Länge Trainings eingeben', foreground='red')
            return

        calories = int(cal_per_min) * int(duration)

        print(calories)

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Trainingsaktivität in die Datenbank einfügen

        # cursor.execute("INSERT INTO workouts (activity, duration, calories, date) VALUES (?, ?, ?, ?)", (activity, current_date))
        cursor.execute("INSERT INTO workouts (activity, duration, calories, date) VALUES (?, ?, ?, ?)", (activity, int(duration), int(calories), current_date))

        # Meldung anzeigen, dass die Trainingsaktivität erfolgreich aufgezeichnet wurde
        self.Trainingrecordview.message_Label.configure(
            text=f"Trainingsaktivität '{activity}' erfolgreich aufgezeichnet.",
            foreground="green")

        # Eingabefelder leeren
        self.Trainingrecordview.workout_entry.delete(0, tk.END)

        cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = cursor.fetchall()

        print(workouts)

        connection.commit()

    def record_meal(self):
        # Eingabewerte vom Benutzer abrufen
        first = self.Mealrecordview.first_combo.get()
        second = self.Mealrecordview.second_combo.get()
        drink = self.Mealrecordview.drink_combo.get()

        meal = Meal()
        meal.first = Meal.first[self.Mealrecordview.first_combo.current()]
        meal.second = Meal.second[self.Mealrecordview.second_combo.current()]
        meal.drink = Meal.drink[self.Mealrecordview.drink_combo.current()]

        meal.fq = int(self.Mealrecordview.first_x_entry.get())
        meal.sq = int(self.Mealrecordview.second_x_entry.get())
        meal.dq = int(self.Mealrecordview.drink_x_entry.get())

        connection = self.db.get_connection()
        cursor = connection.cursor()

        # Überprüfen, ob die Eingabe nicht leer ist
        if first != 'Bitte wählen' and meal.fq == 0:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Mealrecordview.message_Label.configure(
                text="Bitte geben Sie die Menge des Hauptgerichtes in Gramm ein.", foreground="red")
            return

        if second != 'Bitte wählen' and meal.sq == 0:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Mealrecordview.message_Label.configure(
                text="Bitte geben Sie die Menge der Beilage in Gramm ein.", foreground="red")
            return

        if drink != 'Bitte wählen' and meal.dq == 0:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Mealrecordview.message_Label.configure(
                text="Bitte geben Sie die Menge des Getränks in Gramm ein.", foreground="red")
            return

        if first == second == drink == "Bitte wählen":
            self.Mealrecordview.message_Label.configure(
                text="Bitte geben sie mindestens ein Gericht oder Getränk ein.", foreground="red")
            return

        if first == 'Bitte wählen':
            first = ''

        if second == 'Bitte wählen':
            second = ''

        if drink == 'Bitte wählen':
            drink = ''
        # Eingabewerte vom Benutzer abrufen
        # calories = self.calories_entry.get()
        calories = meal.count_cals()

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Mahlzeit in die Datenbank einfügen
        cursor.execute("INSERT INTO meals (meal_name, calories, date) VALUES (?, ?, ?)",
                       (first + ' ' + second + ' ' + drink, calories, current_date))

        # Meldung anzeigen, dass die Mahlzeit erfolgreich aufgezeichnet wurde
        self.Mealrecordview.message_Label.configure(
            text=f"Mahlzeit {first} {second} {drink} mit {calories} Kalorien erfolgreich aufgezeichnet.",
            foreground="green")

        connection.commit()
        # self.calories_entry.delete(0, tki.END)

        # cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
        # meals = cursor.fetchall()
        # print(meals)


    def record_weight(self):
        # Eingabewerte vom Benutzer abrufen
        weight = self.Weightrecordview.weight_entry.get()
        connection = self.db.get_connection()
        cursor = connection.cursor()

        print(weight)
        # Überprüfen, ob die Eingabe eine positive Zahl ist
        try:
            weight = float(weight)
            if weight <= 0:
                raise ValueError("Das Gewicht muss eine positive Zahl sein.")
        except ValueError:
            self.Weightrecordview.message_Label.configure(text="Bitte geben Sie eine gültige Gewichtsangabe ein.",
                                                   foreground="red")

            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gewichtsverlauf in die Datenbank einfügen
        cursor.execute("INSERT INTO weight_logs (weight, date) VALUES (?, ?)", (weight, current_date))

        # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
        self.Weightrecordview.message_Label.configure(text=f"Gewicht {weight} kg erfolgreich aufgezeichnet.",
                                               foreground="green")

        # Eingabefelder leeren
        self.Weightrecordview.weight_entry.delete(0, tk.END)

        cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
        weight_logs = cursor.fetchall()

        connection.commit()

        print(weight_logs)

    # Hier werden alle Funktionen allen Buttons aller Views zugeordnet
    def map_button_functions(self):

        # Mapping der Funktionen in der Startview

        # self.Startview.show_workout_button.configure(command=self.show_workouts)
        self.Startview.show_workout_button.configure(command=lambda: self.show_frame("tv"))
        # self.Startview.record_workout_button.configure(command=self.record_workout)
        self.Startview.record_workout_button.configure(command=lambda: self.show_frame("trv"))

        # self.Startview.show_meal_button.configure(command=self.show_meals)
        # self.Startview.record_meal_button.configure(command=self.record_meal)

        self.Startview.show_meal_button.configure(command=lambda: self.show_frame('mv'))
        self.Startview.record_meal_button.configure(command=lambda: self.show_frame('mrv'))

        # self.Startview.show_weight_button.configure(command=self.show_weight_logs)
        self.Startview.show_weight_button.configure(command=lambda: self.show_frame('wv'))
        self.Startview.record_weight_button.configure(command=lambda: self.show_frame('wrv'))

        # Mapping der Funktionen in allen anderen Views

        self.Userview.create_user_button.configure(command=self.record_user)
        self.Trainingrecordview.safe_workout_button.configure(command=self.record_workout)
        self.Mealrecordview.record_meal_button.configure(command=self.record_meal)

        self.Weightrecordview.safe_weight_button.configure(command=self.record_weight)



if __name__ == "__main__":
    app = FitnessTrackerApp()
    app.mainloop()