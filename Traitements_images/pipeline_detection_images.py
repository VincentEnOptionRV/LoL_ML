import cv2
import matplotlib.pyplot as plt # on utilise matplotlib pour afficher les images sinon on fait crash le kernel avec cv2.imshow
import numpy as np
from tensorflow import keras
import tensorflow as tf
import os

def group_show(liste_image,titres):
    """ Pour afficher directement les images par team

    Args
    ----
    liste_image: list
        liste des images à afficher
    titres: list
        titre des images
    """
    if titres == None: # on gère le cas où les titres ne sont pas renseignés
        titres = [None]*len(liste_image)

    fig, ax = plt.subplots(1, len(liste_image), figsize=(20, 20))
    liste_image_modif = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB)for image in liste_image]
    for i in range(len(liste_image_modif)):
        ax[i].imshow(liste_image_modif[i])
        ax[i].set_title(titres[i])

def detection_champ(image,titre):
    """ Fonction qui détecte les champions de la champ select avec des cercles

    Args
    ----
    image: list of numpy.ndarray
        liste d'images dans laquelle on veut détecter les cercles pour un champion : car il y a un décalage entre les deux images
    titre: str
        titre de l'image

    Returns
    -------
    image: numpy.ndarray
        image avec les cercles détectés
    """

    cv2.imwrite(f"{titre}.jpg", image[0])
    img = cv2.imread(f"{titre}.jpg",0)
    
    if len(image)>1:
        cv2.imwrite(f"{titre}.jpg", image[1])
        image_pos_2 = cv2.imread(f"{titre}.jpg",0)

    # increase the contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    # detect and show circles in the "img" image
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,
                                param1=50,param2=30,minRadius=12,maxRadius=50)
    if len(image)>1:
        if circles is not None :
            # on essaie avec la première image
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                mask = np.zeros_like(image[0])
                mask = cv2.circle(mask, (i[0],i[1]), i[2], (255,255,255), -1)
                image[0] = cv2.bitwise_and(image[0], mask)
                # # draw the outer circle
                # cv2.circle(image[0],(i[0],i[1]),i[2],(0,255,0),1)
                return(image[0])
        else :
            # on passe sur la deuxième image si elle existe
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            image_pos_2 = clahe.apply(image_pos_2)
            circles = cv2.HoughCircles(image_pos_2,cv2.HOUGH_GRADIENT,1,80,param1=50,param2=30,minRadius=12,maxRadius=50)
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    mask = np.zeros_like(image[1])
                    mask = cv2.circle(mask, (i[0],i[1]), i[2], (255,255,255), -1)
                    image[1] = cv2.bitwise_and(image[1], mask)

                #     # draw the outer circle
                #     cv2.circle(image[1],(i[0],i[1]),i[2],(0,255,0),1)
            return(image[1])

    elif circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            mask = np.zeros_like(image[0])
            mask = cv2.circle(mask, (i[0],i[1]), i[2], (255,255,255), -1)
            image[0] = cv2.bitwise_and(image[0], mask)

        #     # draw the outer circle
        #     cv2.circle(image[0],(i[0],i[1]),i[2],(0,255,0),1)
    return(image[0])

