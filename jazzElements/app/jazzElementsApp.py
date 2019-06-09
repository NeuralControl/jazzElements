# KIVY
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, NumericProperty
import sys

sys.path.append('d:\\Code\\jazzElements\\')
from jazzElements.progression import Progression
from jazzElements.chord import Chord
from jazzElements.note import Note


class WdgRoundedButton(BoxLayout):
    pass


class ScrMain(Screen):
    pass


class WdgChordName(Button):
    note = StringProperty(None)
    alt = StringProperty(None)
    type = StringProperty(None)
    duration = NumericProperty(1)


class WdgMeasure(WdgRoundedButton):
    def addChord(self, root, alt, type, duration):
        self.add_widget(WdgChordName(note=root, alt=alt, type=type, duration=duration))


class WdgProgression(BoxLayout):
    title = StringProperty('Unknown')

    def addMeasure(self):
        m = WdgMeasure()
        self.add_widget(m)
        return m


class JazzElementsApp(App):
    def __init__(self):
        super().__init__()

    def build(self):
        self.bgdColor = (0.282, 0.31, 0.34, 1)
        Window.clearcolor = self.bgdColor
        self.title = 'Jazz Elements'
        self.root = ScreenManager()
        self.root.add_widget(ScrMain(name='Main'))
        self.scrMain = self.root.get_screen('Main')
        self.wdgPrg = self.scrMain.ids['progression']
        bar = []
        bar.append(self.wdgPrg.addMeasure())
        bar[-1].addChord('E', '', 'm7', 1)
        bar[-1].addChord('C', '', 'm7', 1)
        bar[-1].addChord('%', '', '', 1)
        bar[-1].addChord('%', '', '', 1)

        self.prg = Progression('Misty')

        return self.root


if __name__ == '__main__':
    JazzElementsApp().run()
