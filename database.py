import sqlite3

class Database:
    def __init__(self, db_path="tracker.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Erstellen von Tabellen, falls sie nicht existieren
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT,
                duration INTEGER,
                date DATE
            )
        """)
        
        # (Weitere Tabellen hier)

        self.connection.commit()
