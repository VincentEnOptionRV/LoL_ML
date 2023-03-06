import kivy as kv
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window

class Champion(Image):
    def __init__(self, champion, **kwargs):
        super(Champion, self).__init__(**kwargs)
        if champion is not None:
            self.source = '../Traitements_images/images_draft/' + champion + '/' + champion + '_0.jpg'
        else:
            self.source = 'no_champ.PNG'

class PickedWidget(BoxLayout):
    def __init__(self, liste_champions, **kwargs):
        super(PickedWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        for i in range(5):
            if i < len(liste_champions):
                champion = liste_champions[i]
            else:
                champion = None
            
            c = Champion(champion)
            self.add_widget(c)

class BannedWidget(PickedWidget):
    def __init__(self, liste_champions, **kwargs):
        super().__init__(liste_champions, **kwargs)
        self.orientation = 'horizontal'

class RecommandationWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = CustomLabel(text='RECOMMANDED CHAMPIONS',pos_hint={'x':0.2,'y':0.8}, size_hint=(.6,.2))
        self.add_widget(l)

class CustomLabel(Label):
    def on_resize(self, *args):
        self.font_size = 0.5*self.height

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 0.5*self.height
        Window.bind(size=self.on_resize)

    
class TestApp(App):

    def build(self):
        self.title = 'League of Legends CHREC (Champion Recommendation)'
        self.icon = '../Traitements_images/images_draft/Rammus/Rammus_0.jpg'

        root = FloatLayout()
        root.add_widget(PickedWidget(['Akali','Samira','Soraka'], pos_hint={'x':0,'y':0}, size_hint=(.25,.85)))
        root.add_widget(PickedWidget(['Azir','Jinx'], pos_hint={'x':0.75,'y':0}, size_hint=(.25,.85)))
        root.add_widget(BannedWidget(['Xerath','Alistar','Zeri'], pos_hint={'x':0,'y':.9}, size_hint=(.4,.1)))
        root.add_widget(BannedWidget(['Blitzcrank','Ahri','Aatrox','Morgana'], pos_hint={'x':.6,'y':.9}, size_hint=(.4,.1)))
        root.add_widget(RecommandationWidget(pos_hint={'x':0.25,'y':0}, size_hint=(.5,.85)))
        return root


if __name__ == '__main__':
    TestApp().run()