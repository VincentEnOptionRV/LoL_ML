import pandas as pd
import numpy as np
import copy
import pickle

from main import predictChampions,topChamp,orderChamps
from utils import createListGames,requestInfoGames,roleCode,getValues
from roles import loadModels,getRoles,getRolesMulti

KEY = ""

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

def generateGame(tier="I",rank="GOLD"): #TODO
    L = createListGames(1,KEY,tier,rank)
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
            print(f"Generation for {rank} {tier}")
            bans,blue,red,blue_p,red_p,blue_r,red_r,blue_s,red_s,blue_c,red_c = [],[],[],[],[],[],[],[],[],[],[]
            for player in range(10):
                p = order[player]
                team = p<5
                if team:
                    roles_num = list(map(lambda x:roles.index(x),X[game][1][:5]))
                else:
                    roles_num = list(map(lambda x:roles.index(x),X[game][1][5:]))
                try:
                    L,scores,banned = predictChampions(bans,blue,red,roles_num,p<5,p%5,X[game][0][p],KEY,verbose=False)
                    top = topChamp(L,scores,banned,roles_num[p%5])
                except Exception as ex:
                    print(ex)
                    top = [-1,0]
                if p<5:
                    blue.append(None if top is None else top[1])
                    blue_p.append(X[game][0][p])
                    blue_s.append(None if top is None else top[0])
                    blue_r.append(roles[roles_num[p%5]])
                    blue_c.append(None if top is None else champions[top[1]])
                else:
                    red.append(None if top is None else top[1])
                    red_p.append(X[game][0][p])
                    red_s.append(None if top is None else top[0])
                    red_r.append(roles[roles_num[p%5]])
                    red_c.append(None if top is None else champions[top[1]])
                print(f"Score for player {player} ({X[game][0][p]}): {None if top is None else '%.1f' % top[0]} with champion {None if top is None else champions[top[1]]} for role {roles[roles_num[p%5]]}")
            df = pd.DataFrame({"Player blue":blue_p,"Role blue":blue_r,"Champions blue":blue_c,"Score blue":blue_s,\
                               "Player red":red_p,"Role red":red_r,"Champions red":red_c,"Score red":red_s})
            print(df)
            #df.to_csv(f"recommendation/drafts/{rank}_{tier}.csv")

# def validation():
#     vals=[np.arange(0,500,25),np.arange(0,500,25),np.arange(0,1,0.05),[True,False],[True,False],np.arange(800,2400,100),np.arange(0,100,5),np.arange(0,100000,5000),np.arange(0,100,5),np.arange(0,100,5),np.arange(0,1,0.05),np.arange(0,200,10)]
#     scores = [[[] for m in range(len(vals[k]))] for k in range(12)]
#     for rank in ['IRON','PLATINUM','DIAMOND']:
#         for tier in ['IV','III','II','I']:
#             draft = pd.read_csv(f"recommendation/drafts/{rank}_{tier}.csv",index_col=0)
#             blue = []
#             red = []
#             roles_blue = list(map(lambda x:roles.index(x),list(draft["Role blue"])))
#             roles_red = list(map(lambda x:roles.index(x),list(draft["Role red"])))
#             for player in range(10):
#                 try:
#                     print(rank,tier,player)
#                     order = [0,5,6,1,2,7,8,3,4,9]
#                     p = order[player]
#                     team = p<5
#                     id = p%5
#                     color = "blue" if p else "red"
#                     roles_num = roles_blue if team else roles_red
#                     pseudo = draft.iloc[id][f"Player {color}"]
#                     role = draft.iloc[id][f"Role {color}"]
#                     champ = draft.iloc[id][f"Champions {color}"]
#                     id_champ = champions.index(champ)
#                     L,X = getValues(pseudo,None,KEY)
#                     for k in range(12):
#                         for z in range(len(L)):
#                             Lc = copy.deepcopy(L[z])
#                             Xc = copy.deepcopy(X[z])
#                             Xt = []
#                             Lt = []
#                             for val in vals[k]:
#                                 Xc[-12+k]=val
#                                 Xt.append(Xc)
#                                 Lt.append(Lc)
#                                 print(Xc)
#                             Z,score,banned=predictChampions([],blue,red,roles_num,p<5,p%5,pseudo,KEY,verbose=False,L=Lt,X=Xt)
#                             j = 0
#                             for s in score:
#                                 scores[k][j].append(s)
#                                 j += 1
#                     if team:
#                         blue.append(id_champ)
#                     else:
#                         red.append(id_champ)
#                 except Exception as ex:
#                     print(ex)
#         with open(f"validation{rank}.pkl", "wb") as fp:
#             pickle.dump(scores, fp)



if __name__ == "__main__":
    # validation()
    # testRoles()
    generateGame('IV','BRONZE')
    # for rank in ['BRONZE','SILVER','GOLD','PLATINUM','DIAMOND']:
    #     for tier in ['IV','III','II','I']:
    #         try:
    #             generateGame(tier,rank)
    #         except Exception as ex:
    #             print(ex)