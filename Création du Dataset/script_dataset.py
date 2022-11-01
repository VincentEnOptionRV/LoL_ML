import requests
import pandas as pd
import json
import time
import copy

KEY = ""
# Get your key on https://developer.riotgames.com/

def badRequestsHandler(url):
    """
    Permet d'analyser le code de retour de la requête pour gérer les problèmes éventuels.
    Pas sûr que cela permette de gérer tous les problèmes, certains seront probablement spécifiques.
    """
    r = requests.get(url)
    while r.status_code == 429:
        time.sleep(5)
        r = requests.get(url)
    if r.status_code == 400:
        raise Exception("Requête invalide")
    elif r.status_code == 401:
        raise Exception("Unauthorized")
    elif r.status_code == 403:
        raise Exception("Non autorisé: vérifiez la clé")
    elif r.status_code == 404:
        raise Exception("Données non trouvées")
    elif r.status_code == 405:
        raise Exception("Méthode non autorisée")
    elif r.status_code == 415:
        raise Exception("Unsupported media type")
    elif r.status_code == 500:
        raise Exception("Internal server error")
    elif r.status_code == 502:
        raise Exception("Bad gateway")
    elif r.status_code == 503:
        raise Exception("Service non disponible")
    elif r.status_code == 504:
        raise Exception("Gateway timeout")
    elif r.status_code == 200:
        return r.json()

