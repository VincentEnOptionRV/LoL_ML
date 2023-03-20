import os
import sys

sys.path.append('recommendation')

from recommendation.main import predictChampions,orderChamps
from Traitements_images.pipeline_detection_images import predictions_globales


ABS_PATH = os.path.abspath(os.path.dirname(__file__))

champions_labels = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
roles_labels = ["TOP","JGL","MID","ADC","SUP"]

def pipeline(pseudo,side,pos,role,KEY):
    res = predictions_globales(ABS_PATH + "/" + "Interface/draft.png")
    blue_picks = [0,3,4,7,8]
    red_picks = [1,2,5,6,9]
    draft_order =  blue_picks[pos] if side else red_picks[pos]
    role_id = roles_labels.index(role)
    bans = res['bans1'] + res['bans2']
    blue = res['champs1'] if side else ['champs2']
    red = res['champs2'] if side else ['champs1']
    blue_locks = []
    red_locks = []
    for i in range(5):
        if blue_picks[i]<draft_order:
            blue_locks.append(champions_labels.index(blue[i]))
        if red_picks[i]<draft_order:
            red_locks.append(champions_labels.index(red[i]))
    roles = [i for i in range(5)]
    roles[pos] = role_id
    roles[role_id] = pos
    L,scores,banned=predictChampions(bans,blue_locks,red_locks,roles,side,pos,pseudo,KEY,verbose=False)
    X = orderChamps(L,scores,banned,role_id)
    return X[-1][1]

if __name__ == "__main__":
    pseudo = "agurin"
    pos = 4
    side = True #blue_side
    role = "JGL"
    KEY = "RGAPI-bb1e3828-b34b-4d61-b17d-d8510e226cb5"
    r = champions_labels[pipeline(pseudo,side,pos,role,KEY)]
    print(r)