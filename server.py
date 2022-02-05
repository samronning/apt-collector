from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import pandas as pd

# mylibs
from routes.apartments.apartments import AptList
from routes.cities import CitySearch

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(AptList, '/apartments/list')
api.add_resource(CitySearch, '/cities')
app.run()
