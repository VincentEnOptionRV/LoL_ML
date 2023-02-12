#Prédiction des rôles d'une équipe à partir d'une liste de champions incomplète

import pandas as pd
import numpy as np
import copy
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
from tensorflow.keras import layers

#Liste des champions dans l'ordre alphabétique
champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
roles = ["TOP","JGL","MID","ADC","SUP"]

def getData(df):
    #renvoie des exemples d'équipes incomplètes [[role,champion]]
    #pour chacune des 5 positions à prédire (first pick, etc...)
    D = []
    for position in range(5):
        M = []
        for l in range(len(df)):
            for t in range(2):
                r = copy.copy(roles)
                np.random.shuffle(r)
                for d in range(position,5):
                    V = []
                    for role in r[:d+1]:
                        V.append([roles.index(role),champions.index(df.iloc[l][f"{role}{t}_CHAMP"])])
                    M.append(V)
        np.random.shuffle(M)
        D.append(M)
    return D

#ind_train = int(len(M)*4/5)
def getTrain(D,ind_train):
    X = []
    Y = []
    for position in range(5):
        Xp = []
        Yp = []
        for V in D[position][:ind_train]:
            x = []
            y = []
            for i in range(len(V)):
                x.append(V[i][1])
                y0 = [0,0,0,0,0]
                y0[V[i][0]] = 1
                y.append(y0)
            Xp.append(x + (5-len(x))*[len(champions)])
            Yp.append(y + (5-len(x))*[[0,0,0,0,0]])
        X.append(Xp)
        Y.append(Yp)
    return X,Y

def getModels(X,Y):
    #renvoie une liste de 5 modèles pour chaucune des positions dans la draft (first pick, etc ...)
    #qui prennent en entrée une équipe incomplète [2,56,31] et renvoie en sortie les probas d'appartenir 
    #à chaque poste [P(TOP),P(JGL),P(MID),P(ADC),P(SUP)]
    models_list = []
    for position in range(5):
        X_train = X[position]
        y_train = Y[position]
        model = keras.Sequential(
            [   
                layers.Embedding(len(champions)+1, 20, input_length=5),
                layers.Flatten(),
                layers.Dense(5, activation="softmax"),
            ]
        )
        model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
        model.fit(np.array(X_train),np.array(y_train)[:,position,:],epochs=10)
        models_list.append(model)
    return models_list

def getRoles(L0,models):
    L = copy.copy(L0)
    #renvoie les rôles supposés à partir d'une équipe incomplète [c1,c2,c3,c4] 
    n = len(L)
    L += (5-n)*[len(champions)]
    p = []
    for i in range(n):
        mod = models[i]
        p.append((mod.predict([L],verbose = 0)).tolist()[0])
    res = n*[None]
    for k in range(n):
        j,i = np.argmax(np.max(p, axis=0)), np.argmax(np.max(p, axis=1))
        res[i] = j
        for z in range(len(p)):
            p[z][j]=0
        for z in range(len(p[0])):
            p[i][z]=0
    return res

def getRolesMulti(L0,models):
    L = copy.copy(L0)
    #renvoie les rôles supposés à partir d'une liste d'équipe incomplète [[9],[3,86,20],[15,36]] 
    n = len(L[0])
    for l in L:
        l += (5-n)*[len(champions)]
    p = []
    for i in range(n):
        mod = models[i]
        p.append((mod.predict(L,verbose = 0)).tolist())
    p = np.swapaxes(p,0,1)
    results = []
    for ind in range(len(L)):
        res = n*[None]
        for k in range(n):
            j,i = np.argmax(np.max(p[ind], axis=0)), np.argmax(np.max(p[ind], axis=1))
            res[i] = j
            for z in range(len(p[ind])):
                p[ind][z][j]=0
            for z in range(len(p[ind][0])):
                p[ind][i][z]=0
        results.append(res)
    return results

def toChamp(x):
    if x<len(champions):
        return champions[x]
    else:
        return "vide"

def evaluateModels(D,ind_train,models_list):
    #évalue des modèles entrainés sur D[:ind_train]
    count_errors = 0
    scores = []
    totals = []
    for lenV in range(1,6):
        for position in range(lenV):
            score = 0
            total = 0
            Xp = []
            Yp = []
            for V in D[position][ind_train:]:
                if len(V)==lenV:
                    Xp.append([v[1] for v in V])
                    Yp.append([v[0] for v in V])
            Y_pred = getRolesMulti(Xp,models_list)
            for i in range(len(Yp)):
                if Yp[i]==Y_pred[i]:
                    score += 1
                elif count_errors<100 and lenV==5:
                    count_errors+=1
                    #print(list(map(toChamp,Xp[i])),list(map(lambda x:roles[x],Yp[i])),list(map(lambda x:roles[x],Y_pred[i])))
                total += 1
            scores.append(score)
            totals.append(total)

    print(scores)
    print(totals)
    print(f"Score: {100*np.sum(scores)/np.sum(totals)}%")

def saveModels(models):
    for i in range(5):
        models[i].save(f"recommendation/models_role/model_{i+1}p")

def loadModels():
    models = []
    for i in range(5):
        models.append(keras.models.load_model(f"recommendation/models_role/model_{i+1}p"))
    return models

def createModels():
    D = getData(df)
    ind = len(D[-1])
    X,y = getTrain(D,ind_train=ind)
    models = getModels(X,y)
    saveModels(models)

if __name__ == "__main__":
    #evaluation of models
    df = pd.read_pickle("Création du Dataset/datasetv3.pkl")
    D = getData(df)
    ind = 4617
    X,y = getTrain(D,ind_train=ind)
    models = getModels(X,y)
    evaluateModels(D,ind_train=ind,models_list=models)
    createModels()
    