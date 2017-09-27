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

def org_sc2_dict(replay_dict):
    import pandas as pd
    # Game Event Data
    ge_df = pd.DataFrame(replay_dict['GameEvts'])
    ge_df = pd.concat([ge_df.loc[:,['ID','Name']], ge_df['Struct'].apply(pd.Series)], 
                    axis = 1)
    # Tracker data
    te_df = pd.DataFrame(replay_dict['TrackerEvts']['Evts'])
    # Expand the struct into multiple columns, filling in empty values
    te_df = pd.concat([te_df.loc[:,['ID','Name']], te_df['Struct'].apply(pd.Series)], 
                    axis = 1)
    # Explode out the stats attribute
    stats_df = te_df['stats'].apply(pd.Series)
    stats_df = pd.concat([te_df.loc[:,['ID', 'Name', 'loop', 'playerId']], stats_df], axis = 1)
    del stats_df[0]
    stats_df = stats_df.sort_values(by = "loop")
    # Subset to only take playerstats in this frame
    stats_df = stats_df[stats_df.Name == "PlayerStats"]
    
    te_df = te_df[te_df.Name != "PlayerStats"]
    # te_df contains tracker data
    # Player data
    player_df = pd.DataFrame(replay_dict['Metadata']['Struct']['Players'])
    ge_df.drop(['baseBuildNum', 'buildNum', 'debugPauseEnabled', 'developmentCheatsEnabled', 
            'gameFullyDownloaded', 'hotkeyProfile', 'multiplayerCheatsEnabled', 
            'syncChecksummingEnabled', 'platformMac', 'testCheatsEnabled', 
            'versionFlags', 'useGalaxyAsserts'], axis=1, inplace=True)

    replay_dataframes = {}
    replay_dataframes['header'] = replay_dict['Header']['Struct']
    replay_dataframes['details'] = replay_dict['Details']['Struct']
    replay_dataframes['players'] = player_df
    replay_dataframes['tracker'] = te_df
    replay_dataframes['gameevent'] = ge_df
    replay_dataframes['stats'] = stats_df
    return(replay_dataframes)


def get_timings(data, unitStub, unitList, n):
    import pandas as pd
    data = data[data['unitTypeName'].isin(unitList)]
    data = data[(data['loop'] >0)]
    data = data.groupby('controlPlayerId')['loop'].unique()
    data = pd.DataFrame(data)
    data = data.loop.apply(pd.Series)
    data = pd.DataFrame(data)
    data = data.reset_index()
    data = data.iloc[:, 0:n+1]
    colNames = [['playerId'] + 
                [unitStub + s for s in [str(x) for x in range(1, len(data.columns))]]]
    data.columns = colNames
    return(data)


def get_first_unit_time(data, unitList, name = None):
    if name is None:
        name = "unitTime"
    import pandas as pd
    data = data[data['unitTypeName'].isin(unitList)]
    data = data[(data['loop'] >0)]
    data = data.groupby('controlPlayerId')['loop'].min()
    data = pd.DataFrame(data)
    data = data.reset_index()
    data.columns = ['playerId', name]
    return(data)


def get_spawn_location(data):
    unitList = ['CommandCenter', 'Hatchery', 'Nexus']
    data = data[data['unitTypeName'].isin(unitList)]
    data = data[(data['loop']) < 200]
    data = data[['controlPlayerId', 'x', 'y']]
    return(data)



def get_maptime(ts):
    # Time conversion notes https://www.powershelladmin.com/wiki/Convert_between_Windows_and_Unix_epoch_with_Python_and_Perl
    from datetime import datetime as dt
    ts = ts / 10000000 # from nanoseconds to seconds
    ts = ts - 11644473600 # offset for Windows
    return(dt.fromtimestamp(ts))
    
