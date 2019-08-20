#!/usr/bin/env python3
"""convert sparql outputs to json files for resource agent initialization"""
# watch out: no error handling implemented!

import csv
import json

CAPACITIES = "queryingPAonto/ra-freeCapa.csv"
CAPABILITIES = "queryingPAonto/ra-feats.csv"

class Resource(dict):
    """class to represent resources with their capabilities"""
    def __init__(self, name, freecapa):
        self.name = name
        self.freecapa = freecapa,
        self.features = {}
    def add_feature(self, feature):
        self.features.update(feature)

class Feature(dict):
    """class to represent a feature and the processes it can be realized with"""
    def __init__(self, name):
        self["name"] = {"processes": {}}
        self[name] = self.pop("name")

class Process(dict):
    """class to represent a process and its duration"""
    def __init__(self, name, rc):
        self["name"] = rc
        self[name] = self.pop("name")

def csv_to_array(file_path):
    """import data from csv and return as array"""
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        return list(csv_reader)

def return_capacities(array):
    """return dict with capacities of resources"""
    resourcelist = []
    for i in range(1, len(array)):
        if array[i][0] != array[i-1][0]:
            resourcelist.append(Resource(array[i][0].split("#")[-1], array[i][1]))
    return resourcelist

def return_capabilities(array, resourcelist):
    """return dict with capabilities of resources"""
    for i in range(len(resourcelist)):
        for j in range(1, len(array)):
            resource = array[j][0].split("#")[-1]
            feat = array[j][1].split("#")[-1]
            proc = array[j][2].split("#")[-1]
            if resource == resourcelist[i].name and\
             feat not in resourcelist[i].features:
                resourcelist[i].add_feature(Feature(feat))
            for k in range(len(resourcelist[i].features)):
                if resource == resourcelist[i].name and\
                 feat in resourcelist[i].features and\
                 proc not in resourcelist[i].features[feat]["processes"]:
                    resourcelist[i].features[feat]["processes"].\
                     update(Process(proc, array[j][3]))
    return resourcelist

def main():
    """read information from csv sparql output and save to json"""
    resourcelist = return_capabilities(csv_to_array(CAPABILITIES),\
     return_capacities(csv_to_array(CAPACITIES)))
    for i in range(len(resourcelist)):
        file = open("%s.json" % resourcelist[i].name, "w")
        file.write(json.dumps({"freeCapacity": resourcelist[i].freecapa,\
         "capabilities": resourcelist[i].features}, indent=2))
        file.close()

main()
