from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import re
import pandas as pd

from utils import roleCode,requestInfoGames

KEY = "RGAPI-efba3c40-a760-4586-bfc3-f06edd4c46b7"

def getWinrates(summoner,champion):
    if champion == "MonkeyKing":
        champion = "Wukong"
    url = f"https://u.gg/lol/profile/euw1/{summoner}/champion-stats?season=18&queueType=ranked_solo_5x5"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "lxml")
    rates = soup.find_all('div', class_="champion-rates")
    names = soup.find_all('span', class_="champion-name")
    for i in range(len(rates)):
        c = re.sub(r'[^a-zA-Z]','',names[i].text.lower())
        w = list(map(int,re.findall(r'\d+', rates[i].text)))
        if c == champion.lower():
            return [w[1]/(w[1]+w[2]),w[1],w[2]]

def main():
    df = pd.read_pickle("Création du Dataset/datasetv3.pkl")
    df2 = pd.read_pickle("Création du Dataset/scrapping.pkl")
    
    #df = pd.read_pickle("c:/Users/ptrin/Documents/EI3/PROJET/LoL_ML/Création du Dataset/dataset.pkl")
    #df2 = pd.read_pickle("c:/Users/ptrin/Documents/EI3/PROJET/LoL_ML/Création du Dataset/scrapping.pkl")
    
    roles = ["TOP","JGL","MID","ADC","SUP"]
    stats = ["name","role","champion","winrate","wins","losses"]
    columns = []
    dataset = {}
    for i in range(2):
        for role in roles:
            for stat in stats:
                columns.append(f"{role}{i}_{stat}")
    for column in columns:
        dataset[column] = list(df2[column]) # !!

    index_total = list(df.index)
    index_past = list(df2.index) # !!
    index = []
    for ind in index_total:
        if ind not in index_past:
            index.append(ind)

    for partie in index:
        try: #au cas où un problème survient (tellement de requêtes que ça arrive de temps en temps, il faudrait regarder dans le détail...)
            data = requestInfoGames(partie,KEY)
            participants = data["info"]["participants"] #info des joueurs
            for i in range(10): #pour chacun des joueurs (une équipe après l'autre, TOP->JGL->MID->ADC->SUP)
                ROLE = roleCode(participants[i]['teamPosition'])
                CHAMP = participants[i]['championName']
                NAME = participants[i]['summonerName']
                try:
                    w = getWinrates(NAME,CHAMP)
                    if w is None:
                        WR = -1
                        W = -1
                        L = -1
                    else:
                        WR = w[0]
                        W = w[1]
                        L = w[2]
                except Exception as ex:
                    print(NAME,ex)
                    WR = -1
                    W = -1
                    L = -1
                k = 0
                for feature in [NAME,ROLE,CHAMP,WR,W,L]:
                    dataset[f"{ROLE}{i//5}_{stats[k]}"].append(feature)
                    k += 1 
        except Exception as ex:
            print(f"({len(index_past)}/{len(index_total)}) partie {partie}, erreur {ex}")
            for i in range(10):
                k=0
                for feature in [NAME,ROLE,CHAMP,WR,W,L]:
                    dataset[f"{ROLE}{i//5}_{stats[k]}"].append(0)
                    k += 1 
        else:
            print(f"({len(index_past)}/{len(index_total)}) partie {partie}")
        index_past.append(partie)
        df2 = pd.DataFrame(data=dataset, index=index_past)
        df2.to_pickle("Création du Dataset/scrapping.pkl")
        df2.to_csv("Création du Dataset/scrapping.csv")

def complete_dataset():
    roles = ["TOP","JGL","MID","ADC","SUP"]
    


if __name__ == "__main__":    
    main()