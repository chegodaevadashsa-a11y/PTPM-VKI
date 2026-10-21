
import sqlite3


class TriangleDatabase:
    def __init__(self, database_path=":memory:"):
        self.connection = sqlite3.connect(database_path)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                side_a REAL NOT NULL,
                side_b REAL NOT NULL,
                side_c REAL NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT,
                UNIQUE(side_a, side_b, side_c)
            )
        """)
        self.connection.commit()

    def get(self, a, b, c):
        row = self.connection.execute("""
            SELECT triangle_type, error_message
            FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (a, b, c)).fetchone()

        if row is None:
            return None

        return {"type": row[0], "error": row[1]}

    def add(self, a, b, c, result):
        self.connection.execute("""
            INSERT OR REPLACE INTO triangles
            (side_a, side_b, side_c, triangle_type, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (a, b, c, result["type"], result["error"]))
        self.connection.commit()

    def delete(self, a, b, c):
        cursor = self.connection.execute("""
            DELETE FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (a, b, c))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()
