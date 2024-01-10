import sqlite3


class Database:

    # Erstellen eines Singletons für die Datenbankklasse

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('fitness_tracker.db')
        return cls._instance

    # Db Connection für alle Methoden und Klassenmethoden die eine Connection brauchen, Cursor im Scope erstellen!
    def get_connection(self):
        return self.connection

    def create_tables(self):
        # Erstellen von Tabellen, falls noch nicht existieren
        cursor = self.get_connection().cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT,
                    duration INTEGER,
                    calories INTEGER,
                    date TEXT
                )
            ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_name TEXT,
                    calories INTEGER,
                    date TEXT
                )
            ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS weight_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weight REAL,
                    goal_weight REAL,  -- Neue Spalte für das Zielgewicht
                    date TEXT
                )
            ''')

        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                age INT,
                                weight INT,
                                fl text
                            )
                        ''')

        # (Weitere Tabellen hier)

        self.connection.commit()
