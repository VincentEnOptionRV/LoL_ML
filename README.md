# LoL_ML
Ici sont déposés nos codes et nos recherches pour le projet Gaming de l'option IA de Centrale Nantes de 2022-2023.

L'objectif final de ce projet est la création d'un outil de recommandation de champions sur League of Legends utilisable au début des parties par un joueur.

Les réalisations sont les suivantes : 
Partie 1 :
  - Création d'un dataset à partir de récolte de données par API et par web-scrapping
  - Prédiction de victoires à partir de données tabulaires en utilisant des modèles de Machine Learning et du feature engineering
  - Comparaison de ces modèles à des réseaux de neurones 
Partie 2 :
  - Reconnaissance et détection d'images à l'aide d'un FCN, de Data Augmentation et de bibliothèques Pythons comme OpenCV
  - Création d'un système de recommandation de champions pour les joueurs en recréant des modèles avec des données manquantes
  - Création d'une application utilisable pour pour effectuer des recommandations en temps réel au début d'une partie

Pour la première partie du projet, les features utilisées sont listées ci-dessous (dupliquées pour chacun des 10 participants de la partie de League of Legendes) :

| Features | signification                                                            | Source         | Type   |
|----------|--------------------------------------------------------------------------|----------------|:--------:|
| Y        | Résultat de la partie                                                    | API (direct)   | bool   |
| CHAMP    | Champion joué sur la partie                                              | API (direct)   | string |
| LVL      | Niveau d'invocateur                                                      | API (direct)   | int    |
| TOTAL    | Nombre de parties jouées sur la saison                                    | API (direct)   | int    |
| GWR      | Winrate en classé sur la saison                                          | API (direct)   | float  |
| VET      | Attribut vétéran du joueur                                               | API (direct)   | bool   |
| RANK     | Rang en classé solo/duo du joueur (elo)                                  | API (direct)   | list   |
| HOT      | Attribut "série de victoires du joueur"                                  | API (direct)   | bool   |
| KDAG     | KDA moyen sur les 5 dernières parties (tous champions)                   | API (5 games)  | list   |
| KDA      | KDA moyen sur les 5 dernières parties (champion de la partie)            | API (5 games)  | list   |
| WR       | Winrate moyen sur les 5 dernières parties (champion de la partie)        | API (5 games)  | float  |
| NB       | Nombre de partie jouées sur le champion sélectionné parmis les 5 dernières | API (5 games)  | int    |
| FILL     | Le joueur joue-t-il sur le même poste que ses 5 dernières parties (autofill)    | API (5 games)  | bool   |
| VS       | Winrate moyen sur le matchup entre les 2 champions d'un même poste        | mobachampion   | float  |
| MAS      | Niveau de maîtrise sur le champion joué                                  | API (direct)   | int    |
| WRCH     | Winrate de la saison sur le champion de la partie                        | scraping u.gg | float  |
| WCH      | Victoires de la saison sur le champion de la partie                      | scraping u.gg | int    |
| LCH      | Défaites de la saison sur le champion de la partie                       | scraping u.gg | int    |
| TOTCH    | Total de parties jouées dans la saison sur le champion de la partie      | scraping u.gg | int    |

Le rapport et la présentation finale pour la soutenance sont disponibles dans ce projet, ainsi que l'application pour laquelle il faut lancer le programme chrec.py
