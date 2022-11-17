import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestClassifier

def elo(L):
    if L[0]=="IRON":
        e = 0
    elif L[0]=="BRONZE":
        e = 400
    elif L[0]=="SILVER":
        e = 800
    elif L[0]=="GOLD":
        e = 1200
    elif L[0]=="PLATINUM":
        e = 1600
    elif L[0]=="DIAMOND":
        e = 2000
    else:
        e = 2300
    if L[1] == 'III':
        e += 100
    elif L[1] == 'II':
        e += 200
    elif L[1] == 'I':
        e += 300
    return e + L[2]

def kda(L):
    if L[1] == 0:
        return L[0] + L[2]
    return (L[0] + L[2])/L[1]

df = pd.read_pickle("Création du Dataset/dataset.pkl")

roles = ["TOP","JGL","MID","ADC","SUP"]
stats = ["LVL","TOTAL","GWR","WR","NB","HOT","FILL","RANK"]
columns = []

for i in range(2):
    for role in roles:
        for stat in stats:
            columns.append(f"{role}{i}_{stat}")

for c in columns:
    if c[-4:] == "RANK":
        df[c] = df[c].apply(elo)
    if c[-3:] == "KDA":
        df[c] = df[c].apply(kda)
    if c[-4:] == "KDAG":
        df[c] = df[c].apply(kda)

Xraw = df[columns].to_numpy().astype('float32')
Xp = Xraw.reshape(2293,2,5,8)
Xmean = Xp.mean(axis = 2)
X = Xmean.reshape(2293, 16)
y = df["Y"].to_numpy().astype('float32')

scores = []
N = 10
for i in range(N):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    scores.append(clf.score(X_test,y_test))

print(f"Moyenne des scores sur {N} modèles: {np.mean(scores)}")