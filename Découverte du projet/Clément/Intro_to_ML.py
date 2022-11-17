from select import select
import pandas as pd
pd.read_csv # pour ouvrir un excel
data.describe() #affiche un résumé
data.columns #pour obtenir la liste des colonnes du DataFrames
# Prediction Target : colomne que l'on voudra prédire
# Features : colomnes que l'on va utiliser pour la prédiction
data.head() # affiche les premières lignes

# Utilisation de scikit-learn  pour les modèles :
from sklearn.tree import DecisionTreeRegressor

modele = DecisionTreeRegressor(max_leaf_nodes=z,random_state=1) # un exemple de modèle, max_leaf_nodes permet de gérer la profondeur de l'arbre pour 
                                                                # gérer l'underfitting ou l'overfitting par tests successifs 
y=data.Nom_Colomne
X = data[[liste colomnes]]

modele.fit(X,y) # pour entrainer le modèle
model.predict(données) # on prédit la colomne y pour des lignes ayant "données" comme X
#  Mean Absolute Error (MAE) : pour vérifier le modèle

from sklearn.metrics import mean_absolute_error # pour importer la fonction de la MAE
mean_absolute_error(données_réelles, données_prédites)

from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y,train_size=0.8, test_size=0.2, random_state=1) # pour séparer le modèle en deux parties : une pour l'entrainement et l'autre pour la validation
# random_state (0 ou 1 ?) permet d'avoir le même découpage à chaque fois
# on peut rajouter les train_size et test_size pour choisir son découpage

#Pour l'underfitting ou l'overfitting : tests sur la MAE pour la minimiser puis :
modele = DecisionTreeRegressor(max_leaf_nodes=z,random_state=1)

#Random Forests :
from sklearn.ensemble import RandomForestRegressor
RandomForestRegressor(n_estimators=200) # plein d'arguments possibles (profondeur max...) voir la doc

output = pd.DataFrame({'Id': X_test.index, 'SalePrice': preds_test})
output.to_csv('submission.csv', index=False)        #pour save le résultat des prédictions en DataFrame puis en Excel

# Dealing with missing values :
colonne_avec_données_manquantes = [col for col in X_train.columns if X_train[col].isnull().any()] #pour obtenir les colonnes avec des données manquantes
data= X_train.drop(colonne_avec_données_manquantes, axis=1) #supprime les colonnes demandées

from sklearn.impute import SimpleImputer #permettra de remplacer une valeur manquant par la moyenne de la colonne
my_imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))

## SimpleImputer supprime le nom des colonnes, dont on les remet à la fin:
imputed_X_train.columns = X_train.columns
X_train_plus[col + '_was_missing'] = X_train_plus[col].isnull() #pour créer une colonne nommé ...was_missing et la remplir

## Number of missing values in each column of training data
missing_val_count_by_column = (X_train.isnull().sum())

# Categorical variable
s = (X_train.dtypes == 'object')    # pour avoir la liste des colonnes avec comme type "objet"
object_cols = list(s[s].index)

## Drop Categorical Variables
drop_X_train = X_train.select_dtypes(exclude=['object'])

## Ordinal Encoding
from sklearn.preprocessing import OrdinalEncoder # pour appeler la fonction d'ordinal encoder
ordinal_encoder = OrdinalEncoder()
label_X_train[object_cols] = ordinal_encoder.fit_transform(X_train[object_cols])

## One-Hot Encoding : permet de rajouter des colonnes de 0 ou 1 pour les valeurs categoricals
from sklearn.preprocessing import OneHotEncoder
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_train.index = X_train.index # One-hot encoding removed index; put it back
num_X_train = X_train.drop(object_cols, axis=1) # Remove categorical columns (will replace with one-hot encoding)
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1) # Add one-hot encoded columns to numerical features

# Columns that can be safely ordinal encoded
good_label_cols = [col for col in object_cols if set(X_valid[col]).issubset(set(X_train[col]))]
#Pour après drop les autres et faire:
label_X_train[good_label_cols] = ordinal_encoder.fit_transform(label_X_train[good_label_cols])
label_X_valid[good_label_cols] = ordinal_encoder.transform(label_X_valid[good_label_cols])

# Pour connaitre les colomnes avec des données de type object de cardinalité < 10 (pour appliquer one-hot Encoding)
low_cardinality_cols = [col for col in object_cols if X_train[col].nunique() < 10]


