import pandas as pd
import numpy as np
from datetime import datetime

lineups = pd.read_csv("lineups.csv")
codes = pd.read_csv("Codes.csv")
playByPlay = pd.read_csv("PlayByPlay.csv")

relevantEvents = playByPlay[(playByPlay['Event_Msg_Type'] == 1) | (playByPlay['Event_Msg_Type'] == 8) | (playByPlay['Event_Msg_Type'] == 3)]
relevantEvents = relevantEvents.sort_values(['Game_id', 'Period', 'PC_Time', 'Event_Msg_Type'], ascending = [True, True, False, True])
plusMinus_list = []
# players1 = pd.DataFrame(lineups[['Game_id', 'Person_id']])
# players1.columns = ['Game_id', 'Person1']
# plusMinus = pd.concat([relevantEvents[['Game_id', 'Person1']], players1]).groupby(['Game_id', 'Person1']).count().reset_index()
# plusMinus['Player_Plus/Minus'] = 0

class lineup:
	def __init__(team, players):
		self.team = team
		self.players = players

	def swapPlayer(pIn, pOut):
		self.players[self.players.index(pOut)] = pIn



def changePlusMinus(Game_id, Event_Msg_Type, Period, Option1, Team_id, Person1, Person2):
	if Event_Msg_Type == 1:
		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
		np.vectorize(shotFor, otypes = [None])(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
		np.vectorize(shotAgainst, otypes = [None])(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
	elif Event_Msg_Type == 3 and Option1 == 1:
		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
		np.vectorize(shotFor, otypes = [None])(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
		np.vectorize(shotAgainst, otypes = [None])(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
	elif Event_Msg_Type == 8:
		makeSubstitute(Game_id, Period, Person1, Person2)

games = relevantEvents['Game_id'].unique()
#g = games[4]

#np.vectorize(changePlusMinus)(relevantEvents.loc[relevantEvents['Game_id'] == g]['Game_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Event_Msg_Type'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Period'],  \
#	relevantEvents.loc[relevantEvents['Game_id'] == g]['Option1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Team_id'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person1'], relevantEvents.loc[relevantEvents['Game_id'] == g]['Person2'])

def shotFor(Game_id, Person_id, Option1):
	plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': Person_id, 'Player_Plus/Minus': Option1})

def shotAgainst(Game_id, Person_id, Option1):
	plusMinus_list.append({'Game_ID': Game_id, 'Person_ID': Person_id, 'Player_Plus/Minus': -1 * Option1})

def makeSubstitute(Game_id, Period, Person1, Person2):
	lineups.loc[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Person_id'] == Person1), 'Person_id'] = Person2

start = datetime.now()
np.vectorize(changePlusMinus, otypes = [None])(relevantEvents['Game_id'], relevantEvents['Event_Msg_Type'], relevantEvents['Period'],  \
	relevantEvents['Option1'], relevantEvents['Team_id'], relevantEvents['Person1'], relevantEvents['Person2'])

plusMinus = pd.DataFrame(plusMinus_list).groupby(['Game_ID', 'Person_ID']).sum().reset_index()
print datetime.now() - start






# def shotFor(Game_id, Person_id, Option1):
# 	plusMinus.loc[(plusMinus['Game_id'] == Game_id) & (plusMinus['Person1'] == Person_id), 'Player_Plus/Minus'] += Option1

# def shotAgainst(Game_id, Person_id, Option1):
# 	plusMinus.loc[(plusMinus['Game_id'] == Game_id) & (plusMinus['Person1'] == Person_id), 'Player_Plus/Minus'] -= Option1

# def makeSubstitute(Game_id, Period, Person1, Person2):
# 	lineups.loc[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Person_id'] == Person1), 'Person_id'] = Person2

# start = datetime.now()
# np.vectorize(changePlusMinus, otypes = [None])(relevantEvents['Game_id'], relevantEvents['Event_Msg_Type'], relevantEvents['Period'],  \
# 	relevantEvents['Option1'], relevantEvents['Team_id'], relevantEvents['Person1'], relevantEvents['Person2'])
# print datetime.now() - start













































