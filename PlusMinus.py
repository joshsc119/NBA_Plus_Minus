import pandas as pd
import numpy as np

lineups = pd.read_csv("lineups.csv")
codes = pd.read_csv("Codes.csv")
playByPlay = pd.read_csv("PlayByPlay.csv")

relevantEvents = playByPlay[(playByPlay['Event_Msg_Type'] == 1) | (playByPlay['Event_Msg_Type'] == 8) | (playByPlay['Event_Msg_Type'] == 3)]


plusMinus = pd.DataFrame(lineups.groupby(['Game_id', 'Person_id']).count().reset_index()[['Game_id', 'Person_id']])
plusMinus['Player_Plus/Minus'] = 0


relevantEvents = relevantEvents.sort_values(['Game_id', 'Period', 'PC_Time', 'Event_Msg_Type'], ascending = [True, True, False, True])


def changePlusMinus(Game_id, Event_Msg_Type, Period, Option1, Team_id, Person1, Person2):
	if Event_Msg_Type == 1:
		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
		np.vectorize(shotFor)(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
		np.vectorize(shotAgainst)(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
	elif Event_Msg_Type == 3 and Option1 == 1:
		scoringTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] == Team_id)]
		againstTeam = lineups[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Team_id'] != Team_id)]
		np.vectorize(shotFor)(scoringTeam['Game_id'], scoringTeam['Person_id'], Option1)
		np.vectorize(shotAgainst)(againstTeam['Game_id'], againstTeam['Person_id'], Option1)
	elif Event_Msg_Type == 8:
		makeSubstitute(Game_id, Period, Person1, Person2)



def shotFor(Game_id, Person_id, Option1):
	plusMinus.loc[(plusMinus['Game_id'] == Game_id) & (plusMinus['Person_id'] == Person_id), 'Player_Plus/Minus'] += Option1

def shotAgainst(Game_id, Person_id, Option1):
	plusMinus.loc[(plusMinus['Game_id'] == Game_id) & (plusMinus['Person_id'] == Person_id), 'Player_Plus/Minus'] -= Option1

def makeSubstitute(Game_id, Period, Person1, Person2):
	lineups.loc[(lineups['Game_id'] == Game_id) & (lineups['Period'] == Period) & (lineups['Person_id'] == Person1), 'Person_id'] = Person2

np.vectorize(changePlusMinus)(relevantEvents['Game_id'], relevantEvents['Event_Msg_Type'], relevantEvents['Period'],  \
	relevantEvents['Option1'], relevantEvents['Team_id'], relevantEvents['Person1'], relevantEvents['Person2'])















































