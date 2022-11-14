import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# On import Offset Image pour pouvoir afficher les images
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

df = pd.read_csv("/Users/felixdoublet/Desktop/Scripts python/TM/Création du Dataset/dataset.csv")
print(df.head())

#Trouver les 5 champions les plus joués et afficher leur winrate avec un graphique matplotlib

#On récupère les 5 champions les plus joués
champions = df["TOP0_CHAMP"].value_counts().index[:5]
print(champions)

#On récupère les winrates de ces champions
winrates = []
for champion in champions:
    winrates.append(df[df["TOP0_CHAMP"]==champion]["Y"].mean())
print(winrates)


#On met l'image correspondant à chaque champion au dessus de chaque barre

#On récupère les images
images = []
for champion in champions:
    images.append(plt.imread(f"/mettre/son/chemin/dragontail-12.19.1/img/champion/centered/{champion}_0.jpg"))

#On affiche jusqu'a 0.7
fig, ax = plt.subplots()
ax.bar(champions,winrates)
for i in range(len(champions)):
    imagebox = OffsetImage(images[i], zoom=0.050)
    ab = AnnotationBbox(imagebox, (champions[i], winrates[i]+0.05), frameon=False)
    ax.add_artist(ab)
plt.ylim(0,0.7)
plt.show()

#On affiche avec un graphique seaborn 
fig, ax = plt.subplots()
ax = sns.barplot(x=champions, y=winrates)
for i in range(len(champions)):
    imagebox = OffsetImage(images[i], zoom=0.050)
    ab = AnnotationBbox(imagebox, (i, winrates[i]+0.05), frameon=False)
    ax.add_artist(ab)
plt.ylim(0,0.7)
plt.show()
