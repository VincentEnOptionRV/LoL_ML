import requests
import pandas as pd
import json
import time
import copy

# Get your key on https://developer.riotgames.com/

def badRequestsHandler(url):
    """
    Permet d'analyser le code de retour de la requête pour gérer les problèmes éventuels.
    Pas sûr que cela permette de gérer tous les problèmes, certains seront probablement spécifiques.
    """
    r = requests.get(url)
    while r.status_code == 429:
        time.sleep(20)
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

def roleCode(role):
    if role == "BOTTOM":
        return "ADC"
    if role == "UTILITY":
        return "SUP"
    if role == "JUNGLE":
        return "JGL"
    else:
        return role[:3]

def getStatsOnLastGames(puuid,n,champion,game_avoid,key):
    games = requestMostRecentGamesIdbis(puuid,key,nb_of_games=n+1)
    if game_avoid in games:
        games.remove(game_avoid)
    else:
        games = games[:n]
    KDAG, KDA, WR, NB, MOST, = [0,0,0],[0,0,0],0,0,[]
    for game in games:
        data = requestInfoGames(game,key)
        participants = data["info"]["participants"] #info des joueurs
        if len(participants)!=0:
            for i in range(10):
                if participants[i]['puuid']==puuid:
                    KDAG[0] += participants[i]['kills']
                    KDAG[1] += participants[i]['deaths']
                    KDAG[2] += participants[i]['assists']
                    MOST.append(roleCode(participants[i]['teamPosition']))
                    if participants[i]['championName']==champion:
                        NB += 1
                        WR += participants[i]['win']
                        KDA[0] += participants[i]['kills']
                        KDA[1] += participants[i]['deaths']
                        KDA[2] += participants[i]['assists']
        else:
            n -= 1
    if n == 0:
        n = 1
        MOST = ["MIDDLE"]
    if NB == 0:
        WR = 0.5
    else:
        WR = WR/NB
    return [a/n for a in KDAG], [a/(max(1,NB)) for a in KDA], WR, NB, max(set(MOST), key = MOST.count)

def getMasteries(encryptedSummonerId, championId, key):
    return badRequestsHandler(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}/by-champion/{championId}?api_key={key}")