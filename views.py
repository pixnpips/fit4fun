from tkinter import ttk


class Startview:
    def __init__(self,root):

        self.root = root
        self.workout_entry = ttk.Entry(self.root)
        self.weight_entry = ttk.Entry(self.root)
        self.meal_entry = ttk.Entry(self.root)

        # Button um User zu erstellen
        self.create_user_button = ttk.Button(self.root, text="User erstellen")

        #Buttons um Werte einzutragen und zu speichern
        self.record_workout_button = ttk.Button(self.root, text="Trainingsaktivität aufzeichnen")
        self.record_meal_button = ttk.Button(self.root, text="Mahlzeit aufzeichnen")
        self.record_weight_button = ttk.Button(self.root, text="Gewicht aufzeichnen")

        #Buttons um Werte anzuzeigen
        self.show_workout_button = ttk.Button(self.root, text="Trainingsaktivitäten anzeigen")
        self.show_meal_button = ttk.Button(self.root, text="Mahlzeiten anzeigen")
        self.show_weight_button= ttk.Button(self.root, text="Gewichtsverlauf anzeigen")

        #Labels der Erstansicht
        self.training_label = ttk.Label(self.root, text="Trainingsaktivität:")
        self.meal_Label = ttk.Label(self.root, text="Mahlzeit:")
        self.weight_label = ttk.Label(self.root, text="Gewicht (kg):")

        self.message_Label = ttk.Label(self.root, text="lalala")



    def show(self):

        # Buttons zum Aufzeichnen von Daten
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

        #Buttons zum Recorden platzieren
        self.record_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.record_weight_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Buttons zum Anzeigen von Daten platzieren
        self.show_workout_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.show_meal_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.show_weight_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.message_Label.grid(row=10, column=0, columnspan=2, pady=10)


class Userview:
    def __init__(self, root):
        self.root = root

        self.meal_entry = ttk.Entry(self.root)

        # Button um User zu erstellen
        self.create_user_button = ttk.Button(self.root, text="User erstellen")

        # Labels der Erstansicht
        self.training_label = ttk.Label(self.root, text="Trainingsaktivität:")

        # Buttons zum Aufzeichnen von Daten
        self.create_user_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
