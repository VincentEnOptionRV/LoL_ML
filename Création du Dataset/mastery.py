#Fichier pour ajouter les informations de mastery

import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
from utils import getMasteries,requestInfoGames

PATCH = "12.21.1"
CHAMPIONS_JSON_URL = "https://ddragon.leagueoflegends.com/cdn/" + PATCH + "/data/en_US/champion.json"
KEY= "RGAPI-c01527a9-1c43-429b-b303-2b75def18d92"

data = json.loads(urlopen(CHAMPIONS_JSON_URL).read())
dfchamps = pd.DataFrame(data['data']).transpose()

def getChampionId(champ):
    return dfchamps.loc[champ]["key"]

def main(start,end,KEY):
    df = pd.read_pickle("Création du Dataset/dataset.pkl")
    mas = []
    roles = ["TOP","JGL","MID","ADC","SUP"]
    count = 0
    for game in list(df.index)[start:end]:
        print(f"game ({start+count}/{end-1})")
        count += 1
        m = [game]+[[] for i in range(10)] 
        try:
            players = requestInfoGames(game, KEY)["info"]["participants"]
        except Exception as ex:
            mas.append([game]+[0 for i in range(10)])
        else:
            for i in range(10):
                role = roles[i%5]
                team = i//5
                try:
                    m[i+1] = getMasteries(players[i]['summonerId'],getChampionId(df.loc[game][f"{role}{team}_CHAMP"]),KEY)['championPoints']
                except Exception as ex:
                    m[i+1] = 0
            mas.append(m)
    return mas

start = 2700
end = 2887 #max: 2887
X = np.load("Création du Dataset/masteries.npy")
L0 = X.tolist()

L = main(start,end,KEY)

with open("Création du Dataset/masteries.npy", 'wb') as f:
    np.save(f,np.array(L0+L))