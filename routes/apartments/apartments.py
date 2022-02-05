from flask import request
from flask_restful import Resource
import json

#mylibs
from .collector import get_page_data_by_area, get_all_data_by_area
from .apartments_com_parser import listing_parser

class AptList(Resource):
    def __init__(self, r):
        self.r = r


    def get(self):
        location = request.args.get('location')
        page = request.args.get('page')
        #data is stale after 24 hours
        timeout = 60 * 60 * 12
        if location is None:
            return "Must specify a location", 400
        if page is None:
            if self.r.exists(location):
                return json.loads(self.r.get(location)), 200
            raw = get_all_data_by_area(location)
            parsed = listing_parser(raw)
            self.r.setex(location, timeout, json.dumps(parsed))
            return parsed, 200
        try:
            int(page)
        except:
            return "Invalid Page", 400
        if int(page) < 0:
            return "Invalid Page", 400
        try:
            rediskey = f"{location}-{page}"
            if self.r.exists(rediskey):
                return json.loads(self.r.get(rediskey))
            raw = get_page_data_by_area(location, page)
            parsed = listing_parser(raw)
            self.r.setex(rediskey, timeout, json.dumps(parsed))
            return parsed, 200
        except Exception as inst:
            print("Exception!")
            return inst.args