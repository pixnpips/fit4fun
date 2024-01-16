import tkinter
import tkinter as tk # python 3
from database import Database
import sqlite3
from tkinter import messagebox, ttk
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from user_meal_activity_weight import *
from PIL import Image, ImageTk



class Startview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()


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
        self.calories_label.grid(row=0, column=1, padx=5, pady=5)
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)
 
        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT activity, calories, date FROM workouts ORDER BY date DESC")
            workouts = cursor.fetchall()
            print('Workouts' + str(workouts))

        for index, workout in enumerate(workouts, start=1):
            tk.Label(self, text=workout[0]).grid(row=index, column=0, padx=5, pady=5)
            tk.Label(self, text=workout[1]).grid(row=index, column=1, padx=5, pady=5)
            tk.Label(self, text=workout[2]).grid(row=index, column=2, padx=5, pady=5)

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

        self.training_label = tk.Label(self, text="Trainingsaktivität:")
        self.workout_entry = ttk.Combobox(self, state="readonly", values=OPTIONS)
        self.duration_label = tk.Label(self, text="Minuten:")
        self.duration_entry = tk.Entry(self, validate='all', validatecommand=(is_number, '%P'))
        self.message_Label = tk.Label(self, text="")
        self.safe_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")

    def show(self):
        self.training_label.grid(row=1, column=0, padx=10, pady=10)
        self.workout_entry.grid(row=1, column=1, padx=10, pady=10)
        self.duration_label.grid(row=2, column=0, padx=10, pady=10)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10)
        self.safe_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("sv"))
        button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)


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

        self.first_x_entry = tk.Entry(self)
        self.first_x_entry.insert(0, '0')

        self.second_x_entry = tk.Entry(self)
        self.second_x_entry.insert(0, '0')

        self.drink_x_entry = tk.Entry(self)
        self.drink_x_entry.insert(0, '0')

        self.message_Label = tk.Label(self, text="lalala")
        self.record_meal_button = tk.Button(self, text="Speichern")

    # def on_select(self, combo):
    #     selected_item = combo.get()
    #     print(f"Ausgewählt: " + str(selected_item))



    def show(self):

        self.first_label.grid(row=2, column=0, padx=10, pady=10)
        self.first_combo.grid(row=2, column=1, padx=10, pady=10)
        self.first_x_label.grid(row=2, column=2, padx=10, pady=10)
        self.first_x_entry.grid(row=2, column=3, padx=10, pady=10)

        self.second_label.grid(row=3, column=0, padx=10, pady=10)
        self.second_combo.grid(row=3, column=1, padx=10, pady=10)
        self.second_x_label.grid(row=3, column=2, padx=10, pady=10)
        self.second_x_entry.grid(row=3, column=3, padx=10, pady=10)

        self.drink_label.grid(row=4, column=0, padx=10, pady=10)
        self.drink_combo.grid(row=4, column=1, padx=10, pady=10)
        self.drink_x_label.grid(row=4, column=2, padx=10, pady=10)
        self.drink_x_entry.grid(row=4, column=3, padx=10, pady=10)

        button = tk.Button(self, text="Go to the start page", command=self.reset)
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)
        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)
        self.record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

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
        self.controller = controller
        self.weight_logs = []

        # Label für die Spaltenüberschrift
        self.weight_label = tk.Label(self, text="Gewicht in (kg)")
        self.date_label = tk.Label(self, text="Datum")

        # Graph für die Gewichtsanzeige
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10)
        self.canvas.draw()

        # Add a toolbar (optional)
        toolbar = ttk.Notebook(self)
        toolbar.grid(row=0, column=0, columnspan=2)
        toolbar.add(self.canvas.get_tk_widget(), text="Graph")

        # Liste zum Speichern von Gewichtsdaten
        self.weight_logs = []

    def update_graph(self):
        # Gewichtsdaten aus der Weightview-Klasse
        weight_logs = self.weight_logs

        # Extrahiere Gewichtsdaten und Datum für den Graphen
        weights = [float(log[0]) for log in weight_logs]
        dates = [mdates.datestr2num(log[1]) for log in weight_logs]  # Convert dates to numerical format

        # Plotte die Gewichtsdaten in rot
        self.ax.clear()
        self.ax.plot(dates, weights, marker='o', linestyle='-', color='red')

         #Beschriftungen hinzufügen
        self.ax.set_xlabel('Datum')  
        self.ax.set_ylabel('Gewicht') 
        self.ax.set_title('Gewichtsverlauf')
          
        # Red line example (you can customize this based on your criteria)
        if weights and weights[-1] > 100:
            self.ax.axhline(y=100, color='red', linestyle='--', label='Critical Weight')

        # Formatierung der x-Achse
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())  # Adjust as needed
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Adjust date format

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45)

        # Zeige den aktualisierten Graphen an
        self.canvas.draw()

    def show(self):
        # Label für Gewicht
        self.weight_label.grid(row=0, column=0, padx=5, pady=5)

        button = tk.Button(self, text="Go to the start page", command=lambda: self.controller.show_frame("sv"))
        button.grid(row=11, column=0, columnspan=1, padx=10, pady=10)

        with self.controller.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            self.weight_logs = cursor.fetchall()  # Update the weight_logs attribute 
            
             
class Weightrecordview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()
        
        # Entry für Gewicht
        self.weight_entry = tk.Entry(self)
        self.weight_entry.insert(0, '0')
        
        # Entry für Datum
        self.date_entry = tk.Entry(self)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Standardwert auf das aktuelle Datum und die Uhrzeit
        
        self.record_weight_button = tk.Button(self, text="Gewicht aufzeichnen", command=self.record_weight)
        
        

        # Button für Startview
        self.back_button = tk.Button(self, text="Zurück zur Startseite", command=lambda: self.controller.show_frame("sv"))
        self.show()

    def show(self):
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)  # Add this line to display date_entry
        self.record_weight_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.back_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def record_weight(self):
        print("Record weight button clicked")
        #Gewicht aus dem Eingabefeld abrufen
        entered_weight = self.weight_entry.get()
        entered_date = self.date_entry.get()  

        try:
            
            # Das Gewicht in Float konvertieren
            entered_weight = float(entered_weight)

           # Datum aus dem Eingabefeld abrufen
            entered_date = self.date_entry.get()

            # Das Gewicht mit dem eingegebenen Datum in die Datenbank einfügen
            with self.controller.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO weight_logs (weight, date) VALUES (?, ?)", (entered_weight, entered_date))
                conn.commit()

            # Fetch the latest data from the database
            cursor.execute("SELECT weight, date FROM weight_logs ORDER BY date DESC")
            self.controller.Weightview.weight_logs = cursor.fetchall()

            # Update weight_logs attribut in Weightview
            self.controller.frames["Weightview"].weight_logs = self.weight_logs
            
            # Optional: Check if entered weight exceeds a threshold, show a red line in the graph
            threshold = 100  # Replace with your desired threshold
            if entered_weight > threshold:
                self.controller.Weightview.show_red_line(threshold)
            
            # Update the graph in the Weightview class
            self.controller.Weightview.update_graph()
            
            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", "Gewicht erfolgreich aufgezeichnet!")
            
        except ValueError:
            # Show an error message if the entered weight is not a valid number
            messagebox.showerror("Fehler", "Ungültige Gewichtseingabe. Bitte geben Sie eine Zahl ein.")
            
        except Exception as e:
            # Fehlermeldung anzeigen, wenn etwas schief geht
            messagebox.showerror("Fehler", "Fehler beim Aufzeichnen des Gewichts: {str(e)}")