import tkinter as tki
from views import Startview, Userview, Trainingview, Trainingrecordview
from tkinter import font as tkfont
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import Database

class Weightview(tki.Frame):
    def __init__(self, parent, controller):
        tki.Frame.__init__(self, parent)
        self.controller = controller
        self.zielgewicht = 70  # Hier das gewünschte Zielgewicht eintragen

    def show_weight_logs(self):
        # Ein Frame erstellen, um den Gewichtsverlauf anzuzeigen
        neues_fenster = tki.Toplevel(self.controller.container)
        weight_logs_frame = tki.Frame(neues_fenster)
        weight_logs_frame.grid(row=16, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        tki.Label(weight_logs_frame, text="Gewicht (kg)").grid(row=0, column=0, padx=5, pady=5)
        tki.Label(weight_logs_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        # Gewichtsverlauf aus der Datenbank abrufen
        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            weight_logs = cursor.fetchall()

        # Gewichtsverlauf im Frame anzeigen
        for index, log in enumerate(weight_logs, start=1):
            tki.Label(weight_logs_frame, text=log[0]).grid(row=index, column=0, padx=5, pady=5)
            tki.Label(weight_logs_frame, text=log[1]).grid(row=index, column=1, padx=5, pady=5)

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

        canvas = FigureCanvasTkAgg(fig, master=neues_fenster)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=16, column=2, padx=10, pady=10)

        canvas.draw()
        
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

        self.frames['sv'] = self.Startview
        self.frames['uv'] = self.Userview
        self.frames['tv'] = self.Trainingview
        self.frames['trv'] = self.Trainingrecordview

        self.Startview.grid(row=0, column=0, sticky="nsew")
        self.Userview.grid(row=0, column=0, sticky="nsew")
        self.Trainingview.grid(row=0, column=0, sticky="nsew")
        self.Trainingrecordview.grid(row=0, column=0, sticky="nsew")

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
        cursor.execute("INSERT INTO user (name, age, weight, goal_weight,fl) VALUES (?, ?, ?, ? )", (name, age, weight, fl ))


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

        cursor.execute("INSERT INTO workouts (activity, date) VALUES (?, ?)", (activity, current_date))

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
        meal_name = self.Startview.meal_entry.get()
        print(meal_name)

        connection = self.db.get_connection()
        cursor = connection.cursor()

        # Überprüfen, ob die Eingabe nicht leer ist
        if not meal_name:
            # Zeige eine Meldung an, dass das Feld nicht leer sein darf
            self.Startview.message_Label.configure(text="Bitte geben Sie den Mahlzeitennamen ein.", foreground="red")

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
        self.Startview.message_Label.configure(
            text=f"Mahlzeit '{meal_name}' mit {calories} Kalorien erfolgreich aufgezeichnet.",
            foreground="green")

        # Eingabefelder leeren
        self.Startview.meal_entry.delete(0, tki.END)
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

    def show_workouts(self):
        # Ein Frame erstellen, um Trainingsaktivitäten anzuzeigen

        neues_fenster = tki.Toplevel(self.container)
        workouts_frame = tki.Frame(neues_fenster)

        workouts_frame.pack()

        connection = self.db.get_connection()
        cursor = connection.cursor()

        # Ein Label für die Spaltenüberschriften
        tki.Label(workouts_frame, text="Aktivität").grid(row=0, column=0, padx=5, pady=5)
        tki.Label(workouts_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        # Trainingsaktivitäten aus der Datenbank abrufen
        cursor.execute("SELECT activity, date FROM workouts ORDER BY date DESC")
        workouts = cursor.fetchall()

        print(workouts)

        # Trainingsaktivitäten im Frame anzeigen
        for index, workout in enumerate(workouts, start=1):
            tki.Label(workouts_frame, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
            tki.Label(workouts_frame, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)



    def show_meals(self):
        # Ein Frame erstellen, um Mahlzeiten anzuzeigen
        neues_fenster = tki.Toplevel(self.container)

        connection = self.db.get_connection()
        cursor = connection.cursor()

        meals_frame = tki.Frame(neues_fenster)
        meals_frame.grid(row=15, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        tki.Label(meals_frame, text="Mahlzeit").grid(row=0, column=0, padx=5, pady=5)
        tki.Label(meals_frame, text="Kalorien").grid(row=0, column=1, padx=5, pady=5)
        tki.Label(meals_frame, text="Datum").grid(row=0, column=2, padx=5, pady=5)

        # Mahlzeiten aus der Datenbank abrufen
        cursor.execute("SELECT meal_name, calories, date FROM meals ORDER BY date DESC")
        meals = cursor.fetchall()

        # Mahlzeiten im Frame anzeigen
        for index, meal in enumerate(meals, start=1):
            tki.Label(meals_frame, text=meal[0]).grid(row=index, column=0, padx=5, pady=5)
            tki.Label(meals_frame, text=meal[1]).grid(row=index, column=1, padx=5, pady=5)
            tki.Label(meals_frame, text=meal[2]).grid(row=index, column=2, padx=5, pady=5)

    def show_weight_logs(self):
        # Ein Frame erstellen, um den Gewichtsverlauf anzuzeigen
        neues_fenster = tki.Toplevel(self.container)

        connection = self.db.get_connection()
        cursor = connection.cursor()

        weight_logs_frame = tki.Frame(neues_fenster)
        weight_logs_frame.grid(row=16, column=0, columnspan=2, pady=10)

        # Ein Label für die Spaltenüberschriften
        tki.Label(weight_logs_frame, text="Gewicht (kg)").grid(row=0, column=0, padx=5, pady=5)
        tki.Label(weight_logs_frame, text="Datum").grid(row=0, column=1, padx=5, pady=5)

        # Gewichtsverlauf aus der Datenbank abrufen
        cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
        weight_logs = cursor.fetchall()

        # Gewichtsverlauf im Frame anzeigen
        for index, log in enumerate(weight_logs, start=1):
            tki.Label(weight_logs_frame, text=log[0]).grid(row=index, column=0, padx=5, pady=5)
            tki.Label(weight_logs_frame, text=log[1]).grid(row=index, column=1, padx=5, pady=5)


    #Hier werden alle Funktionen allen Buttons aller Views zugeordnet
    def map_button_functions(self):
        self.Startview.show_workout_button.configure(command=lambda: self.show_frame("tv"))
        # self.Startview.show_workout_button.configure(command=self.show_workouts)
        self.Startview.show_meal_button.configure(command=self.show_meals)
        self.Startview.show_weight_button.configure(command=self.show_weight_logs)
        # self.Startview.record_workout_button.configure(command=self.record_workout)
        self.Startview.record_workout_button.configure(command=lambda: self.show_frame("trv"))
        self.Startview.record_meal_button.configure(command=self.record_meal)
        self.Startview.record_weight_button.configure(command=self.record_weight)

        self.Userview.create_user_button.configure(command=self.record_user)

        self.Trainingrecordview.safe_workout_button.configure(command=self.record_workout)

        
if __name__ == "__main__":
    app = FitnessTrackerApp()
    weight_view = Weightview(app, controller=app)
    app.frames['wv'] = weight_view
    app.mainloop()