def requestSummonerInfo(summoner_name,key):
    """
    Renvoie un dictionnaire contenant des infos sur le joueur 'summoner_name', à savoir :
    accountId :    string - Encrypted account ID. Max length 56 characters.
    profileIconId:    int - ID of the summoner icon associated with the summoner.
    revisionDate:    long - Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: summoner name change, summoner level change, or profile icon change.
    name:          string - Summoner name.
    id:            string - Encrypted summoner ID. Max length 63 characters.
    puuid:         string - Encrypted PUUID. Exact length of 78 characters.
    summonerLevel:   long - Summoner level associated with the summoner.
    """
    return badRequestsHandler(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={key}")

def requestMostRecentGamesIdbis(puuid,key, nb_of_games,type_queue='ranked'):
    res_games = []
    r = badRequestsHandler(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={nb_of_games}&api_key={key}&type={type_queue}")
    res_games += r
    return res_games

def requestPlayersOfARank(queue,tier,division,number_of_players,key):
    """ 
    Pour récupérer des joueurs de même ELO

    Args
    ----
    queue : String
        Quelle queue ? Parmis RANKED_SOLO_5x5,RANKED_FLEX_SR,RANKED_FLEX_TT
    tier : String
        Nom de la ligue en anglais (ex : GOLD, PLATINIUM...)
    division : String
        numéro de la division : I,II,III,IV
    number_of_players : Int
        Nombre de joueurs voulus
    
    Returns
    -------
    Dict
        Dictionnaire rassemblant les informations des différents joueurs
        Attention : le nombre de joueurs sera arrondi aux 205 supérieurs (par exemple pour 320, 410 seront donnés)
    """

    tier=tier.upper()
    if number_of_players > 205 : # les pages renvoyées par chaque requête contiennent 205 joueurs
        liste_joueurs = []
        for i in range(1,(number_of_players//205)+2):
            r = badRequestsHandler(f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}I?page={i}&api_key={key}")
            if r == []:
                return liste_joueurs # on a atteint le nombre de joueur total de la division
            liste_joueurs += r
    else :
        liste_joueurs = badRequestsHandler(f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}I?page=1&api_key={key}")
    return liste_joueurs

def requestRankedInfo(summoner_id,key):
    """
    Renvoie une liste de dictionnaire contenant des infos sur les résultats du joueur en partie classées, à savoir :
    SOLOQ: {
        tier: string - Iron -> Challenger
        rank: string - IV -> I
        lp: int - league points
        wins: int
        losses: int
    }
    FLEXQ: {pareil}
    """
    data = badRequestsHandler(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={key}")
    if len(data)==2 and data[0]['queueType']!='RANKED_SOLO_5x5':
        return [data[1],data[0]]
    return data

def requestInfoGames(game_id,key):
    """
    Renvoie les informations d'une game
    METADATA: 'matchId'
              'participants' : liste des puuids
    INFO :    'gameDuration'
              'gameEndTimestamp'
              'gameId'
              'gameMode'
              'gameName'
              'gameStartTimestamp'
              'gameType'
              'gameVersion'
              'mapId':
              'participants': liste des informations de la game des 10 participants
              'platformId'
              'queueId'
              'teams': informations globales sur les équipes
    """
    return badRequestsHandler(f"https://europe.api.riotgames.com/lol/match/v5/matches/{game_id}?api_key={key}")
    
def getStatsOnLastGames(puuid,n,champion,key):
    games = requestMostRecentGamesIdbis(puuid,key,nb_of_games=n)
    KDAG, KDA, WR, NB, MOST, = [0,0,0],[0,0,0],0,0,[]
    for game in games:
        data = requestInfoGames(game,key)
        participants = data["info"]["participants"] #info des joueurs
        for i in range(10):
            if participants[i]['puuid']==puuid:
                KDAG[0] += participants[i]['kills']
                KDAG[1] += participants[i]['deaths']
                KDAG[2] += participants[i]['assists']
                MOST.append(participants[i]['teamPosition'])
                if participants[i]['championName']==champion:
                    NB += 1
                    WR += participants[i]['win']
                    KDA[0] += participants[i]['kills']
                    KDA[1] += participants[i]['deaths']
                    KDA[2] += participants[i]['assists']
    return [a/n for a in KDAG], [a/n for a in KDA], WR/n, NB, max(set(MOST), key = MOST.count)


#SCRIPT DE CREATION DU DATASET

#Paramètres
n_stats = 10 #Nombre de parties sur lesquelles on regarde les stats des joueurs
size_dataset = 25 #Taille du dataset

#Création d'une liste de parties pour le dataset dans un index
liste_joueurs = requestPlayersOfARank("RANKED_SOLO_5x5","DIAMOND","II",size_dataset,KEY) #modifier le rank ici
INDEX = []
for joueur in liste_joueurs[:size_dataset]:
    try:
        summoners = requestSummonerInfo(joueur["summonerName"],KEY)
        puuid = summoners["puuid"]
        partie = requestMostRecentGamesIdbis(puuid,KEY, nb_of_games=1)
        INDEX.append(partie[0])
    except:
        pass
print(INDEX)

INDEX_copie=copy.deepcopy(INDEX)
#Création de la strucure du dataset (=features)
roles = ["TOP","JUNGLE","MIDDLE","BOTTOM","UTILITY"]
stats = ["CHAMP","LVL","TOTAL","GWR","VET","RANK","HOT","KDAG","KDA","WR","NB","FILL"]
columns = ["Y"]

for i in range(2):
    for role in roles:
        for stat in stats:
            columns.append(f"{stat}_{role}_{i}")

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
            ROLE = participants[i]['teamPosition']
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
            KDAG, KDA, WR, NB, MOST = getStatsOnLastGames(puuid,n_stats,CHAMP,KEY)
            FILL = (ROLE!=MOST)
            k=0
            for feature in [CHAMP,LVL,TOTAL,GWR,VET,RANK,HOT,KDAG,KDA,WR,NB,FILL]:
                dataset[f"{stats[k]}_{ROLE}_{i//5}"].append(feature)
                k += 1
        Y = data["info"]["teams"][0]["win"]
        dataset["Y"].append(Y)
    except:
        INDEX_copie.remove(partie)
        dataset = copy.deepcopy(copie_dataset)
        print(f"Erreur pour la partie {partie}")

df = pd.DataFrame(data=dataset, index=INDEX_copie)
df.to_pickle("Création du Dataset/test.pkl") #on sauvegarde le dataset pandas