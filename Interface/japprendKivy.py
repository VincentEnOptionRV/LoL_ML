from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
ratio = 4.0/3.0
Window.size = (Window.size[0],1/ratio*Window.size[1])

import kivy as kv
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty
from kivy.app import App

pseudo = "Arkyce"
pos = 4
side = False #blue_side
role = "SUP"
KEY = "RGAPI-b68df1a9-ab31-4bcf-98e1-f5f435ed5037"
champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

class Champion(Image):
    champion = StringProperty('blank')

    def changeChamp(self, instance, champion):
        if champion != '':
            self.source = '../Traitements_images/images_draft/' + champion + '/' + champion + '_0.jpg'
        else:
            self.source = 'no_champ.PNG'

    def __init__(self, champion, **kwargs):
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

class RecommandationWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = CustomLabel(text='RECOMMANDED CHAMPIONS',pos_hint={'x':0.3,'y':0.8}, size_hint=(.4,.2))
        self.add_widget(l)

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 0.3*self.width

class But(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_release(self):
        TestApp.in_session()

class TestApp(App):
    def build(self):
        self.title = 'League of Legends CHREC (Champion Recommendation)'
        self.icon = '../Traitements_images/images_draft/Rammus/Rammus_0.jpg'

        root = FloatLayout()
        root.add_widget(PickedWidget(['Akali','Samira','Soraka'], pos_hint={'x':0,'y':0}, size_hint=(.85/5/ratio,.85)))
        root.add_widget(PickedWidget(['Azir','Jinx'], pos_hint={'x':1-0.85/5/ratio,'y':0}, size_hint=(.85/5/ratio,.85)))
        root.add_widget(BannedWidget(['Xerath','Alistar','Zeri'], pos_hint={'x':0,'y':.9}, size_hint=(.3,.1)))
        root.add_widget(BannedWidget(['Blitzcrank','Ahri','Aatrox','Morgana'], pos_hint={'x':.7,'y':.9}, size_hint=(.3,.1)))
        root.add_widget(RecommandationWidget(pos_hint={'x':0.25,'y':0}, size_hint=(.5,.85)))
        root.add_widget(But(pos_hint={'x':0.4,'y':0.4}, size_hint=(.3,.3)))
        return root
    
    def in_session():
        app= App.get_running_app()
        app.root.children[-2].liste_champions = ['Camille','Garen','Vi']


if __name__ == '__main__':
    TestApp().run()