import tkinter as tki
from views import Startview, Userview, Trainingview, Trainingrecordview, Mealview, Mealrecordview, Weightview
from tkinter import font as tkfont
from datetime import datetime
from database import Database
        
class FitnessTrackerApp(tki.Tk):
    def __init__(self, *args, **kwargs):
        tki.Tk.__init__(self, *args, **kwargs)

        #Titel und Schriftart
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        #self.container wird erstellt, der alle Frames beinhaltet
        self.container = tki.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #Liste der Frames
        self.frames = {}

        #View Objekte erzeugen und in den Frame packen

        self.Startview = Startview(parent=self.container, controller=self)
        self.Userview = Userview(parent=self.container, controller=self)
        self.Trainingview = Trainingview(parent=self.container, controller=self)
        self.Trainingrecordview = Trainingrecordview(parent=self.container, controller=self)
        self.Mealview = Mealview (parent=self.container, controller=self)
        self.Mealrecordview = Mealrecordview (parent=self.container, controller=self)
        self.Weightview = Weightview(parent=self.container, controller=self)

        self.frames['sv'] = self.Startview
        self.frames['uv'] = self.Userview
        self.frames['tv'] = self.Trainingview
        self.frames['trv'] = self.Trainingrecordview
        self.frames['mv'] = self.Mealview
        self.frames['mrv'] = self.Mealrecordview
        self.frames['wv'] = self.Weightview

        self.Startview.grid(row=0, column=0, sticky="nsew")
        self.Userview.grid(row=0, column=0, sticky="nsew")
        self.Trainingview.grid(row=0, column=0, sticky="nsew")
        self.Trainingrecordview.grid(row=0, column=0, sticky="nsew")
        self.Mealview.grid(row=0, column=0, sticky="nsew")
        self.Mealrecordview.grid(row=0, column=0, sticky="nsew")
        self.Weightview.grid(row=0, column=0, sticky="nsew")

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
        frame.show()
        frame.tkraise()


    def record_user(self):

        name = self.Userview.name_entry.get()
        age = self.Userview.weight_entry.get()
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
        cursor.execute("INSERT INTO user (name, age, weight, fl) VALUES (?,?,?,?)", (name, age, weight, fl ))


        # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
        self.Userview.message_Label.configure(text=f"Hallo {name}, es kann losgehen",
                                               foreground="green")

        # Eingabefelder leeren
        self.Startview.weight_entry.delete(0, tki.END)

        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        print(users)

    def record_workout(self):
        # Eingabewerte vom Benutzer abrufen
        activity = self.Trainingrecordview.workout_entry.get()
        connection = self.db.get_connection()
        cursor = connection.cursor()

        print(activity)

        # Überprüfen, ob die Eingabe nicht leer ist
        if activity == "":
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Trainingrecordview.message_Label.configure(text='Bitte Training eingeben', foreground='red')
            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Trainingsaktivität in die Datenbank einfügen

        cursor.execute("INSERT INTO workouts (activity, duration, calories, date) VALUES (?, ?, ?, ?)", (activity, current_date))

        # Meldung anzeigen, dass die Trainingsaktivität erfolgreich aufgezeichnet wurde
        self.Trainingrecordview.message_Label.configure(text=f"Trainingsaktivität '{activity}' erfolgreich aufgezeichnet.",
                                           foreground="green")

        # Eingabefelder leeren
        self.Trainingrecordview.workout_entry.delete(0, tki.END)

        cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = cursor.fetchall()

        print(workouts)

    def record_meal(self):
        # Eingabewerte vom Benutzer abrufen
        meal_name = self.Mealrecordview.meal_entry.get()
        print(meal_name)

        connection = self.db.get_connection()
        cursor = connection.cursor()

        # Überprüfen, ob die Eingabe nicht leer ist
        if not meal_name:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Mealrecordview.message_Label.configure(text="Bitte geben Sie den Mahlzeitennamen ein.", foreground="red")

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
            (tki.Label( text="Bitte geben Sie eine gültige Kalorienanzahl ein.", foreground="red").
             grid(row=10, column=0, columnspan=2, pady=10))
            return

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Mahlzeit in die Datenbank einfügen
        cursor.execute("INSERT INTO meals (meal_name, calories, date) VALUES (?, ?, ?)",
                               (meal_name, calories, current_date))

        # Meldung anzeigen, dass die Mahlzeit erfolgreich aufgezeichnet wurde
        self.Mealrecordview.message_Label.configure(
            text=f"Mahlzeit '{meal_name}' mit {calories} Kalorien erfolgreich aufgezeichnet.",
            foreground="green")

        # Eingabefelder leeren
        self.Mealrecordview.meal_entry.delete(0, tki.END)
        # self.calories_entry.delete(0, tki.END)

        cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
        meals = cursor.fetchall()
        print(meals)

    def record_weight(self):
        # Eingabewerte vom Benutzer abrufen
        weight = self.Startview.weight_entry.get()
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

        # Aktuelles Datum und Uhrzeit abrufen
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gewichtsverlauf in die Datenbank einfügen
        cursor.execute("INSERT INTO weight_logs (weight, date) VALUES (?, ?)", (weight, current_date))

        # Meldung anzeigen, dass das Gewicht erfolgreich aufgezeichnet wurde
        self.Startview.message_Label.configure(text=f"Gewicht {weight} kg erfolgreich aufgezeichnet.", foreground="green")

        # Eingabefelder leeren
        self.Startview.weight_entry.delete(0, tki.END)

        cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
        weight_logs = cursor.fetchall()

        print(weight_logs)


    #Hier werden alle Funktionen allen Buttons aller Views zugeordnet
    def map_button_functions(self):

        #Mapping der Funktionen in der Startview

        # self.Startview.show_workout_button.configure(command=self.show_workouts)
        self.Startview.show_workout_button.configure(command=lambda: self.show_frame("tv"))
        # self.Startview.record_workout_button.configure(command=self.record_workout)
        self.Startview.record_workout_button.configure(command=lambda: self.show_frame("trv"))


        # self.Startview.show_meal_button.configure(command=self.show_meals)
        # self.Startview.record_meal_button.configure(command=self.record_meal)

        self.Startview.show_meal_button.configure(command=lambda: self.show_frame('mv'))
        self.Startview.record_meal_button.configure(command=lambda: self.show_frame('mrv'))

        # self.Startview.show_weight_button.configure(command=self.show_weight_logs)
        self.Startview.show_weight_button.configure(command=lambda:self.show_frame('wv'))
        self.Startview.record_weight_button.configure(command=self.record_weight)

        #Mapping der Funktionen in allen anderen Views

        self.Userview.create_user_button.configure(command=self.record_user)
        self.Trainingrecordview.safe_workout_button.configure(command=self.record_workout)
        self.Mealrecordview.record_meal_button.configure(command=self.record_meal)

        
if __name__ == "__main__":
    app = FitnessTrackerApp()
    app.mainloop()