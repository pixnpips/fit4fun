try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.grid(row=11, column=0, columnspan=1, padx=10, pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=11 , column=1, columnspan=1, padx=10, pady=10)

        workout_entry = tk.Entry(self)
        weight_entry = tk.Entry(self)
        meal_entry = tk.Entry(self)

        # Button um User zu erstellen
        create_user_button = tk.Button(self, text="User erstellen")

        #Buttons um Werte einzutragen und zu speichern
        record_workout_button = tk.Button(self, text="Trainingsaktivität aufzeichnen")
        record_meal_button = tk.Button(self, text="Mahlzeit aufzeichnen")
        record_weight_button = tk.Button(self, text="Gewicht aufzeichnen")

        #Buttons um Werte anzuzeigen
        show_workout_button = tk.Button(self, text="Trainingsaktivitäten anzeigen")
        show_meal_button = tk.Button(self, text="Mahlzeiten anzeigen")
        show_weight_button= tk.Button(self, text="Gewichtsverlauf anzeigen")

        #Labels der Erstansicht
        training_label = tk.Label(self, text="Trainingsaktivität:")
        meal_Label = tk.Label(self, text="Mahlzeit:")
        weight_label = tk.Label(self, text="Gewicht (kg):")

        message_Label = tk.Label(self, text="lalala")

        create_user_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Label für Trainingsaktivitäten
        training_label.grid(row=1, column=0, padx=10, pady=10)
        workout_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label für Mahlzeiten
        meal_Label.grid(row=2, column=0, padx=10, pady=10)
        meal_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label für Gewichtsverlauf
        weight_label.grid(row=3, column=0, padx=10, pady=10)
        weight_entry.grid(row=3, column=1, padx=10, pady=10)

        #Buttons zum Recorden platzieren
        record_workout_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        record_meal_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        record_weight_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Buttons zum Anzeigen von Daten platzieren
        show_workout_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        show_meal_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        show_weight_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        message_Label.grid(row=10, column=0, columnspan=2, pady=10)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()