def predictions(liste_image,nom_model, print_off = False, resnet = False):
    """ Fonction qui prédit les champions à partir des images

    Args
    ----
    liste_image: list of numpy.ndarray
        liste d'images des champions
    nom_model: str
        nom du modèle à utiliser

    Returns
    -------
    predictions: list of str
        liste des champions prédits
    """

    predictions_finales = []
    images_RGB = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB)for image in liste_image]

    # get the max image shape
    max_shape = tuple(max(image.shape[x] for image in images_RGB) for x in range(3))

    # construct an image batch object
    image_to_pred = np.zeros((5,) + max_shape, dtype='float32')

    # copy all images to the upper left part of the image batch object
    for image_index, image in enumerate(images_RGB):
        image_to_pred[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image
    
    if resnet:
        # resize the images
        image_to_pred = tf.image.resize(image_to_pred, (224, 224))
        # preprocess the images
        image_to_pred = tf.keras.applications.resnet.preprocess_input(image_to_pred)

    model = keras.models.load_model(f"{nom_model}")

    # get the predictions for the test data
    predictions = model.predict(image_to_pred)

    # get the five index of highest probability
    top_5 = np.argsort(predictions, axis=1)[:,-5:]


    # Liste des champions dont les labels sont inversés 
    K = ['Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante']
    
    champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

    if print_off == False :
        print(" 5 + grandes probas pour chaque prédiction :")
    for i in range(len(top_5)):
        # inverse la liste pour avoir les plus grandes probas en premier
        liste_top_5 = top_5[i][::-1]
        res_5 = [champions[j] for j in liste_top_5]
        for j in range(len(res_5)): # On gère les problèmes de Draven/DrMundo ainsi que des champions commençant par K
            if res_5[j]=="Draven":
                res_5[j] = "DrMundo"
            elif res_5[j]=="DrMundo":
                res_5[j] = "Draven"
            if res_5[j] in K:
                res_5[j] = K[K.index(res_5[j])-1]
        if print_off == False :
            print(res_5)
        predictions_finales.append(res_5[0])

    return(predictions_finales)

def predictions_globales(image_path):
    """Fonction qui prend en entrée une image de draft et qui renvoie les champoins prédits pour les bans et les picks
    
    Args
    ----
    image_path: str
        chemin de l'image à traiter : ATTENTION : il faut le path absolu de l'image (ie C:/Users/.../image.png)

    Returns
    -------
    res_drafts_pred: dict
        dictionnaire contenant les champs prédits pour les bans et les picks (chaque liste contient 5 champs et à pour clé bans1,picks1, bans2 ou picks2)

    """
    # Get absolute path of current file
    ABS_PATH = os.path.abspath(os.path.dirname(__file__))

    img = cv2.imread(image_path)
    hauteur, largeur = img.shape[:2]

    sep_h_img = int((9/570)*hauteur)
    ratio_deb_h = int((81/570)*hauteur)
    ratio_icon_h = int((55/570)*hauteur)

    liste_champ_1=[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]

    for i in range(len(liste_champ_1)):
        liste_champ_1[i][0] = img[ratio_deb_h+i*(ratio_icon_h+sep_h_img):ratio_deb_h+i*(ratio_icon_h+sep_h_img)+ratio_icon_h, int((40/1019)*largeur):int((40/1019)*largeur)+int((55/1019)*largeur)]
        liste_champ_1[i][1] = img[ratio_deb_h+i*(ratio_icon_h+sep_h_img):ratio_deb_h+i*(ratio_icon_h+sep_h_img)+ratio_icon_h, int((10/1019)*largeur):int((10/1019)*largeur)+int((55/1019)*largeur)]


    sep_h_img = int((9/570)*hauteur)
    ratio_deb_h = int((81/570)*hauteur)
    ratio_icon_h = int((55/570)*hauteur)

    liste_champ_2 = [[],[],[],[],[]]

    for i in range(len(liste_champ_2)):
        liste_champ_2[i].append(img[ratio_deb_h+i*(ratio_icon_h+sep_h_img):ratio_deb_h+i*(ratio_icon_h+sep_h_img)+ratio_icon_h, int((956/1019)*largeur):int((956/1019)*largeur)+int((55/1019)*largeur)])


    titres_1 = ["champ1", "champ2", "champ3", "champ4", "champ5"]
    images_detect_1 = []
    for i,image in enumerate(liste_champ_1):
        images_detect_1.append(detection_champ(image, titres_1[i]))

    titres_2 = ["champ1", "champ2", "champ3", "champ4", "champ5"]
    images_detect_2 = []
    for i,image in enumerate(liste_champ_2):
        images_detect_2.append(detection_champ(image, titres_2[i]))


    sep_l_img = int((8/1019)*largeur)
    ratio_deb_h = int((22/570)*hauteur)

    ratio_icon_l = int((25/1019)*largeur)
    ratio_icon_h = int((25/570)*hauteur)

    ratio_deb_l_1 = int((9/1019)*largeur)
    ratio_deb_l_2 = int((856/1019)*largeur)

    liste_bans_1 = [[],[],[],[],[]]
    liste_bans_2 = [[],[],[],[],[]]

    for i in range(len(liste_champ_2)):
        liste_bans_1[i].append(img[ratio_deb_h:ratio_deb_h+ratio_icon_h,ratio_deb_l_1+i*(ratio_icon_l+sep_l_img):ratio_deb_l_1+i*(ratio_icon_l+sep_l_img)+ratio_icon_l])
        liste_bans_2[i].append(img[ratio_deb_h:ratio_deb_h+ratio_icon_h,ratio_deb_l_2+i*(ratio_icon_l+sep_l_img):ratio_deb_l_2+i*(ratio_icon_l+sep_l_img)+ratio_icon_l])

    liste_bans_1_modif = list(list(zip(*liste_bans_1))[0])

    liste_bans_2_modif = list(list(zip(*liste_bans_2))[0])

    res_drafts_pred = {}
    res_drafts_pred["bans1"]=predictions(liste_bans_1_modif, ABS_PATH + "/modeles/model_24_02", print_off=True)
    group_show(liste_bans_1_modif,res_drafts_pred["bans1"])

    res_drafts_pred["bans2"]=predictions(liste_bans_2_modif, ABS_PATH + "/modeles/model_24_02", print_off=True)
    group_show(liste_bans_2_modif,res_drafts_pred["bans2"])

    res_drafts_pred["champs1"]=predictions(images_detect_1, ABS_PATH + "/modeles/model_24_02", print_off=True)
    group_show(images_detect_1,res_drafts_pred["champs1"])

    res_drafts_pred["champs2"]=predictions(images_detect_2, ABS_PATH + "/modeles/model_24_02", print_off=True)
    group_show(images_detect_2,res_drafts_pred["champs2"])

    return res_drafts_pred


# # Get absolute path of current file
# ABS_PATH = os.path.abspath(os.path.dirname(__file__))
# res = predictions_globales(ABS_PATH + "/" + "exemples_drafts/champ_select4.png")
# print("\n Résultats des prédictions : ",res, "\n")
