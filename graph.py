import re
from py2neo import Graph
import json
from flask import render_template

graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))

class Connect():
    def __init__(self):
        self.query = ""

    def run(self):
        return graph.run(self.query).data()

    def run_query(self):
        result = graph.run(self.query)
        ls = []
        try:
            result.forward()
            if type(result.current[0]) == str:
                ls.append(result.current[0])
            else:
                ls.append(result.current[0]["name"])
                while result.forward():
                    if result.current[0]:
                        ls.append(result.current[0]["name"])
            return ls
        except TypeError:
            return None

    def get_company_list(self):
        query = "MATCH (c: Institution) RETURN c"
        ls = []
        result = graph.run(query)
        while result.forward():
            if result.current[0]:
                ls.append(result.current[0]["name"])
        return ls

    def get_service_list(self):
        query = "MATCH (c: Service) RETURN c"
        ls = []
        result = graph.run(query)
        while result.forward():
            if result.current[0]:
                ls.append(result.current[0]["name"])
        return ls
    
