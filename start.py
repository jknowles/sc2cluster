# Imports
import os
import json
import pandas as pd

import parse_sc2

parse_sc2.read_sc2_replay("data/rep2.SC2Replay")
replay_dict = parse_sc2.parse_sc2_json("tmp.json")
replay_dataframes = parse_sc2.org_sc2_dict(replay_dict)


output = replay_dataframes['players']

map_title = replay_dataframes['details']['title']
game_time = parse_sc2.get_maptime(replay_dataframes['details']['timeUTC'])
game_version = replay_dataframes['header']['version']['major'] + (replay_dataframes['header']['version']['minor']/100 )


spawn_location = parse_sc2.get_spawn_location(replay_dataframes['tracker'])

player_data = replay_dataframes['players']

# Get spawn locations
# Get metadata for matchup -- patch, etc


plotdf = replay_dataframes['tracker']
zzz = parse_sc2.get_first_unit_time(plotdf, unitList = ['Nexus', 'CommandCenter', 'Hatchery'])
parse_sc2.get_first_unit_time(plotdf, unitList = ['EngineeringBay', 'Forge', 'EvolutionChamber'])
parse_sc2.get_first_unit_time(plotdf, unitList = ['Spire', 'Stargate', 'Starport'])
parse_sc2.get_first_unit_time(plotdf, unitList = ['Refinery', 'Extractor', 'Assimilator'])
parse_sc2.get_first_unit_time(plotdf, unitList = ['Factory', 'RoboticsFacility', 'RoachWarren'])


#plotdf = replay_dataframes["stats"]
#plotdf = replay_dataframes["gameevent"]
#plotdf = replay_dataframes["tracker"]



# Do this by player, get minimum loop value

myvalues = {'unitTypeName': ['Barracks', 'Gateway', 'SpawningPool']}



plotdf = plotdf[plotdf['unitTypeName'].isin(["Barracks", "Gateway", "SpawningPool"])]
plotdf.groupby('controlPlayerId')['loop'].min()






unitList = ['Refinery', 'Extractor', 'Assimilator']
parse_sc2.get_timings(plotdf, unitStub = "gasTiming", unitList = unitList, n = 4)
unitList = ['Nexus', 'CommandCenter', 'Hatchery']
parse_sc2.get_timings(plotdf, unitStub = "townHallTiming", unitList = unitList, n = 2)




plotdf = plotdf[plotdf['unitTypeName'].isin(unitList)]
out = plotdf.groupby('controlPlayerId')['loop'].unique()
out = pd.DataFrame(out)

out = out.loop.apply(pd.Series)
out = out.reset_index()
["gasTiming_" + s  for s in [str(x) for x in range(1, 8)]]
out.columns = [["playerId"] + ["gasTiming_" + s  for s in [str(x) for x in range(1, 8)]]]

# Write a function to get stats at certain values
l = list(range(1,22))
l = [480*x for x in l]


def get_econ_timing(data, timeList, var):
    data = data[data['loop'].isin(timeList)]
    var = ['playerId', 'loop'] + var
    data = data.loc[:,var]
    data = pd.wide_to_long(data, ["scoreValue"], i=["playerId", 'loop'], j="score", 
                 suffix = "\\D+")
    data.reset_index(inplace=True)  
    return(data)



scoreIndex = ['scoreValueMineralsUsedCurrentEconomy', 
              'scoreValueVespeneUsedCurrentEconomy', 
              'scoreValueWorkersActiveCount', 
              'scoreValueFoodMade', 
              'scoreValueFoodUsed',
              'scoreValueMineralsUsedCurrentTechnology',
              'scoreValueVespeneLostArmy', 
              'scoreValueMineralsLostArmy',
              'scoreValueVespeneKilledArmy', 
              'scoreValueMineralsKilledArmy']


plotdf = replay_dataframes["stats"]
zzz = get_econ_timing(plotdf, timeList = l, var = scoreIndex)

zzz = zzz.pivot_table(index = 'playerId', columns = ['score', 'loop'])
zzz = zzz.reset_index(inplace=True)





# Loop < 5760 = first 6 minutes of the game
# For each player we want to create a dataset with attributes like

# Player race
# Opponent race
# Spawn location (top, bottom)
# Map
# Map size
# Time of first barracks, spawning pool, gateway

# Time of first spire, stargate, starport
# Time of first robotics, factory, or roach warren /hydralisk den?
# 
# Time of first expansion
# Time of second expansion
# Time of first gas
# Time of second gas geyser
# Time of third gas geyser
# Supply at increments of 30 seconds
# Damage taken at increments of 30 seconds






















### Exploratory stuff
replay_dict['GameEvts'][320:321]
replay_dict['Details']['Struct']['timeUTC']
replay_dict['Details']['Struct']['timeLocalOffset']

# Game Event Data

ge_df = pd.DataFrame(replay_dict['GameEvts'])
ge_df = pd.concat([ge_df.loc[:,['ID','Name']], ge_df['Struct'].apply(pd.Series)], 
                    axis = 1)
# pd.value_counts(ge_df['name'])
# Game events contains camera updates, user selections, 
# pings
# control group updates
# Probably joins with te_df by loop
# What defines a unique row here?

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

# te_df contains tracker data

