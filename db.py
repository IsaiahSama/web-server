"""File used to manage the database which handles the meta information for files."""

from sqlite3 import connect
from os import listdir
from constants import UPLOAD_FOLDER


class Database:
    """Class used to manage the Database.
    
    Attrs:
        DB_NAME (str)

    Methods:
        setup(): Sets up the database
        get_entry(filename): Gets an entry from the database
        get_entries(): Gets all entries from the database
        add_entry(filename): Adds a new entry to the database.
        update_entry(filename, downloaded=True): Updates an entry in the database
        delete_entry(filename): Removes the entry from the database.
        check_entries(): Used to ensure that the db is showing accurate information
"""

    DB_NAME = "metadb.sqlite3"

    def __init__(self):
        self.setup()
    

    def setup(self):
        """Method used to setup the database"""

        with connect(self.DB_NAME) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS MetaTable (
                id INTEGER PRIMARY KEY,
                filename TEXT UNIQUE NOT NULL,
                date_created TEXT,
                last_downloaded TEXT,
                download_count INTEGER,
                last_viewed TEXT,
                view_count INTEGER);""")

            db.commit()

    def get_entry(self, filename:str) -> tuple | None:
        """Method used to get an entry from the database.
        
        Args:
            filename
            
        Returns:
            Tuple | None"""

        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM MetaTable WHERE filename = (?)", (filename,))
            row = cursor.fetchone()
        
        return row

    def get_entries(self) -> list[tuple] | None:
        """Method used to get all entries from the database.
        
        Returns:
            list[tuple] | None"""

        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM MetaTable")
            rows = cursor.fetchall()

        return rows

    def add_entry(self, filename:str) -> None:
        """Method which adds a new entry to the database.
        
        Args:
            filename (str): The name of the file that was uploaded.
        
        Returns:
            None"""

        with connect(self.DB_NAME) as db:
            db.execute("INSERT OR REPLACE INTO MetaTable (filename, date_created, last_downloaded, download_count, last_viewed, view_count) VALUES (?, datetime('now'), NULL, 0, NULL, 0)", (filename, ))
            db.commit()

        return None

    def update_entry(self, filename:str, downloaded:bool=True) -> None:
        """Method used to update or delete an entry. If downloaded is False, then assume the file was deleted.
        
        Args:
            filename (str): The name of the file to update.
            downloaded(bool): Whether the file was downloaded or viewed."""

        col1, col2 = ("download_count", "last_downloaded") if downloaded else ("view_count", "last_viewed")    

        with connect(self.DB_NAME) as db:
            cursor = db.execute(f"SELECT {col1} FROM MetaTable WHERE filename = ?", (filename, ))
            row = cursor.fetchone()
            print(row)
            db.execute(f"UPDATE MetaTable SET {col2} = datetime('now'), {col1} = ? WHERE filename = (?)", (row[0] + 1, filename))
            db.commit()

        return None

    def delete_entry(self, filename:str) -> None:
        """Method used to delete an entry from the database.
        
        Args:
            filename(str): The name of the file to be deleted."""

        with connect(self.DB_NAME) as db:
            db.execute("DELETE FROM MetaTable WHERE filename = (?)", (filename, ))
            db.commit()

        return None

    def check_entries(self) -> None:
        """Method to ensure that the database is showing accurate information"""
        print("Checking files...")
        files = listdir(UPLOAD_FOLDER)
        for filename in files:
            exists = self.get_entry(filename)
            if not exists:
                print(filename, "does not have meta information. Creating now.")
                self.add_entry(filename)          

        # Now we check the other way.
        for file in self.get_entries():
            if file[1] not in files:
                print(file[1], "does not seem to actually exist. Removing from database.")
                self.delete_entry(file[1])

        print("Checking Completed")  
