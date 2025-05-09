import sqlite3
from typing import List, Tuple, Any, Optional
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "database.db"):
        """Initialize the database manager with the given database path."""
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Establish connection to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to database: {e}")

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def create_table(self, table_name: str, columns: List[str]) -> None:
        """
        Create a new table in the database.
        
        Args:
            table_name: Name of the table to create
            columns: List of column definitions (e.g., ["id INTEGER PRIMARY KEY", "name TEXT"])
        """
        if not self.connection:
            self.connect()
        
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, table_name: str, data: dict) -> int:
        """
        Insert a new record into the specified table.
        
        Args:
            table_name: Name of the table to insert into
            data: Dictionary of column names and values to insert
            
        Returns:
            The ID of the inserted row
        """
        if not self.connection:
            self.connect()
        
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        self.cursor.execute(query, list(data.values()))
        self.connection.commit()
        return self.cursor.lastrowid

    def select(self, table_name: str, columns: List[str] = None, 
              where: str = None, params: Tuple = None) -> List[Tuple]:
        """
        Select records from the specified table.
        
        Args:
            table_name: Name of the table to select from
            columns: List of columns to select (None for all columns)
            where: WHERE clause (optional)
            params: Parameters for the WHERE clause
            
        Returns:
            List of tuples containing the selected records
        """
        if not self.connection:
            self.connect()
        
        columns_str = ", ".join(columns) if columns else "*"
        query = f"SELECT {columns_str} FROM {table_name}"
        
        if where:
            query += f" WHERE {where}"
            
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def update(self, table_name: str, data: dict, where: str, params: Tuple) -> int:
        """
        Update records in the specified table.
        
        Args:
            table_name: Name of the table to update
            data: Dictionary of column names and new values
            where: WHERE clause
            params: Parameters for the WHERE clause
            
        Returns:
            Number of rows affected
        """
        if not self.connection:
            self.connect()
        
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        print("set_clause: ", set_clause)
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        print("query: ", query)
        all_params = list(data.values()) + list(params)
        self.cursor.execute(query, all_params)
        self.connection.commit()
        return self.cursor.rowcount

    def delete(self, table_name: str, where: str, params: Tuple) -> int:
        """
        Delete records from the specified table.
        
        Args:
            table_name: Name of the table to delete from
            where: WHERE clause
            params: Parameters for the WHERE clause
            
        Returns:
            Number of rows affected
        """
        if not self.connection:
            self.connect()
        
        query = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.rowcount

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
