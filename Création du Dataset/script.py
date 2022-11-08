import requests
import pandas as pd
import json
import time
import copy
import pickle

from utils import requestSummonerInfo,requestMostRecentGamesIdbis,requestPlayersOfARank,requestRankedInfo,requestInfoGames,roleCode,getStatsOnLastGames

#SCRIPT DE CREATION DU DATASET

#Paramètres
KEY= "RGAPI-dac1fbc5-756e-4c2e-a5cf-b7a8d1f08bf1"
n_stats = 5 #Nombre de parties sur lesquelles on regarde les stats des joueurs
size = 5000 #Taille du dataset

#Création d'une liste de parties pour le dataset dans un index
def createListGames(size_dataset,path="Création du Dataset/listeGames"):
    liste_joueurs = requestPlayersOfARank("RANKED_SOLO_5x5","PLATINUM","II",size_dataset,KEY) #modifier le rank ici
    INDEX = []
    print(len(liste_joueurs))
    z=0
    for joueur in liste_joueurs[:size_dataset]:
        z+=1
        print(z)
        try: 
            summoners = requestSummonerInfo(joueur["summonerName"],KEY)
            puuid = summoners["puuid"]
            partie = requestMostRecentGamesIdbis(puuid,KEY, nb_of_games=1)
            if partie[0] not in INDEX:
                INDEX.append(partie[0])
        except:
            pass
    with open(path, "wb") as fp:   #Pickling
        pickle.dump(INDEX, fp)
    return INDEX

def main(start,end,n_stats,path="Création du Dataset/games.pkl"):
    with open("Création du Dataset/listeGames", "rb") as fp:
        INDEX = pickle.load(fp)
    INDEX=INDEX[start:end]
    INDEX_copie=copy.deepcopy(INDEX)

    #Création de la strucure du dataset (=features)
    roles = ["TOP","JGL","MID","ADC","SUP"]
    stats = ["CHAMP","LVL","TOTAL","GWR","VET","RANK","HOT","KDAG","KDA","WR","NB","FILL"]
    columns = ["Y"]

    for i in range(2):
        for role in roles:
            for stat in stats:
                columns.append(f"{role}{i}_{stat}")

    dataset = {}
    for column in columns:
        dataset[column]=[]
    #On récupère les features pour chacune des parties
    for partie in INDEX:
        copie_dataset = copy.deepcopy(dataset)
        try: #au cas où un problème survient (tellement de requêtes que ça arrive de temps en temps, il faudrait regarder dans le détail...)
            data = requestInfoGames(partie,KEY)
            participants = data["info"]["participants"] #info des joueurs
            for i in range(10): #pour chacun des joueurs (une équipe après l'autre, TOP->JGL->MID->ADC->SUP)
                ROLE = roleCode(participants[i]['teamPosition'])
                CHAMP = participants[i]['championName']
                summoner_name = participants[i]['summonerName']
                summoner_id = participants[i]['summonerId']
                puuid = participants[i]['puuid']
                summoner_info = requestSummonerInfo(summoner_name,KEY)
                LVL = summoner_info['summonerLevel']
                ranked_info = requestRankedInfo(summoner_id,KEY)[0]
                TOTAL = ranked_info["wins"]+ranked_info["losses"]
                GWR = ranked_info["wins"]/(TOTAL)
                VET = ranked_info["veteran"]
                RANK = [ranked_info['tier'],ranked_info['rank'],ranked_info['leaguePoints']]
                HOT = ranked_info['hotStreak']
                KDAG, KDA, WR, NB, MOST = getStatsOnLastGames(puuid,n_stats,CHAMP,partie,KEY)
                FILL = (ROLE!=MOST)
                k=0
                for feature in [CHAMP,LVL,TOTAL,GWR,VET,RANK,HOT,KDAG,KDA,WR,NB,FILL]:
                    dataset[f"{ROLE}{i//5}_{stats[k]}"].append(feature)
                    k += 1 
            Y = data["info"]["teams"][0]["win"]
            dataset["Y"].append(Y)
        except Exception as ex:
            INDEX_copie.remove(partie)
            dataset = copy.deepcopy(copie_dataset)
            print(f"Erreur pour la partie {partie}")
            print(ex)
        else:
            print(f"Aucune erreur pour la partie {partie}")

    df = pd.DataFrame(data=dataset, index=INDEX_copie)
    df.to_pickle(path) #on sauvegarde le dataset pandas

def pickle_to_csv(path_pickle,path_csv):
    df = pd.read_pickle(path_pickle)
    df.to_csv(path_csv)

start = 1000 # à modifier: indice de début
end = 1101 # à modifier: indice de fin (non inclus)
main(start,end,n_stats,path=f"Création du Dataset/data/data{start}_{end}.pkl")
#pickle_to_csv(f"Création du Dataset/data/data{start}_{end}.pkl","Création du Dataset/csv_exemple.csv")