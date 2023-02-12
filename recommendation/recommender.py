import pandas as pd
import numpy as np
import pickle
from utils import getValues
from role_predictor import getRoles,loadModels

champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
stats = ["LVL","TOTAL","GWR","HOT","FILL","RANK","VS","MAS","WCH","LCH","TOTCH","WRCH"]
KEY = ""

def getModels():
    models = []
    for position in range(10):
        models.append(pickle.load(open(f"recommendation/models_winner/model_w{position+1}", 'rb')))
    return models

models_roles = loadModels()

def predictChampions(bans_input,blue_input,red_input,roles_input,team_input,position_input,pseudo_input,KEY):
    if team_input:
        ally = blue_input
        enemy = red_input
        pick = [1,4,5,8,9][position_input]
    else:
        ally = red_input
        enemy = blue_input
        pick = [2,3,6,7,10][position_input]
    role = roles_input[position_input]
    enemy_roles = getRoles(enemy,models_roles)
    if role in enemy_roles:
        ind = enemy_roles.index(role)
        opponent = enemy[ind]
    else:
        opponent = None
    
    L,X = getValues(pseudo_input,champions[opponent],KEY)
    full_teams = []
    full_roles = []
    p=0
    blue_picks = [0,3,4,7,8]
    red_picks = [1,2,5,6,9]
    while p<pick-1:
        if p in blue_picks:
            ind = blue_picks.index(p)
            full_teams.append(blue_input[ind])
            full_roles.append(roles_input[p] if team_input else enemy_roles[ind])
        else: 
            ind = red_picks.index(p)
            full_teams.append(red_input[ind])
            full_roles.append(roles_input[p] if not team_input else enemy_roles[ind])
        p += 1
    for i in range(len(X)):
        X[i] = full_teams + full_roles + X[i]
    
    model = pickle.load(open(f"recommendation/models_winner/model_w{pick}", 'rb'))
    probas = model.predict_proba(X)
    for i in range(len(L)):
        print(L[i],probas[i][0] if team_input else probas[i][1])
    #TODO : enlever les bans, les champions ne correspondant pas au bon rôle, vérifier les inputs.


if __name__ == "__main__":
    bans_input = [] #ids des champions bannis
    blue_input = [0,1,4] #ids de la team bleu
    red_input = [27,2,8,18] #ids de la team rouge
    roles_input = [0,2,4,1,3] #roles de l'équipe du joueur
    team_input = True #équipe du joueur (blue=True)
    position_input = 3 #ordre de sélection du joueur de son équipe 0: first pick / 4 last pick
    pseudo_input = "agurin" #pseudo du joueur
    print(predictChampions(bans_input,blue_input,red_input,roles_input,team_input,position_input,pseudo_input,KEY))