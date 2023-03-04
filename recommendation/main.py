import pandas as pd
import numpy as np
import pickle
from time import time
from utils import getValues
from roles import getRoles,loadModels

champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
champions2 = ['aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'amumu', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelionsol', 'azir', 'bard', 'belveth', 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', 'chogath', 'corki', 'darius', 'diana', 'draven', 'drmundo', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce', 'jhin', 'jinx', 'kaisa', 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', 'khazix', 'kindred', 'kled', 'kogmaw', 'ksante', 'leblanc', 'leesin', 'leona', 'lillia', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar', 'maokai', 'masteryi', 'missfortune', 'wukong', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuwillump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'rammus', 'reksai', 'rell', 'renataglasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion', 'sivir', 'skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahmkench', 'taliyah', 'talon', 'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', 'velkoz', 'vex', 'vi', 'viego', 'viktor', 'vladimir', 'volibear', 'warwick', 'xayah', 'xerath', 'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra']
stats = ["LVL","TOTAL","GWR","HOT","FILL","RANK","VS","MAS","WCH","LCH","TOTCH","WRCH"]
top_champs = [['jax','gangplank','darius','fiora','malphite','illaoi'],\
              ['jarvaniv','evelynn','zac','udyr','rammus','fiddlesticks','wukong','rengar','masteryi'],\
              ['aurelionsol','annie','anivia','cassiopeia','katarina','vladimir'],\
              ['xayah','draven','twitch','kaisa','jhin','nilah'],\
              ['annie','blitzcrank','rakan','pyke','thresh','nautilus']]

KEY = ""

"""Fichier principal: calcul des probabilités de victoire d'un joueur en fonction du champion
sélectionné, à partir d'une draft incomplète""" 

def getModels(): #chargement des modèles
    models = []
    for position in range(10):
        models.append(pickle.load(open(f"recommendation/models_winner/model_w{position+1}", 'rb')))
    return models

models_roles = loadModels()

def predictChampions(bans_input,blue_input,red_input,roles_input,team_input,position_input,pseudo_input,KEY,verbose=True,L=None,X=None):
    """Fonction principale: calcul des probabilités de victoire pour chacun des champions
    d'un joueur, à partir d'une draft incomplète.

    Tous les ids des champions sont de 0 à 161 (ordre alphabétique).
    L'équipe alliée est l'équipe du joueur auquel on veut recommander un champion.

	Parameters:
		bans_input (list of ints): ids des 10 champions bannis
		blue_input (list of ints): ids des champions sélectionnés de l'équipe bleue (taille 0 à 5)
        red_input (list of ints): ids des champions sélectionnés de l'équipe rouge (taille 0 à 5)
        roles_input (list of ints): ids des rôles (de 0 à 4) de l'équipe alliée (taille 5)
        team_input (bool): True si l'équipe alliée est bleu, False si rouge
        position_input (int): ordre de sélection du joueur de son équipe 0: first pick / 4 last pick
        pseudo_input (str): pseudo du joueur dont c'est le tour de pick.

	Returns:
		L (list of strings): Liste des noms de champions déjà joués une fois par un joueur en classé
        scores (list of floats): Liste des scores (0-100) associés à chaque champion de L
        bans: champions qui ne peuvent pas être sélectionnés (bans + déjà picks)
    """

    t0 = time()
    if team_input:
        ally = blue_input
        enemy = red_input
        pick = [1,4,5,8,9][position_input]
    else:
        ally = red_input
        enemy = blue_input
        pick = [2,3,6,7,10][position_input]
    #print(f"{pick=}")
    #print(f"ally team: {ally=}, {[champions[i] for i in ally]}")
    #print(f"enemy team: {enemy=}, {[champions[i] for i in enemy]}")
    role = roles_input[position_input]
    #print(f"{role=}")
    enemy_roles = getRoles(enemy,models_roles)
    t1 = time()
    if team_input:
        blue_roles = roles_input
        red_roles = enemy_roles
    else:
        blue_roles = enemy_roles
        red_roles = roles_input
    #print(f"{enemy_roles=}")
    if role in enemy_roles:
        ind = enemy_roles.index(role)
        opponent = enemy[ind]
        ch_opponent = champions[opponent]
    else:
        ch_opponent = None
    #print(f"{opponent=}, {champions[opponent]}")
    if L is None or X is None:
        L,X = getValues(pseudo_input,ch_opponent,KEY)
    t2 = time()
    full_teams = []
    full_roles = []
    p=0
    blue_picks = [0,3,4,7,8]
    red_picks = [1,2,5,6,9]
    while p<pick-1:
        if p in blue_picks:
            ind = blue_picks.index(p)
            full_teams.append(blue_input[ind])
            full_roles.append(blue_roles[ind])
        else: 
            ind = red_picks.index(p)
            full_teams.append(red_input[ind])
            full_roles.append(red_roles[ind])
        p += 1
    #print(f"{full_teams=}")
    #print(f"{full_roles=}")
    for i in range(len(X)):
        X[i] = full_teams + [champions2.index(L[i])] + full_roles + [role] + X[i]
    model = pickle.load(open(f"recommendation/models_winner/model_w{pick}", 'rb'))
    if X==[]:
        probas = []
    else:
        probas = model.predict_proba(X)
    t3 = time()
    scores = []
    for i in range(len(L)):
        score = 100*probas[i][1] if team_input else 100*probas[i][0]
        if verbose:
            print(L[i],f"{'%.1f' % score} %")
        scores.append(score)
    if verbose:
        print(f"time to get roles: {t1-t0}")
        print(f"time to get data: {t2-t1}")
        print(f"time to predict scores: {t3-t2}")
    return L,scores, bans_input+blue_input+red_input

def orderChamps(L,scores,bans,role):
    A = []
    B = []
    for i in range(len(L)):
        c = champions2.index(L[i])
        if c not in bans and getRoles([c],models_roles)[0]==role:
            A.append(c)
            B.append(scores[i])
    AB = list(zip(B,A))
    AB.sort()
    if AB == []:
        A = []
        B = []
        for ch in top_champs[role]:
            c = champions2.index(ch)
            if c not in bans:
                A.append(c)
                B.append(0)
        AB = list(zip(B,A))
        np.random.shuffle(AB)
    return AB

def topChamp(L,scores,bans,role):
    AB = orderChamps(L,scores,bans,role)
    if AB == []:
        return None
    return AB[-1]

if __name__ == "__main__":
    bans_input = [] #ids des champions bannis
    blue_input = [0,1,4] #ids de la team bleu
    red_input = [27,2,8,18] #ids de la team rouge
    roles_input = [0,2,4,1,3] #roles de l'équipe du joueur
    team_input = True #équipe du joueur (blue=True)
    position_input = 3 #ordre de sélection du joueur de son équipe 0: first pick / 4 last pick
    pseudo_input = "agurin" #pseudo du joueur
    L,scores,banned=predictChampions(bans_input,blue_input,red_input,roles_input,team_input,position_input,pseudo_input,KEY)
    print(orderChamps(L,scores,banned,1))