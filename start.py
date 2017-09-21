import os

os.getcwd()
os.chdir(".\\Github\\sc2cluster")
os.system("inst\s2prot.exe -gameevts data/rep1.SC2Replay > test.json")

import json
from pprint import pprint
json_data = open('test.json')
parsed_json = json.load(json_data)
json_data.close()



list(parsed_json.keys())

parsed_json['Header']
# A nested dictionary has keys
parsed_json['Header'].keys()



parsed_json['Metadata']['Struct']['Players']

parsed_json['GameEvts'][5:6]

parsed_json['GameEvts', 'loop' = '822']
list(parsed_json.keys())
list(parsed_json.values())

parsed_json.keys()
parsed_json.values()


parsed_json['GameEvts'][3]['Name']
indices = [i for i, x in enumerate(parsed_json['GameEvts']) if x == "Name"]



