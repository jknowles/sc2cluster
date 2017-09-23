# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:08:18 2017

@author: jknow
"""

def read_sc2_replay(path, track_type = None):
    if track_type is None:
        track_type = "details -gameevts -trackerevts -msgevts -attrevts"
    # modify value here
    import os
    os_call = "inst\\s2prot.exe -" + track_type + " " + path + " > tmp.json"
    print(os_call)
    #os.system("inst\s2prot.exe -trackerevts data/rep1.SC2Replay > test.json")
    os.system(os_call)
    print("Temporary json written to " + os.getcwd() + "\\tmp.json")
    
def read_sc1_replay(path, track_type = None):
    if track_type is None:
        track_type = "-map -cmds -mapres"
    os_call = "inst\\screp.exe \-" + track_type + " " + path + " > tmp.json"
    #os.system("inst\s2prot.exe -trackerevts data/rep1.SC2Replay > test.json")
    print(os_call)

def parse_sc2_json(json_file):
    import json
    json_data = open(json_file)
    replay_dict = json.load(json_data)
    return(replay_dict)
