import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('fitness_tracker.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Erstellen von Tabellen, falls noch nicht existieren
        with self.conn:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT,
                    duration INTEGER,
                    date TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_name TEXT,
                    calories INTEGER,
                    date TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS weight_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weight REAL,
                    date TEXT
                )
            ''')

            self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                age INT,
                                weight INT,
                                fl text
                            )
                        ''')
        
        # (Weitere Tabellen hier)

        self.conn.commit()

