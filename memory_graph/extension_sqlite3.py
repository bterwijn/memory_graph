# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Numpy types. """
from memory_graph.node_key_value import Node_Key_Value
from memory_graph.node_table import Node_Table


import memory_graph.config as config
import memory_graph.config_default as config_default


class SQLite3_Table:
    def __init__(self, header, rows, column_types, primary_keys, foreign_keys):
        self.header = header
        self.rows = rows
        self.column_types = column_types
        self.primary_keys = primary_keys
        self.foreign_keys = foreign_keys


def get_table(conn, table_name):
    # Quote the table name safely
    name = '"' + table_name.replace('"', '""') + '"'

    cursor = conn.execute(f"SELECT * FROM {name}")
    header = [col[0] for col in cursor.description]
    rows = iter(cursor)  # lazy iteration
    # Column types: column name -> declared SQLite type
    # Primary keys: column name -> position in composite primary key
    column_info = list(conn.execute(f"PRAGMA table_info({name})"))
    column_types = {
        col[1]: col[2]
        for col in column_info
    }
    primary_keys = {
        col[1]: col[5]
        for col in column_info
        if col[5] > 0
    }
    # Foreign keys: (column, referenced table, referenced column)
    foreign_keys = [
        (fk[3], fk[2], fk[4])
        for fk in conn.execute(f"PRAGMA foreign_key_list({name})")
    ]
    return SQLite3_Table(
        header, rows, column_types, primary_keys, foreign_keys
    )


def get_tables(conn):
    table_names = (
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    )
    tables = {name: get_table(conn, name) for name in table_names}
    return tables


def sqlite_table_node(d):
    headers = []
    for name in d.header:
        labels = []
        # Declared SQLite column type
        column_type = d.column_types.get(name)
        if column_type:
            labels.append(column_type)
        # Primary key
        if name in d.primary_keys:
            labels.append("PK")
        # Foreign key
        if any(fk[0] == name for fk in d.foreign_keys):
            labels.append("FK")

        suffix = f" ({', '.join(labels)})" if labels else ""
        headers.append(name + suffix)
    return Node_Table(
        d,
        list(d.rows),
        col_names=headers
    )

def extend_sqlite3():
    import sqlite3

    config.type_to_node[sqlite3.Connection] = (
        lambda d: Node_Key_Value(d, get_tables(d).items())
    )
    config.type_to_node[SQLite3_Table] = sqlite_table_node

    config_default.type_to_color_light[SQLite3_Table] = "lightcyan"
    config_default.type_to_color_dark[SQLite3_Table] = "#2c4f52"

    if not config.color_mode_dark:
        config.type_to_color[SQLite3_Table] = config_default.type_to_color_light[SQLite3_Table]
    else:
        config.type_to_color[SQLite3_Table] = config_default.type_to_color_dark[SQLite3_Table]

def unextend_sqlite3():
    del config.type_to_node[SQLite3_Table]
    del config.type_to_color[SQLite3_Table]
