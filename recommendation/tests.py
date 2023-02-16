import pandas as pd
import numpy as np
import copy

from main import predictChampions,predictChampionsWithData
from utils import createListGames,requestInfoGames,roleCode
from roles import loadModels,getRoles,getRolesMulti

KEY = "RGAPI-959c42b3-0f6b-4c26-b638-a5e1cfb52957"


#Fichier de test des fonctions de prédiction des rôles d'une liste de champions incomplète


champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
roles = ["TOP","JGL","MID","ADC","SUP"]

def testRoles(): #Test de getRoles et getRolesMulti
    models = loadModels()
    c = [145,80,64]
    c2 = [[1,131,117,135,71],[9,29,122,114,104],[23,42,77,33,67]]
    r = getRoles(c,models)
    r2 = getRolesMulti(c2,models)
    for i in range(len(c)):
        print(champions[c[i]],roles[r[i]])
    for i in range(len(c2)):
        print("##########################################")
        for j in range(len(c2[0])):
            print(champions[c2[i][j]],roles[r2[i][j]])

def generateGame():
    L = createListGames(1,KEY,"IV","GOLD")
    X = []
    for partie in L:
        try: #au cas où un problème survient (tellement de requêtes que ça arrive de temps en temps, il faudrait regarder dans le détail...)
            data = requestInfoGames(partie,KEY)
            participants = data["info"]["participants"] #info des joueurs
            r = []
            s = []
            blue = participants[:5]
            red = participants[5:]
            np.random.shuffle(blue)
            np.random.shuffle(red)
            participants = blue + red
            for i in range(10): #pour chacun des joueurs (une équipe après l'autre, TOP->JGL->MID->ADC->SUP)
                ROLE = roleCode(participants[i]['teamPosition'])
                summoner_name = participants[i]['summonerName']
                r.append(ROLE)
                s.append(summoner_name)
            X.append([s,r])
        except Exception as ex:
            print(ex)

    order = [0,5,6,1,2,7,8,3,4,9]
    for game in range(len(X)):
        bans = []
        blue = []
        red = []
        for player in range(10):
            p = order[player]
            team = p<5
            L,scores,banned = predictChampions(bans,blue,red,X[game][1][5*team:5*(team+1)],blue if team else red,player,X[game][0][p])
    print(X)

if __name__ == "__main__":
    testRoles()