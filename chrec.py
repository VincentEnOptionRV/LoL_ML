import os
import sys

sys.path.append('recommendation')

from recommendation.main import predictChampions,orderChamps
from Traitements_images.pipeline_detection_images import predictions_globales

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
ratio = 4.0/3.0
Window.size = (Window.size[0],1/ratio*Window.size[0])
import kivy as kv
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, StringProperty
from kivy.app import App

class Global():
    pseudo = None
    pos = None
    side = None # True si blue_side
    role = None
    KEY = "RGAPI-7bf9de0a-3435-47d4-b447-623e46492a44"
    champions_labels = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']


class Champion(Image):
    champion = StringProperty('blank')

    def changeChamp(self, instance, champion):
        if champion != '':
            self.source = 'Traitements_images/images_draft/' + champion + '/' + champion + '_0.jpg'
        else:
            self.source = 'Interface/no_champ.PNG'

    def __init__(self, champion, text=None, **kwargs):
        super(Champion, self).__init__(**kwargs)
        self.bind(champion=self.changeChamp)
        self.champion = champion

class PickedWidget(BoxLayout):
    liste_champions = ListProperty(['blank']*5)

    def changeChampList(self, instance, liste_champions):
        for i in range(5):
            if i < len(liste_champions):
                champion = liste_champions[i]
            else:
                champion = ''
            
            if len(self.children) < 5:
                self.add_widget(Champion(champion))
            else:
                self.children[-i-1].champion = champion

    def __init__(self, liste_champions, **kwargs):
        super(PickedWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.bind(liste_champions=self.changeChampList)
        self.liste_champions = liste_champions

class BannedWidget(PickedWidget):
    def __init__(self, liste_champions, **kwargs):
        super().__init__(liste_champions, **kwargs)
        self.orientation = 'horizontal'

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 0.3*self.width

class BGImg (Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.source = 'Interface/map.jpg'

class CustomButton(Button):
    def __init__(self, mode1, arg=None, **kwargs):
        super().__init__(**kwargs)
        self.mode1 = mode1
        self.arg = arg
    
    def on_release(self):
        if self.mode1 == 0:
            TestApp.on_press_first_pick(self.arg)
        elif self.mode1 == 1:
            TestApp.on_press_role(self.arg)
        elif self.mode1 == 2:
            TestApp.on_press_team_pos(self.arg)
        elif self.mode1 == 3:
            TestApp.predict()
        elif self.mode1 == 4:
            TestApp.reset()

class TestApp(App):
    def reset():
        app = App.get_running_app()
        while len(app.root.children) > 1:
            app.root.remove_widget(app.root.children[0])
        
        app.root.add_widget(BGImg())
        app.root.add_widget(PickedWidget([], pos_hint={'x':0,'y':0}, size_hint=(.85/5/ratio,.85))) # Alliés
        app.root.add_widget(PickedWidget([], pos_hint={'x':1-0.85/5/ratio,'y':0}, size_hint=(.85/5/ratio,.85))) # Ennemis
        app.root.add_widget(BannedWidget([], pos_hint={'x':0,'y':.9}, size_hint=(.3,.1))) # Bans alliés
        app.root.add_widget(BannedWidget([], pos_hint={'x':.7,'y':.9}, size_hint=(.3,.1))) # Bans ennemis
        app.root.add_widget(CustomButton(4, pos_hint={'x':.45,'y':.95}, size_hint=(.1,.05), text='Reset')) # Reset

        textinput = TextInput(hint_text='Votre pseudo LoL', multiline=False, pos_hint={'x':.3,'y':.8}, size_hint=(.4,.05))
        textinput.bind(on_text_validate=TestApp.on_enter_username)
        app.root.add_widget(textinput)

    def build(self):
        self.title = 'League of Legends CHREC (Champion Recommendation)'
        self.icon = 'Interface/icon.jpg'

        root = FloatLayout()
        root.add_widget(BGImg())
        root.add_widget(PickedWidget([], pos_hint={'x':0,'y':0}, size_hint=(.85/5/ratio,.85))) # Alliés
        root.add_widget(PickedWidget([], pos_hint={'x':1-0.85/5/ratio,'y':0}, size_hint=(.85/5/ratio,.85))) # Ennemis
        root.add_widget(BannedWidget([], pos_hint={'x':0,'y':.9}, size_hint=(.3,.1))) # Bans alliés
        root.add_widget(BannedWidget([], pos_hint={'x':.7,'y':.9}, size_hint=(.3,.1))) # Bans ennemis
        root.add_widget(CustomButton(4, pos_hint={'x':.45,'y':.95}, size_hint=(.1,.05), text='Reset')) # Reset

        textinput = TextInput(hint_text='Votre pseudo LoL', multiline=False, pos_hint={'x':.3,'y':.8}, size_hint=(.4,.05))
        textinput.bind(on_text_validate=TestApp.on_enter_username)
        root.add_widget(textinput)
        return root

    def on_enter_username(instance):
        Global.pseudo = instance.text

        app = App.get_running_app()
        app.root.remove_widget(app.root.children[0])
        text = CustomLabel(text='Qui a le choix du premier champion ?',pos_hint={'x':0.3,'y':0.6}, size_hint=(.4,.1))
        app.root.add_widget(text)
        allies = CustomButton(0,True,pos_hint={'x':.25,'y':.5}, size_hint=(.15,.1),text="Alliés")
        app.root.add_widget(allies)
        ennemies = CustomButton(0,False,pos_hint={'x':.6,'y':.5}, size_hint=(.15,.1),text="Ennemis")
        app.root.add_widget(ennemies)


    def on_press_first_pick(allies):
        Global.side = allies

        app = App.get_running_app()
        for _ in range(3): app.root.remove_widget(app.root.children[0])
        role_list = ['TOP','JGL','MID','ADC','SUP']
        text = CustomLabel(text='Quelle est votre rôle dans l\'équipe ?',pos_hint={'x':0.3,'y':0.6}, size_hint=(.4,.1))
        app.root.add_widget(text)
        for i in range(5):
            app.root.add_widget(CustomButton(1,role_list[4-i],pos_hint={'x':0.4,'y':0.1 + 0.1*i}, size_hint=(.2,.07), text=role_list[4-i]))


    def on_press_role(r):
        Global.role = r

        app = App.get_running_app()
        for _ in range(6): app.root.remove_widget(app.root.children[0])
        text = CustomLabel(text='Quelle est votre position dans la sélection ?',pos_hint={'x':0.3,'y':0.6}, size_hint=(.4,.1))
        app.root.add_widget(text)
        for i in range(5):
            app.root.add_widget(CustomButton(2,4-i,pos_hint={'x':0,'y':0.17*i}, size_hint=(.17/ratio,.17)))

    def on_press_team_pos(num):
        Global.pos = int(num)
        app = App.get_running_app()
        for _ in range(6): app.root.remove_widget(app.root.children[0])
        img = Image(pos_hint={'x':0.1,'y':0.171*(4-int(num))}, size_hint=(.045,.165))
        img.source = 'Interface/you.png'
        app.root.add_widget(img)
        textinput = TextInput(hint_text='Nom de la capture d\'écran', multiline=False, pos_hint={'x':.3,'y':.85}, size_hint=(.4,.05))
        textinput.bind(on_text_validate=TestApp.on_enter_screenshot_file)
        app.root.add_widget(textinput)

    def on_enter_screenshot_file(instance):
        app = App.get_running_app()
        for _ in range(len(app.root.children) - 8): app.root.remove_widget(app.root.children[0])
        app.root.children[-2].liste_champions = []
        app.root.children[-3].liste_champions = []
        app.root.children[-4].liste_champions = []
        app.root.children[-5].liste_champions = []
        TestApp.pipeline(instance.text)

    def pipeline(filename):
        app = App.get_running_app()

        pos = Global.pos
        role = Global.role
        side = Global.side
        champions_labels = Global.champions_labels

        roles_labels = ["TOP","JGL","MID","ADC","SUP"]
        
        res = predictions_globales(ABS_PATH + "/" + filename)
        blue_picks = [0,3,4,7,8]
        red_picks = [1,2,5,6,9]
        draft_order =  blue_picks[pos] if side else red_picks[pos]
        Global.role_id = roles_labels.index(role)
        Global.bans = res['bans1'] + res['bans2']
        blue = res['champs1'] if side else res['champs2']
        red = res['champs2'] if side else res['champs1']
        Global.blue_locks = []
        blue_locks_name = []
        Global.red_locks = []
        red_locks_name = []
        for i in range(5):
            if blue_picks[i]<draft_order:
                Global.blue_locks.append(champions_labels.index(blue[i]))
                blue_locks_name.append(blue[i])
            if red_picks[i]<draft_order:
                Global.red_locks.append(champions_labels.index(red[i]))
                red_locks_name.append(red[i])
        Global.roles = [i for i in range(5)]
        Global.roles[pos] = Global.role_id
        Global.roles[Global.role_id] = pos

        app.root.children[-2].liste_champions = blue_locks_name if Global.side else red_locks_name
        app.root.children[-3].liste_champions = red_locks_name if Global.side else blue_locks_name
        app.root.children[-4].liste_champions = res['bans1']
        app.root.children[-5].liste_champions = res['bans2']

        text = CustomLabel(text='Remplacer les prédictions incorrectes',pos_hint={'x':0.3,'y':0.6}, size_hint=(.4,.1))
        app.root.add_widget(text)

        for i in range(len(res['bans1'])):
            textinput = TextInput(hint_text=f'Ban Allié {i+1}', multiline=False, pos_hint={'x':.17,'y':.5-i*.1}, size_hint=(.13,.05))
            textinput.bind(on_text_validate=TestApp.on_replace_prediction)
            textinput.id = f'ba{i}'
            app.root.add_widget(textinput)
        
        for i in range(len(res['bans2'])):
            textinput = TextInput(hint_text=f'Ban Ennemi {i+1}', multiline=False, pos_hint={'x':1-.17-.13,'y':.5-i*.1}, size_hint=(.13,.05))
            textinput.bind(on_text_validate=TestApp.on_replace_prediction)
            textinput.id = f'be{i}'
            app.root.add_widget(textinput)
        
        for i in range(len(app.root.children[-2].liste_champions)):
            textinput = TextInput(hint_text=f'Ch. Allié {i+1}', multiline=False, pos_hint={'x':.3,'y':.5-i*.1}, size_hint=(.13,.05))
            textinput.bind(on_text_validate=TestApp.on_replace_prediction)
            textinput.id = f'ca{i}'
            app.root.add_widget(textinput)
        
        for i in range(len(app.root.children[-3].liste_champions)):
            textinput = TextInput(hint_text=f'Ch. Ennemi {i+1}', multiline=False, pos_hint={'x':.7-.13,'y':.5-i*.1}, size_hint=(.13,.05))
            textinput.bind(on_text_validate=TestApp.on_replace_prediction)
            textinput.id = f'ce{i}'
            app.root.add_widget(textinput)
        
        app.root.add_widget(CustomButton(3,pos_hint={'x':.4,'y':0.01}, size_hint=(.2,.07), text="Valider"))


    def on_replace_prediction(instance):
        what_replace = instance.id[:2]
        which_replace = int(instance.id[2])
        app = App.get_running_app()
        if what_replace == 'ba':
            app.root.children[-4].liste_champions[which_replace] = instance.text
            Global.bans[which_replace] = Global.champions_labels.index(instance.text)
        elif what_replace == 'be':
            app.root.children[-5].liste_champions[which_replace] = instance.text
            Global.bans[which_replace+5] = Global.champions_labels.index(instance.text)
        elif what_replace == 'ca':
            app.root.children[-2].liste_champions[which_replace] = instance.text
            if Global.side:
                Global.blue_locks[which_replace] = Global.champions_labels.index(instance.text)
            else:
                Global.red_locks[which_replace] = Global.champions_labels.index(instance.text)
        elif what_replace == 'ce':
            app.root.children[-3].liste_champions[which_replace] = instance.text
            if not Global.side:
                Global.blue_locks[which_replace] = Global.champions_labels.index(instance.text)
            else:
                Global.red_locks[which_replace] = Global.champions_labels.index(instance.text)

    
    def predict():
        app = App.get_running_app()
        for _ in range(12 + len(app.root.children[-2].liste_champions) + len(app.root.children[-3].liste_champions)):
            app.root.remove_widget(app.root.children[0])

        L,scores,banned=predictChampions(Global.bans,Global.blue_locks,Global.red_locks,Global.roles,Global.side,Global.pos,Global.pseudo,Global.KEY,verbose=False)
        X = orderChamps(L,scores,banned,Global.role_id)
        X.reverse()
        recommandation = X
        for val,champ in recommandation:
            print(f"{Global.champions_labels[champ]} : {val:.2f}")
        
        text = CustomLabel(text='Champions recommandés',pos_hint={'x':0.3,'y':0.75}, size_hint=(.4,.1))
        app.root.add_widget(text)

        app.root.add_widget(Champion(Global.champions_labels[recommandation[0][1]], pos_hint={'x':0.375,'y':0.5}, size_hint=(.25,.25)))
        app.root.add_widget(CustomLabel(text=f"{recommandation[0][0]:.1f}", pos_hint={'x':0.35,'y':0.5}, size_hint=(.3,.1)))

        gridC = GridLayout(cols=5, pos_hint={'x':0.15,'y':0.05}, size_hint=(.7,.4))
        gridT = GridLayout(cols=5, pos_hint={'x':0.15,'y':0}, size_hint=(.7,.4))
        app.root.add_widget(gridC)
        app.root.add_widget(gridT)
        for val,champ in recommandation[1:]:
            gridC.add_widget(Champion(Global.champions_labels[champ]))
            gridT.add_widget(CustomLabel(text=f"{val:.1f}"))





        




if __name__ == "__main__":
    TestApp().run()