from flask import Flask
from flask_restful import Api
import pandas as pd

# mylibs
from routes.apartments.apartments import AptList
from routes.cities import CitySearch

app = Flask(__name__)
api = Api(app)

api.add_resource(AptList, '/apartments/list')
api.add_resource(CitySearch, '/cities')
app.run()
