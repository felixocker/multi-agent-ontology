#!/usr/bin/env python3
"""convert sparql outputs to json files for automata initialization"""
# watch out: no error handling implemented!

import csv
import json

STATES = "queryingPAonto/pa-states.csv"
TRANSITIONS = "queryingPAonto/pa-transitions.csv"

class Spec(object):
    """specification class combines states and transitions"""
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline
        self.position = None
        self.states = {}
        self.transitions = {}
    def add_state(self, state):
        """add state entry to self.states"""
        self.states.update(state)
    def add_transition(self, transition):
        """add transition entry to self.transitions"""
        self.transitions.update(transition)

class State(dict):
    """class for automaton states"""
    def __init__(self, name, feat):
        self["name"] = {"desiredPhysicalProperty": None,
                        "guards": {
                            "localDeadlineConstraint": None,
                            "customerDeadlineConstraint": None,
                            "qualityConstraint": None},
                        "initialState": False,
                        "finalState": False}
        self[name] = self.pop("name")
        self[name]["desiredPhysicalProperty"] = feat

class Process(dict):
    """class for process to represent valid transitions"""
    def __init__(self, name):
        self["name"] = {"possibleResources": []}
        self[name] = self.pop("name")

class Transition(dict):
    """class for automaton transitions"""
    def __init__(self, name, parent, child):
        self["name"] = {"parent": None,
                        "child": None,
                        "programCall": {},
                        "invariants": {
                            "localDeadlineConstraint": None,
                            "customerDeadlineConstraint": None,
                            "qualityConstraint": None},
                        "resets": {
                            "powerUsage": None}}
        self[name] = self.pop("name")
        self[name]["parent"] = parent
        self[name]["child"] = child

def csv_to_array(file_path):
    """import data from csv and return as array"""
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        return list(csv_reader)

def return_states(array):
    """restructure state information from csv acc. to class State"""
    speclist = []
    for i in range(1, len(array)):
        if array[i][0] != array[i-1][0]:
            # ensure that the spec has not been added already
            filename = array[i][0].split("#")[1]
            deadline = array[i][1]
            speclist.append(Spec(filename, deadline))
            for j in range(1, len(array)):
                # iterate over states
                if array[j][0] == array[i][0]:
                    speclist[-1].add_state(State(array[j][2].split("#")[1],\
                     array[j][2].split("#")[1]))
        speclist[-1].states["start"]["initialState"] = True
        speclist[-1].states["end"]["finalState"] = True
    return speclist

def return_transitions(array, speclist):
    """restructure transition information from csv acc. to class Transition"""
    for i in range(1, len(array)):
        spec = array[i][0].split("#")[1]
        new_t_name = "run" + array[i][1].split("#")[1] + array[i][2].split("#")[1]
        for j in range(len(speclist)):
            if speclist[j].name == spec and\
             new_t_name not in speclist[j].transitions:
                speclist[j].add_transition(Transition(new_t_name,\
                 array[i][1].split("#")[1],\
                 array[i][2].split("#")[1]))
                for k in range(i, len(array)):
                    process_name = None
                    # break if there is a change in spec, feat1 or feat2
                    if array[k][0] != array[i][0] or\
                     array[k][1] != array[i][1] or\
                     array[k][2] != array[i][2]:
                        break
                    # create a new process
                    if k == i or array[k][3] != array[i][3]:
                        process_name = array[k][3].split("#")[1]
                        if process_name not in speclist[j].transitions[new_t_name]["programCall"]:
                            process = Process(process_name)
                            speclist[j].transitions[new_t_name]["programCall"].update(process)
                            for l in range(k, len(array)):
                                # break if change in spec, feats, proc
                                if array[l][0] != array[k][0] or\
                                 array[l][1] != array[k][1] or\
                                 array[l][2] != array[k][2] or\
                                 array[l][3] != array[k][3]:
                                    break
                                process[process_name]["possibleResources"].\
                                 append(array[l][4].split("#")[1])
                            speclist[j].transitions[new_t_name]["programCall"].update(process)
    return speclist

def main():
    """read information from csv sparql output and save to json"""
    speclist = return_transitions(csv_to_array(TRANSITIONS),\
     return_states(csv_to_array(STATES)))
    for i in range(len(speclist)):
        file = open("%s.json" % speclist[i].name, "w")
        file.write(json.dumps({"globalDeadline": speclist[i].deadline,\
         "currentPosition": speclist[i].position,\
         "states": speclist[i].states,\
         "transitions": speclist[i].transitions}, indent=2))
        file.close()

main()
