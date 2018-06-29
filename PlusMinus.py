import pandas as pd
import numpy as np
from datetime import datetime

lineups = pd.read_csv("lineups.csv")
codes = pd.read_csv("Codes.csv")
playByPlay = pd.read_csv("PlayByPlay.csv")

relevantEvents = playByPlay[(playByPlay['Event_Msg_Type'] == 1) | (playByPlay['Event_Msg_Type'] == 8) | (playByPlay['Event_Msg_Type'] == 3) | \
(playByPlay['Event_Msg_Type'] == 12)]
relevantEvents = relevantEvents.sort_values(['Game_id', 'Period', 'PC_Time', 'Event_Msg_Type'], ascending = [True, True, False, True])
plusMinus_list = []
# players1 = pd.DataFrame(lineups[['Game_id', 'Person_id']])
# players1.columns = ['Game_id', 'Person1']
# plusMinus = pd.concat([relevantEvents[['Game_id', 'Person1']], players1]).groupby(['Game_id', 'Person1']).count().reset_index()
# plusMinus['Player_Plus/Minus'] = 0

class Lineup:
	def __init__(self, team, players):
		self.team = team
		self.players = players
	def swapPlayer(self, pOut, pIn):
		self.players[self.players.index(pOut)] = pIn
	def contains(self, player):
		return player in self.players


def changePlusMinus(Game_id, Event_Msg_Type, Period, Option1, Team_id, Person1, Person2, lineup1, lineup2):
	if (Event_Msg_Type == 1) or (Event_Msg_Type == 3 and Option1 == 1):
		scoringTeam = lineup1 if lineup1.contains(Person1) else lineup2
		againstTeam = lineup1 if lineup2.contains(Person1) else lineup2
		shotFor(Game_id, scoringTeam, Option1)
		shotAgainst(Game_id, againstTeam, Option1)
	elif Event_Msg_Type == 8:
		if lineup1.contains(Person1):
			lineup1.swapPlayer(Person1, Person2)
		elif lineup2.contains(Person1):
			lineup2.swapPlayer(Person1, Person2)
	elif Event_Msg_Type == 12:
		teams = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period)]['Team_id'].unique()
		lineup1.__init__(teams[0], lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & \
			(lineups['Team_id'] == teams[0])]['Person_id'].tolist())
		lineup2.__init__(teams[1], lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & \
			(lineups['Team_id'] == teams[1])]['Person_id'].tolist())

games = relevantEvents['Game_id'].unique()
#g = games[4]

#np.vectorize(changePlusMinus)(relevantEvents.loc[relevantEvents['Game_id'] == g]['Game_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Event_Msg_Type'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Period'],  \
#	relevantEvents.loc[relevantEvents['Game_id'] == g]['Option1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Team_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person2'])

def shotFor(Game_id, lineup, Option1):
	for person in lineup.players:
		plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': person, 'Player_Plus/Minus': Option1})

def shotAgainst(Game_id, lineup, Option1):
	for person in lineup.players:
		plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': person, 'Player_Plus/Minus': -1 * Option1})

start = datetime.now()
l1 = Lineup("", [])
l2 = Lineup("", [])
np.vectorize(changePlusMinus, otypes = [None])(relevantEvents['Game_id'], relevantEvents['Event_Msg_Type'], relevantEvents['Period'],  \
	relevantEvents['Option1'], relevantEvents['Team_id'], relevantEvents['Person1'], relevantEvents['Person2'], l1, l2)

plusMinus = pd.DataFrame(plusMinus_list).groupby(['Game_ID', 'Person_ID']).sum().reset_index()
print datetime.now() - start

























# def changePlusMinus(Game_id, Event_Msg_Type, Period, Option1, Team_id, Person1, Person2):
# 	if Event_Msg_Type == 1:
# 		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
# 		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
# 		np.vectorize(shotFor, otypes = [None])(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
# 		np.vectorize(shotAgainst, otypes = [None])(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
# 	elif Event_Msg_Type == 3 and Option1 == 1:
# 		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
# 		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
# 		np.vectorize(shotFor, otypes = [None])(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
# 		np.vectorize(shotAgainst, otypes = [None])(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
# 	elif Event_Msg_Type == 8:
# 		makeSubstitute(Game_id, Period, Person1, Person2)

# games = relevantEvents['Game_id'].unique()
# #g = games[4]

# #np.vectorize(changePlusMinus)(relevantEvents.loc[relevantEvents['Game_id'] == g]['Game_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Event_Msg_Type'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Period'],  \
# #	relevantEvents.loc[relevantEvents['Game_id'] == g]['Option1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Team_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person2'])

# def shotFor(Game_id, Person_id, Option1):
# 	plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': Person_id, 'Player_Plus/Minus': Option1})

# def shotAgainst(Game_id, Person_id, Option1):
# 	plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': Person_id, 'Player_Plus/Minus': -1 * Option1})

# def makeSubstitute(Game_id, Period, Person1, Person2):
# 	lineups.loc[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Person_id'] == Person1), 'Person_id'] = Person2

# start = datetime.now()
# np.vectorize(changePlusMinus, otypes = [None])(relevantEvents['Game_id'], relevantEvents['Event_Msg_Type'], relevantEvents['Period'],  \
# 	relevantEvents['Option1'], relevantEvents['Team_id'], relevantEvents['Person1'], relevantEvents['Person2'])

# plusMinus = pd.DataFrame(plusMinus_list).groupby(['Game_ID', 'Person_ID']).sum().reset_index()
# print datetime.now() - start
















































