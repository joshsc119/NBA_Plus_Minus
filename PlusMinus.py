import pandas as pd
import numpy as np

lineups = pd.read_csv("lineups.csv")
codes = pd.read_csv("Codes.csv")
playByPlay = pd.read_csv("PlayByPlay.csv")

relevantEvents = playByPlay[(playByPlay['Event_Msg_Type'] == 1) | (playByPlay['Event_Msg_Type'] == 8) | (playByPlay['Event_Msg_Type'] == 3)]


plusMinus = pd.DataFrame(lineups.groupby(['Game_id', 'Person_id']).count().reset_index()[['Game_id', 'Person_id']])
plusMinus['Player_Plus/Minus'] = 0

gameToID = pd.DataFrame(playByPlay['Game_id'].unique())
gameToID.columns = ['Game_id']

relevantEvents.sort_values(['Game_id', 'Period', 'PC_Time', 'Event_Msg_Type'], ascending = [True, True, False, True])































































