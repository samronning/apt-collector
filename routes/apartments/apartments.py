from flask import request
from flask_restful import Resource

#mylibs
from .collector import get_page_data_by_area, get_all_data_by_area
from .apartments_com_parser import listing_parser

class AptList(Resource):
    def get(self):
        location = request.args.get('location')
        page = request.args.get('page')
        if location is None:
            return "Must specify a location", 400
        if page is None:
            raw = get_all_data_by_area(location)
            parsed = listing_parser(raw)
            return parsed, 200
        try:
            int(page)
        except:
            return "Invalid Page", 400
        if int(page) < 0:
            return "Invalid Page", 400
        try:
            raw = get_page_data_by_area(location, page)
            parsed = listing_parser(raw)
            return parsed, 200
        except Exception as inst:
            print("Exception!")
            return inst.args