## pipelines
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')  #ce qu'on va appliquer au colonnes numériques

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[      #ce qu'on compte appliquer aux colonnes avec un type categorical ; Pipeline pour créer une chaine de commandes
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(                               #ensemble des opérations sur les colonnes en fonction des colonnes   
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

my_pipeline = Pipeline(...)

## cross validation
from sklearn.model_selection import cross_val_score

# Multiply by -1 since sklearn calculates *negative* MAE
scores = -1 * cross_val_score(my_pipeline, X, y,cv=5, scoring='neg_mean_absolute_error') #pour obtenir les MAE en cross validation avec 5 folds (cv=5) en partant d'un pipeline pour tout faire (prépocessing + model)

my_pipeline = Pipeline(steps=[('preprocessor', SimpleImputer()),
                                ('model', RandomForestRegressor(n_estimators=50,
                                                                random_state=0))])

## XGBoost
my_model = XGBRegressor(n_estimators = 200, learning_rate=0.05, n_jobs=4) #bcp de paramètres dont n_estimators qui donne le fois que le cycle est fait = nombre de modèles dans l'ensemble
                                                                # voir utilisation précise learning_rate : multiplication des res de chaque modèle de l'ensemble par un petit nombre
                                                                #n_jobs : = au nb de coeur du PC, pour // les calculs (utile seulement si grd Dataset)
my_model.fit(X_train, y_train, 
             early_stopping_rounds=5, #si l'erreur se détériore sur 5 cycles on arrête le programme même si < n_estimators
             eval_set=[(X_valid, y_valid)], #obligatoire quand early_stopping_rounds utilisé
             verbose=False)


## Pandas
import pandas as pd

fruits =pd.DataFrame({'Apples': [30], 'Bananas' : [21]})

# paramètre Index pour renommer les lignes :
pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']},index=['Product A', 'Product B'])

#pour les séries :
pd.Series([30, 35, 40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name='Product A') # on peut renommer l'entiéreté mais pas la colonne précisement

#pour lire des excel en DataFrame :
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv")
wine_reviews.shape # rend le tuple des dimensions
wine_reviews.head() # 5 premières lignes
wine_reviews = pd.read_csv("path", index_col=0) # index_cols : pour spécifier la colonne des index si on ne veut pas de celle généré par pandas

data.to_csv("nom.csv") # pour save data en .csv

data.nom_colomne # pour acceder à la colomne
#OU
data["nom_colonne"]
data["col"][x] # pour accéder au x-ième élément de la colonne

data.iloc[x] #selectionne la ligne x
data.iloc[:, 0] # pour accéder à la première colonne, toutes les lignes
data.iloc[[0, 1, 2], 0]
# les valeurs négatives marchent : on compte alors à partir de la fin

data.loc[0, 'country'] # loc : même fonctionnement que iloc mais avec les labels des colonnes (ici premier élément de la colonne 'country')
#attention : iloc avec [1:10] donne de 1 à 9 loc de [1:10] donne de 1 à 10

data.set_index("title") # renomme la colonne des index ~~ (décale la colonne "title" en index ?)

data.country == 'Italy' # créer une Series avec le résultat du test élément par élément
data.loc[data.country == 'Italy']

data.loc[(data.country == 'Italy') & (data.points >= 90)] # mot clé "&" pour mettre deux conditions
data.loc[(data.country == 'Italy') | (data.points >= 90)] # pour le "ou
data.loc[data.country.isin(['Italy', 'France'])]            # pour prendre les lignes respectant que la valeur de "country" est dans les valeurs de la liste
data.loc[data.price.notnull()]                              # pour récupérer les lignes ou le prix est non null

data.nom_col.describe() # donne des infos utiles sur la colonne (moyenne etc...), donne d'autres infos pour des str
data.nom_col.mean()     # fait la moyenne d'une colonne
data.nom_col.unique()   # pour voir les valeurs uniques (ne pas afficher les doublons)
data.nom_col.value_counts() # compte et affiche le nb d'apparitions des valeurs
data.nom_col.map(lambda p: p - moyenne) #map applique à toutes les valeurs de la colonne la lambda fonction, elle retourne une nouvelle Serie
drop_duplicates # permet de supprimer les doublons des lignes
pd.get_dummies # pour faire du One Hot Encoding
data["PorchTypes"] = data[["WoodDeckSF","OpenPorchSF","EnclosedPorch","Threeseasonporch","ScreenPorch"]].gt(0.0).sum(axis=1) # permet de faire la somme de Booléens pour avoir le nombre total de porches différents pour une ligne. .gt permet de faire le test "greater than"
data["MSClass"]=data.Nom_col.str.split("_",n=1,expand=True)[0] # permet de recréer deux colonnes en splitant au premier "_"

def remean_points(row):
    row.points = row.points - review_points_mean
    return row

data.apply(remean_points, axis='columns') # même opération qu'au dessus, mais on peut changer tout le dataframe avec 
                                             # (agit sur chaque ligne : la fonction doit donc prendre une ligne comme entrée).
                                             # Axis = 'index' aurait fait que apply() agit sur les colomnes et non les lignes

data_nom_col_mean = data.nom_col.mean()      # ça marche aussi 
data.nom_col - data_nom_col_mean

n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum() #pour chercher un mot dans une description

# Grouping and Sorting
data.groupby('points').points.count() # group par points et compte les éléments des groupes

data.groupby('winery').apply(lambda df: df.title.iloc[0]) # le apply s'applique sur le novueau dataframe "df" créé (voir le Out [5] : pas comme en SQL, ici crée du multi index)

data.groupby(['country']).price.agg([len, min, max]) # on groupe par 'country' et on applique les trois fonctions len, min et max sur le group by

data["moyenne par pays"] = data.groupby("Pays").habitants_villes.transform("mean") # fait la moyenne de la colonne habitants_villes et groupe par Pays

data.reset_index()        # permet de reset les index, mais garde une partie du groupby

data.sort_values(by='len') #sort le tableau par la colonne 'len', on rajoute l'argument ascending=False pour trié par ordre décroissant

data.sort_index()   #trie par index

# Types et changement de valeurs

data.nom_col.dtype # pour récupérer le type de la colonne
data.dtypes # même chose mais pour toutes les colonnes
data.nom_col.astype('float64') # pour retyper une colomne

data[pd.isnull(data.nom_col)] # selectionne l'ensemble des lignes pour lesquelles les valeurs de la colomne spécifiée sont nulles
data.nom_col.fillna("Unknown") # remplace les NA par ce qu'on veut : ici "Unknown"
data.nom_col.replace("rien", "truc") # remplace les "rien" en "tout"

# Renommage et Combinage
data.rename(columns={'points': 'score'}) # renomme la colomne "points" en "score"
data.rename(index={0: 'firstEntry', 1: 'secondEntry'}) # renomme les deux premières entrées des index
data.rename_axis('wines', axis='rows') # renomme l'axe des index en "wines"


pd.concat([dataframe1, dataframe2]) # concatène les deux dataframes s'ils ont les mêmes colomnes

left = dataframe1.set_index(['title', 'trending_date']) # passe ces colonnes en index
right = dataframe2.set_index(['title', 'trending_date'])
left.join(right, lsuffix='_CAN', rsuffix='_UK') # permet de concatener horizontalement (si les index correspondent, c'est pour ça qu'on les renomme avant). lsuffix et rsuffix permettent de rajouteur des suffixes aux noms de colomnes des  dataframes de gauche et de droite

## Feature Engineering
# Mutual information (MI : mesure des relations, un peu comme une corrélation)
# le MI est supérieur à 0, échelle log
# MI ne permet que tester l'intéraction entre une features et le rés voulu, pas entre les features
# deux algos dans scikit learn : mutual_info_regression (pour les res real-valued) et mutual_info_classif (pour les categorical targets)
# ATTENTION de bien séparer les discrete features (qui doivent être mis en type int, donc les cateogorical doivent subir un encoder) des autres dans les deux algos
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

## Clustering
sklearn.cluster.KMeans
kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)
X["Cluster"] = kmeans.fit_predict(dataframe)
#Cluster_Distance Features
# Create the cluster-distance features using `fit_transform`
X2 = kmeans.fit_transform(X_scaled)
#PCA
from sklearn.decomposition import PCA

## M Estimate Encoders
from category_encoders import MEstimateEncoder
encoder = MEstimateEncoder(cols=["Neighborhood"],m=1.0)