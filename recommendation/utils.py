import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup as bs
import requests
import re

ch_id = {'aatrox': '266',
 'ahri': '103',
 'akali': '84',
 'akshan': '166',
 'alistar': '12',
 'amumu': '32',
 'anivia': '34',
 'annie': '1',
 'aphelios': '523',
 'ashe': '22',
 'aurelionsol': '136',
 'azir': '268',
 'bard': '432',
 'belveth': '200',
 'blitzcrank': '53',
 'brand': '63',
 'braum': '201',
 'caitlyn': '51',
 'camille': '164',
 'cassiopeia': '69',
 'chogath': '31',
 'corki': '42',
 'darius': '122',
 'diana': '131',
 'draven': '119',
 'drmundo': '36',
 'ekko': '245',
 'elise': '60',
 'evelynn': '28',
 'ezreal': '81',
 'fiddlesticks': '9',
 'fiora': '114',
 'fizz': '105',
 'galio': '3',
 'gangplank': '41',
 'garen': '86',
 'gnar': '150',
 'gragas': '79',
 'graves': '104',
 'gwen': '887',
 'hecarim': '120',
 'heimerdinger': '74',
 'illaoi': '420',
 'irelia': '39',
 'ivern': '427',
 'janna': '40',
 'jarvaniv': '59',
 'jax': '24',
 'jayce': '126',
 'jhin': '202',
 'jinx': '222',
 'kaisa': '145',
 'kalista': '429',
 'karma': '43',
 'karthus': '30',
 'kassadin': '38',
 'katarina': '55',
 'kayle': '10',
 'kayn': '141',
 'kennen': '85',
 'khazix': '121',
 'kindred': '203',
 'kled': '240',
 'kogmaw': '96',
 'ksante': '897',
 'leblanc': '7',
 'leesin': '64',
 'leona': '89',
 'lillia': '876',
 'lissandra': '127',
 'lucian': '236',
 'lulu': '117',
 'lux': '99',
 'malphite': '54',
 'malzahar': '90',
 'maokai': '57',
 'masteryi': '11',
 'missfortune': '21',
 'wukong': '62',
 'mordekaiser': '82',
 'morgana': '25',
 'nami': '267',
 'nasus': '75',
 'nautilus': '111',
 'neeko': '518',
 'nidalee': '76',
 'nilah': '895',
 'nocturne': '56',
 'nunu': '20',
 'olaf': '2',
 'orianna': '61',
 'ornn': '516',
 'pantheon': '80',
 'poppy': '78',
 'pyke': '555',
 'qiyana': '246',
 'quinn': '133',
 'rakan': '497',
 'rammus': '33',
 'reksai': '421',
 'rell': '526',
 'renata': '888',
 'renekton': '58',
 'rengar': '107',
 'riven': '92',
 'rumble': '68',
 'ryze': '13',
 'samira': '360',
 'sejuani': '113',
 'senna': '235',
 'seraphine': '147',
 'sett': '875',
 'shaco': '35',
 'shen': '98',
 'shyvana': '102',
 'singed': '27',
 'sion': '14',
 'sivir': '15',
 'skarner': '72',
 'sona': '37',
 'soraka': '16',
 'swain': '50',
 'sylas': '517',
 'syndra': '134',
 'tahmkench': '223',
 'taliyah': '163',
 'talon': '91',
 'taric': '44',
 'teemo': '17',
 'thresh': '412',
 'tristana': '18',
 'trundle': '48',
 'tryndamere': '23',
 'twistedfate': '4',
 'twitch': '29',
 'udyr': '77',
 'urgot': '6',
 'varus': '110',
 'vayne': '67',
 'veigar': '45',
 'velkoz': '161',
 'vex': '711',
 'vi': '254',
 'viego': '234',
 'viktor': '112',
 'vladimir': '8',
 'volibear': '106',
 'warwick': '19',
 'xayah': '498',
 'xerath': '101',
 'xinzhao': '5',
 'yasuo': '157',
 'yone': '777',
 'yorick': '83',
 'yuumi': '350',
 'zac': '154',
 'zed': '238',
 'zeri': '221',
 'ziggs': '115',
 'zilean': '26',
 'zoe': '142',
 'zyra': '143'}