# contains
# UnitBorn UnitDied
# PlayerStats
# Upgrade
# Unit Positions
# pd.DataFrame.hist(ge_df, column = "loop")
# can join with loop as the primary key to ge_df
# What defines a unique row here?

# Player data
player_df = pd.DataFrame(replay_dict['Metadata']['Struct']['Players'])

#ATTR
# I think this has something to do with map destructibles, etc.
#attr_df = pd.DataFrame(replay_dict['AttrEvts']['Struct'])
#attr_df2 = attr_df['scopes'].apply(pd.Series)
#

# MEssage events are ping events and chat events
# Details, metadata, and header are replay wide information

# Clean up dataframes
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


zzz = ge_df[(ge_df.Name == "Cmd")]
zzz = zzz[['ID', 'abil', 'cmdFlags', 'controlId', 'data', 'id', 
          'loop', 'userid']]

zzz['abil'].apply(pd.Series)
zzz['data'].apply(pd.Series)


te_df = pd.concat([te_df.loc[:,['ID','Name']], te_df['Struct'].apply(pd.Series)], 
                    axis = 1)


# Loop < 5760 = first 6 minutes of the game
# For each player we want to create a dataset with attributes like

# Player race
# Opponent race
# Spawn location (top, bottom)
# Map
# Map size
# Time of first barracks, spawning pool, gateway
# Time of first spire, stargate, starport
# Time of first robotics, factory, or roach warren /hydralisk den?
# 
# Time of first expansion
# Time of second expansion
# Time of first gas
# Time of second gas geyser
# Time of third gas geyser
# Supply at increments of 30 seconds
# Damage taken at increments of 30 seconds


# Loop is recorded as frames, the replay keeps 16 frames per second
te_df[te_df.unitTagIndex == 642].unitTypeName
#pd.value_counts(te_df['name'])
# plotdf = te_df[te_df.name == "UnitBorn"]
# plotdf = te_df[te_df.name == "UnitInit"]
# plotdf = te_df[te_df.name == "UnitDone"]
#pd.value_counts(plotdf['creatorAbilityName'])
#plotdf = stats_df[(stats_df.Name == "PlayerStats")]
#
#import matplotlib.pyplot as plt
#
#fig, ax = plt.subplots()
#ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
#for name, group in plotdf.groupby('playerId'):
#    ax.plot(group.loop, group.scoreValueVespeneKilledArmy, 
#            linestyle='-', ms=12, label=name)
#ax.legend()
#plt.show()
#
#
#fig, ax = plt.subplots()
#ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
#for name, group in plotdf.groupby('playerId'):
#    ax.plot(group.loop, group.scoreValueVespeneKilledArmy, 
#            linestyle='-', ms=12, label=name)
#ax.legend()
#plt.show()



# Find the wd
os.getcwd()
# os.chdir(".\\Github\\sc2cluster")
# Change to the right wd
os.chdir(".\\Documents\\GitHub\\sc2cluster")

# Dump the replay file to a json text file
os.system("inst\s2prot.exe -trackerevts data/rep1.SC2Replay > test.json")

json_data = open('test.json')
replay_dict = json.load(json_data)
json_data.close()

list(replay_dict.keys())
replay_dict['Header']
# A nested dictionary has keys
replay_dict['Header'].keys()
replay_dict['Metadata']['Struct']['Players']
replay_dict['TrackerEvts'].keys()

replay_dict['TrackerEvts']['PIDPlayerDescMap']
replay_dict['TrackerEvts']['Evts']

# Convert to a panda dataframe
#
test_df = pd.DataFrame(replay_dict['TrackerEvts']['Evts'])
# Expand the struct into multiple columns, filling in empty values
out_df = pd.concat([test_df.loc[:,['ID','Name']], test_df['Struct'].apply(pd.Series)], 
                    axis = 1)
# expand_df = test_df['Struct'].apply(pd.Series)

# Let's append some header data here now
pd.DataFrame(replay_dict['Metadata']['Struct']['Players'])


out_df2 = pd.merge(out_df, pd.DataFrame(replay_dict['Metadata']['Struct']['Players']), 
                   left_on = "playerId", right_on = "PlayerID", how = "left")

# Explode out the stats attribute

stats_df = out_df['stats'].apply(pd.Series)

out_df2 = pd.concat([out_df2, stats_df], axis = 1)


# Clean up the resulting objects
del out_df
del replay_dict
del test_df
del stats_df
del out_df2['stats']
del out_df2[0]


#replay_dict['TrackerEvts']['Evts'].keys()

#parsed_json['GameEvts'][5:6]
#parsed_json['GameEvts', 'loop' = '822']
#list(parsed_json.keys())
#list(parsed_json.values())
#parsed_json.keys()
#parsed_json.values()
#parsed_json['GameEvts'][3]['Name']
#indices = [i for i, x in enumerate(parsed_json['GameEvts']) if x == "Name"]

#
#
## Alternative sc2protocol
#import mpyq
#
## Using mpyq, load the replay file.
#archive = mpyq.MPQArchive('data/rep1.SC2Replay')
#contents = archive.header['user_data_header']['content']
#
## Now parse the header information.
#from s2protocol import versions
#header = versions.latest().decode_replay_header(contents)