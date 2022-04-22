"""File used to manage the database which handles the meta information for files."""

from sqlite3 import connect



class Database:
    """Class used to manage the Database.
    
    Attrs:
        DB_NAME (str)

    Methods:
        setup(): Sets up the database
        get_entry(filename): Gets an entry from the database
        get_entries(): Gets all entries from the database
        add_entry(filename): Adds a new entry to the database.
        update_entry(filename, downloaded=True): Updates or deletes an entry to the database
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
                download_count INTEGER);""")

            db.commit()

    def get_entry(self, filename:str) -> tuple | None:
        """Method used to get an entry from the database.
        
        Args:
            filename
            
        Returns:
            Tuple | None"""

        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM MetaTable WHERE filename = ?", (filename,))
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
            db.execute("INSERT OR REPLACE INTO MetaTable (filename, date_created, last_downloaded, download_count) VALUES (?, datetime('now'), NULL, 0)", (filename, ))
            db.commit()

        return None

    def update_entry(self, filename:str, downloaded:bool=True) -> None:
        """Method used to update or delete an entry. If downloaded is False, then assume the file was deleted.
        
        Args:
            filename (str): The name of the file to update.
            downloaded(bool): Whether the file was downloaded or not."""

        with open(self.DB_NAME) as db:
            if downloaded:
                cursor = db.execute("SELECT download_count FROM MetaTable WHERE filename = ?", (filename, ))
                row = cursor.fetchone()
                db.execute("UPDATE MetaTable SET last_downloaded = datetime('now'), download_count = ? WHERE filename = ?", (row[0], filename))
            else:
                db.execute("DELETE FROM MetaTable WHERE filename = ?", (filename, ))
            db.commit()

        return None