roles = ["TOP","JGL","MID","ADC","SUP"]
stats = ["LVL","TOTAL","GWR","HOT","FILL","RANK","VS","MAS","WCH","LCH","TOTCH","WRCH"]

def badRequestsHandler(url):
    r = requests.get(url)
    while r.status_code == 429: #éventuellement à revoir
        time.sleep(5)
        r = requests.get(url)
    if r.status_code == 400:
        print(r.text)
        raise Exception("Requête invalide")
    elif r.status_code == 401:
        raise Exception("Unauthorized")
    elif r.status_code == 403:
        raise Exception("Non autorisé: vérifiez la clé")
    elif r.status_code == 404:
        raise Exception("Données non trouvées")
    elif r.status_code == 405:
        raise Exception("Méthode non autorisée")
    elif r.status_code == 415:
        raise Exception("Unsupported media type")
    elif r.status_code == 500:
        raise Exception("Internal server error")
    elif r.status_code == 502:
        raise Exception("Bad gateway")
    elif r.status_code == 503:
        raise Exception("Service non disponible")
    elif r.status_code == 504:
        raise Exception("Gateway timeout")
    elif r.status_code == 200:
        return r.json()

def requestSummonerInfo(summoner_name,key):
    return badRequestsHandler(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={key}")

def requestRankedInfo(summoner_id,key):
    data = badRequestsHandler(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={key}")
    if len(data)==2 and data[0]['queueType']!='RANKED_SOLO_5x5':
        return [data[1],data[0]]
    return data

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

def getMasteries(encryptedSummonerId, championId, key):
    return badRequestsHandler(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}/by-champion/{championId}?api_key={key}")

def getScrapped(summoner):
    url = f"https://u.gg/lol/profile/euw1/{summoner}/champion-stats?season=18&queueType=ranked_solo_5x5"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "lxml")
    rates = soup.find_all('div', class_="champion-rates")
    names = soup.find_all('span', class_="champion-name")
    D = []
    for i in range(len(rates)):
        c = re.sub(r'[^a-zA-Z]','',names[i].text.lower())
        w = list(map(int,re.findall(r'\d+', rates[i].text)))
        D.append([c]+[w[1],w[2],w[1]/(w[1]+w[2]),w[1]+w[2]])
    return D

def getConstantValues(summoner,KEY):
    try: #au cas où un problème survient (tellement de requêtes que ça arrive de temps en temps, il faudrait regarder dans le détail...)
        summoner_info = requestSummonerInfo(summoner,KEY)
        summoner_id = summoner_info['id']
        puuid = summoner_info['puuid']
        LVL = summoner_info['summonerLevel']
        ranked_info = requestRankedInfo(summoner_id,KEY)[0]
        TOTAL = ranked_info["wins"]+ranked_info["losses"]
        GWR = ranked_info["wins"]/(TOTAL)
        RANK = [ranked_info['tier'],ranked_info['rank'],ranked_info['leaguePoints']]
        HOT = ranked_info['hotStreak']
        FILL = False
    except Exception as ex:
        print(ex)
    else:
        pass
    return [LVL,TOTAL,GWR,HOT,False,elo(RANK)], summoner_id

def formate(c):
    c = c.lower()
    if c == 'wukong':
        return 'monkeyking'
    return c
    
def winrate(c1,c2):
    url = f"https://www.mobachampion.com/counter/{formate(c1)}-vs-{formate(c2)}/"
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    counters = soup.find_all('div', class_="flex flex-row items-center")
    return float(counters[-2].text.replace("","").replace("%","").replace("\n","").replace(" ", ""))

def getValues(summoner,opponent,KEY):
    M = getScrapped(summoner)
    X = []
    L = []
    const, summoner_id = getConstantValues(summoner,KEY)
    for i in range(len(M)):
        X.append(const + [0.5 if opponent is None or opponent.lower()==M[i][0].lower() else winrate(M[i][0],opponent)] + [getMasteries(summoner_id,int(ch_id[M[i][0]]),KEY)['championPoints']] + M[i][1:])
        L.append(M[i][0])
    return L,X

if __name__ == "__main__":
    L,X = getValues("agurin","warwick","RGAPI-f4ac39da-ec2d-4c99-a2c1-83e54ada1a41")
    print(X)