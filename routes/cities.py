from .postgres import connect_postgres, close_postgres
from flask import request
from flask_restful import Resource

def top_5_cities_by_search(search="jersey"):
  connection, cursor = connect_postgres()
  cursor.execute("SELECT * from us_cities where city iLIKE %(search)s or zips iLIKE %(search)s", {"search": f"{search}%"})
  return cursor.fetchmany(5)
  close_postgres(connection, cursor)

class CitySearch(Resource):
  def get(self):
    search = request.args.get('search')
    try:
      result = top_5_cities_by_search(search)
      return result, 200
    except:
        return "Internal Server Error", 500
