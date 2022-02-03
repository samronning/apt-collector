import os
import psycopg2
from psycopg2 import Error

def connect_postgres():
  password = os.environ.get("pgpass")
  try:
      # Connect to an existing database
      connection = psycopg2.connect(user="postgres",
                                    password=password,
                                    host="localhost",
                                    port="5432",
                                    database="postgres")

      # Create a cursor to perform database operations
      cursor = connection.cursor()
      # Print PostgreSQL details
      print("Connected to postgres...")
      return connection, cursor

  except (Exception, Error) as error:
      print("Error while connecting to PostgreSQL", error)

def close_postgres(connection, cursor):
    if (connection, cursor):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
