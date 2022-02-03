from postgres import connect_postgres, close_postgres

def top_5_cities_by_search(search="jersey"):
  connection, cursor = connect_postgres()
  cursor.execute("SELECT * from us_cities where city iLIKE %(search)s or zips iLIKE %(search)s", {"search": f"%{search}%"})
  return cursor.fetchmany(5)
  close_postgres(connection, cursor)