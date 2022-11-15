import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error # pour importer la fonction de la MAE
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_regression

data = pd.read_pickle("Création du Dataset/dataset.pkl")

#suppression des KDA car bcp de 0
roles = ["TOP","JGL","MID","ADC","SUP"]
colomnes = []
for i in [0,1]:
    for role in roles :
        colomnes.append(f"{role}{i}_KDA")
# print(colomnes)
data = data.drop(columns = colomnes)

# suppression des listes pour le KDAG par transformation en plusieurs colomnes
colomnes_KDAG=[]
for colomne in colomnes:
    colomnes_KDAG.append(colomne + "G")
# print(colomnes_KDAG)

for colomne in colomnes_KDAG:
    nom = colomne[:-4]
    data2 = pd.DataFrame(data[f"{colomne}"].to_list(),data.index,columns=[f"{nom}K",f"{nom}D",f"{nom}A",])
    data[f'{nom}KDA_Ratio'] = (data2[f'{nom}K'] + data2[f'{nom}A']) / (data2[f'{nom}D']+1)
    data = data.drop(columns = colomne)
# print(data)

#champion par leur ID :
dict_champ = {}
L=['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw','KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
for i in range(len(L)):
    dict_champ[L[i]]=i

def ID_champ(L):
    return(dict_champ[L])

for colomne in colomnes:
    nom = colomne[:-3]
    data[f"{nom}CHAMP"] = data[f"{nom}CHAMP"].apply(ID_champ)

# On s'occupe du rank (voir Paul) :
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

for c in data.columns:
    if c[-4:] == "RANK":
        data[c] = data[c].apply(elo)


for role in roles:
    data[f"{role}_LVL_RATIO"]=data[f"{role}0_LVL"]/data[f"{role}1_LVL"]
data[f"{role}_LVL_RATIO_MEAN"]=(data["SUP0_LVL"]+data["ADC0_LVL"]+data["MID0_LVL"]+data["JGL0_LVL"]+data["TOP0_LVL"])/(data["SUP1_LVL"]+data["ADC1_LVL"]+data["MID1_LVL"]+data["JGL1_LVL"]+data["TOP1_LVL"])


def make_mi_scores(X, y):
    X = X.copy()
    for colname in X.select_dtypes(["object", "category"]):
        X[colname], _ = X[colname].factorize()
    # All discrete features should now have integer dtypes
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in X.dtypes]
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features, random_state=0)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores

y = data["Y"]
X=data.drop(columns = ["Y"])


scores = []
N = 10
for i in range(N):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    scores.append(clf.score(X_test,y_test))

print(f"Moyenne des scores sur {N} modèles: {sum(scores)/len(scores)}")