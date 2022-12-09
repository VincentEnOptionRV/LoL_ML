import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# On import Offset Image pour pouvoir afficher les images
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

df = pd.read_csv("/Users/felixdoublet/Desktop/Scripts python/TM/Création du Dataset/datasetv3.csv")
print(df.head())

#Trouver les 5 champions les plus joués et afficher leur winrate avec un graphique matplotlib

#On récupère les 5 champions les plus joués
champions = df["JGL0_CHAMP"].value_counts().index[:5]
print(champions)

#On récupère les winrates de ces champions
winrates = []
for champion in champions:
    winrates.append(df[df["JGL0_CHAMP"]==champion]["Y"].mean())
print(winrates)


#On met l'image correspondant à chaque champion au dessus de chaque barre

#On récupère les images
images = []
for champion in champions:
    images.append(plt.imread(f"/Users/felixdoublet/Desktop/Cours_CN/Info_IA/Projet Gaming/dragontail-12.6.1/img/champion/centered/{champion}_0.jpg"))

sns.set()
fig, ax = plt.subplots()
#Colorer les barres avec des couleurs pales 
ax.bar(champions,winrates,color=["#FFD700","#C0C0C0","#CD7F32","#FFD700","#C0C0C0"])        
for i in range(len(champions)):
    imagebox = OffsetImage(images[i], zoom=0.080)
    ab = AnnotationBbox(imagebox, (champions[i], winrates[i]-0.25), frameon=False)
    ax.add_artist(ab)
    plt.text(i, winrates[i], round(winrates[i],3), ha='center', va='bottom', fontweight='bold')
plt.ylim(0,0.7)
plt.show()
