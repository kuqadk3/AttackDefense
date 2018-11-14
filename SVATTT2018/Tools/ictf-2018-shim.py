#!/usr/bin/env python3
from flask import Flask
from flask_restful import Resource, Api, reqparse
from elasticsearch import Elasticsearch
from swpag_client import Team
import time
import re

app = Flask(__name__)
api = Api(app)

es_index = "submissions"

class targets(Resource):
    def get(self,service):
        t = Team(None, "API_KEY")
        status = t.get_game_status()
        ownscore = status['scores']['151']['total_points']
        result = []
        top_ten = sorted([team['total_points'] for team in status['scores'].values()], reverse = True)[10]

        for target in t.get_targets(service):
            team_id = target['hostname'][4:]
            if status['scores'][team_id]['total_points'] > ownscore or status['scores'][team_id]['total_points'] >top_ten:
                result.append(target)
        return result

class flag(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('author', type=str ,required=True)
        parser.add_argument('scriptname', type=str ,required=True)
        parser.add_argument('service', type=str ,required=True)
        parser.add_argument('flag', type=str ,required=True)
        parser.add_argument('target', type=str ,required=True)
        args = parser.parse_args()
        es=Elasticsearch()

        if(es.search(index=es_index, body={"query": {"term" : {"flag" : args['flag']}}})['hits']['total'] > 0):
            result = "ALREADY_SUBMITTED"
        else:
            try:
                result = self.validate_flag(args)
            except:
                result = "DUNNO"
                pass
        doc = args
        doc['result'] = result
        doc['timestamp'] = time.time()
        es.index(index=es_index, doc_type='flags', body=doc)
        return  result

    def validate_flag(self,args):
        t = Team(None, "API_KEY")
        return t.submit_flag([args['flag']])



api.add_resource(targets, '/targets/<int:service>')
api.add_resource(flag, '/flag')

if __name__ == '__main__':
    app.run(debug=True)
