import memory_graph as mg
import sqlite3
mg.extend_sqlite3()

conn = sqlite3.connect(":memory:")

conn.executescript("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    );
""")

conn.executemany(
    "INSERT INTO students VALUES (?, ?, ?)",
    [
        (1, "Alice", 20),
        (2, "Bob", 21),
        (3, "Charlie", 22),
    ]
)

mg.render( locals(), "extension_sqlite3.png")
conn.close()
