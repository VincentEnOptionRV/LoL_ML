#Prédiction du gagnant à partir des informations partielles: champions sélectionnés, rôle et informatio d'un joueur

import pandas as pd
import numpy as np
import copy
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.model_selection import train_test_split 
import pickle

df = pd.read_pickle("Création du Dataset/datasetv4_fillmissing.pkl")

champions_list = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
#stats = ["LVL","TOTAL","GWR","WR","NB","HOT","FILL","RANK","KDA","KDAG","VS","MAS","WCH","LCH","TOTCH","WRCH"]
#stats = ["LVL","TOTAL","GWR","WR","NB","FILL","RANK","MAS","WCH","LCH","TOTCH","WRCH"]
stats = ["LVL","TOTAL","GWR","HOT","FILL","RANK","VS","MAS","WCH","LCH","TOTCH","WRCH"]
roles = ["TOP","JGL","MID","ADC","SUP"]

def generateDraft():
    #génère une draft aléatoire
    b = [0,1,2,3,4]
    r = [5,6,7,8,9]
    np.random.shuffle(b)
    np.random.shuffle(r)
    return [b[0],r[0],r[1],b[1],b[2],r[2],r[3],b[3],b[4],r[4]]

def generateDraftMulti():
    #génère 5 drafts aléatoires avec chacun à une position différente
    blue = [0,1,2,3,4]
    red = [5,6,7,8,9]
    np.random.shuffle(blue)
    np.random.shuffle(red)
    drafts = []
    for i in range(5):
        b=np.roll(blue,i)
        r=np.roll(red,i)
        drafts.append([b[0],r[0],r[1],b[1],b[2],r[2],r[3],b[3],b[4],r[4]])
    return drafts

def getData(data):
    #renvoie un jeu de données X de taille len(data) pour chacune des 10 positions
    M = [[], [], [], [], [], [], [], [], [], []]
    for i in range(len(data)):
        line = data.iloc[i]
        draft = generateDraft()
        for player in range(10):
            v=[]
            t = []
            for p in range(player):
                p_team = draft[p]//5
                p_role = draft[p]%5
                v.append(champions_list.index(line[f"{roles[p_role]}{p_team}_CHAMP"]))
                t.append(p_role)
            v += ((10-len(v))*[len(champions_list)])
            t += ((10-len(t))*[5])
            v += t
            player_team = draft[player]//5
            player_role = draft[player]%5
            for stat in stats:
                v.append(line[f"{roles[player_role]}{player_team}_{stat}"])
            M[player].append(v)
    return M

def getDataMulti(df):
    data = copy.deepcopy(df)
    #renvoie un jeu de données (X,y) de taille 5*len(data) pour chacune des 10 positions
    M = [[], [], [], [], [], [], [], [], [], []]
    Y = []
    for i in range(len(data)):
        line = data.iloc[i]
        drafts = generateDraftMulti()
        for draft in drafts:
            for player in range(10):
                v=[]
                t = []
                for p in range(player):
                    p_team = draft[p]//5
                    p_role = draft[p]%5
                    v.append(champions_list.index(line[f"{roles[p_role]}{p_team}_CHAMP"]))
                    t.append(p_role)
                #v += ((10-len(v))*[len(champions_list)])
                #t += ((10-len(t))*[5])
                v += t
                player_team = draft[player]//5
                player_role = draft[player]%5
                for stat in stats:
                    v.append(line[f"{roles[player_role]}{player_team}_{stat}"])
                M[player].append(v)
            Y.append(data.iloc[i]["Y"])
    return M,Y

def generateModels(df):
    print("Generation of data")
    X,y = getDataMulti(df)
    for position in range(10):
        print(f"Generation of model {position+1}")
        model = GradientBoostingClassifier()
        model.fit(np.array(X[position]),y)
        pickle.dump(model, open(f"recommendation/models_winner/model_w{position+1}", 'wb'))
    #to read model: loaded_model = pickle.load(open(filename, 'rb'))

if __name__ == "__main__":
    X,y = getDataMulti(df)
    for position in range(10):
        model = GradientBoostingClassifier()
        X_train, X_test, y_train, y_test = train_test_split(np.array(X[position]), y, test_size=0.2)
        model.fit(X_train,y_train)
        print(f"Score for mode {position}: {100*model.score(X_test,y_test)} %")
    generateModels(df)