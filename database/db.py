import sqlite3


class IntegrityError(Exception):
    """
    Custom error for duplicate voting.
    """
    pass


class Database:
    """
    SQLite database class for voting system.
    """

    def __init__(self, db_path: str = "database/votes.db") -> None:
        """
        Initiates the Database class and creates database tables
        """
        self.db_path = db_path
        self.create_tables()

    def create_tables(self) -> None:
        """
        Creates votes table with structure:
        id (Primary key), user_id (integer, unique), candidate (Text)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER UNIQUE, 
                    candidate TEXT
                )
            """)
            conn.commit()

    def get_user_vote(self, user_id: int) -> tuple | None:
        """
        Returns a database record for user_id or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM votes WHERE user_id = ?", (user_id,))
            return cursor.fetchone()

    def add_vote(self, user_id: int, candidate: str) -> None:
        """
        Inserts a vote for candidate. If user_id already votes raises an error
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO votes (user_id, candidate) VALUES (?, ?)",
                               (user_id, candidate))
                conn.commit()
            except sqlite3.IntegrityError:
                raise IntegrityError(f"User with id {user_id} already voted.")

    def count_votes(self) -> dict:
        """
        Returns a dictionary: {candidate_name: votes_count}
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
            rows = cursor.fetchall()

            return {candidate: count for candidate, count in rows}
