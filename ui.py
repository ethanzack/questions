import kivy
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import App
from testsimilarity_FORUI import pipeline


kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label

def testsimilarity(groups, curr, text):
    # pipeline(False, text)
    if not groups:
        inpArr = text.splitlines()
        return pipeline(False, curr, inpArr)
    else:
        pipeline(True, curr, "")

class storeQuestions:
    currentQuestions = []
    def __init__(self):
        self.currQuestions = []

    def testsim(self, text):
        self.update(testsimilarity(False, self.currQuestions, text))

    def getCurr(self):
        outputStr = ""
        i = 1
        for group in self.currQuestions:
            outputStr = outputStr + "Group " + str(i) + ": " + str(group) + "\n"
            i = i + 1

        return outputStr

    def update(self, qs):
        self.currQuestions = qs

class MyApp(App):
    def build(self):
        qstore = storeQuestions()

        layout = BoxLayout(spacing=10, orientation='vertical')
        textinput = TextInput(text="Enter a question or questions in this space\nEach Question Should Go on its Own Line", font_size = 45)
        btn2 = Button(text='Analyze Questions', size_hint=(1, .3))
        btn3 = Button(text='Show Groups', size_hint=(1, .3))

        # pipeLineCallBack = lambda x: self.setCurr(testsimilarity(self, self.getCurr(), textinput.text))
        pipeLineCallBack = lambda x: qstore.testsim(textinput.text)
        groupsCallBack = lambda x: Popup(title='Output',
                content=Label(text=str(qstore.getCurr())),
                size_hint=(.7, .5), size=(1000, 1000)).open()

        btn2.bind(on_press=pipeLineCallBack)
        btn3.bind(on_press=groupsCallBack)

        layout.add_widget(textinput)
        layout.add_widget(btn2)
        layout.add_widget(btn3)


        return layout



if __name__ == '__main__':
    MyApp().run()
