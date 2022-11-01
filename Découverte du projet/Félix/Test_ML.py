import pandas as pd

#Algorithme de machine learning pour prédire le gagnant d'un match en fonction des champions joués par les deux équipes

from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn import utils
import numpy as np

#On importe le dataset
df=pd.read_csv('/Users/felixdoublet/Desktop/Scripts python/TM/Découverte du projet/Félix/games.csv')

#Création d'un nouveau data frame avec seulement le vainqueur et les champions joués

df2 = pd.DataFrame(columns=['winner','blueTop','blueJungle','blueMiddle','blueADC','blueSupport','redTop','redJungle','redMiddle','redADC','redSupport'])



print(type(df.participants[0]))


