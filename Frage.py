#!/usr/bin/env python
# *-* coding: utf-8 *-*

from tkinter import *
import random
import json


class Frage(object):
    feedback = (False, 'test', 'test2')

    def __init__(self, kategorie, team='winner'):
        self.frage = Toplevel()
        self.frage.geometry('800x120+400+400')
        self.frage.title('Frage zu der Kategorie ' + kategorie)
        fragenFile = open('fragen_neu.txt')
        fragenJson = json.load(fragenFile)
        frageText = Label(self.frage,
                          text=fragenJson[kategorie][0]['Frage'])
        frageText.pack()
        antwort1 = Button(self.frage,
                          text=fragenJson[kategorie][0]['Richtig'],
                          command=lambda feedback=(True, kategorie, 'chicken'): self.getFeedback(feedback),
                          width=700)
        antwort2 = Button(self.frage,
                          text=fragenJson[kategorie][0]['Falsch1'],
                          command=lambda feedback=(False, kategorie, 'chicken'): self.getFeedback(feedback),
                          width=700)
        antwort3 = Button(self.frage,
                          text=fragenJson[kategorie][0]['Falsch2'],
                          command=lambda feedback=(False, kategorie, 'chicken'): self.getFeedback(feedback),
                          width=700)
        antworten = [antwort1, antwort2, antwort3]
        random.shuffle(antworten)
        for a in antworten:
            a.pack()


    def getFeedback(self, feedback):
        self.feedback=feedback
        self.frage.destroy()

