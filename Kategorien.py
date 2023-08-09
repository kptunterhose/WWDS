#!/usr/bin/env python
### *-* coding: utf-8 *-*
import tkinter.colorchooser
from tkinter import *
import json
import random

NAMEFRAGENFILE = "fragen_neu.txt"

TEAMS = {
    'Team 1': {
        'Punkte': 0,
        'Name': 'A',
        'Farbe': 'red'
    },
    'Team 2': {
        'Punkte': 0,
        'Name': 'B',
        'Farbe': 'blue'
    }
}


class Kategorien(object):
    kategorienListe = []
    masterKategorie = ''
    kategorienButtons = {}
    team1aktiv = True
    kategorieAktiv = False
    antwortEinloggen = False
    counter = 0
    first = True
    bildschirmBreite = 0
    bildschirmHoehe = 0
    geometrieUebersicht = '830x420+10+10'
    geometrieTeams = ''
    geometrieFragen = ''

    def __init__(self, kategorienListe):
        self.Uebersicht = Tk()  # heigth = 450, width = 700
        self.background = Toplevel()
        self.background.attributes('-fullscreen', True)
        self.background.config(background='black')

        if len(kategorienListe) == 13:
            self.kategorienListe = kategorienListe
        else:
            print('Es müssen 12+1 Kategorien+Master sein. Es sind aber ' + str(len(kategorienListe)))

        self.Uebersicht.attributes('-topmost', True)
        self.bildschirmBreite = self.Uebersicht.winfo_screenwidth()
        self.bildschirmHoehe = self.Uebersicht.winfo_screenheight()
        self.calcFensterGeometrie()
        self.Uebersicht.geometry(self.geometrieUebersicht)  # width x height + x-offset + y-offset
        self.Uebersicht.title('Wer weiß denn sowas?')
        self.Uebersicht.configure(background='darkblue')
        self.Teams = Toplevel()
        self.Teams.attributes('-topmost', True)
        self.Teams.geometry(self.geometrieTeams)
        self.Teams.title('Aktueller Stand')
        self.Teams.configure(background='black')
        a = StringVar()
        a.set('Team A')
        b = StringVar()
        b.set('Team B')
        self.Team1 = Entry(self.Teams, textvariable=a)
        self.Team1.grid(row=0, column=0, padx=10, pady=10)
        self.Team1.config(font=('Times', 25),
                          width=10)
        self.Team2 = Entry(self.Teams, textvariable=b)
        self.Team2.grid(row=0, column=1, padx=10, pady=10)
        self.Team2.config(font=('Times', 25),
                          width=10)
        self.Team1Farbe = Button(self.Teams,
                                 text='Farbe',
                                 command=self.farbwahl1)
        self.Team2Farbe = Button(self.Teams,
                                 text='Farbe',
                                 command=self.farbwahl2)
        self.Team1Farbe.grid(row=1, column=0)
        self.Team2Farbe.grid(row=1, column=1)
        self.start = Button(self.Teams, text='Start', command=self.startRunde)
        self.start.grid(row=2, column=0, columnspan=2)
        self.start.config(font=('Times', 25))

    def calcFensterGeometrie(self):
        self.geometrieUebersicht = '830x420+10+10'
        xoffsetTeams = self.bildschirmBreite - 420 - 10
        self.geometrieTeams = '420x420+' + str(xoffsetTeams) + '+10'
        xoffsetFragen = (self.bildschirmBreite - 1100) / 2
        yoffsetFragen = self.bildschirmHoehe - 500
        self.geometrieFragen = '1100x400+' + str(int(xoffsetFragen)) + '+' + str(yoffsetFragen)

    def farbwahl1(self):
        farbe = tkinter.colorchooser.askcolor(title='Farbwahl für Team A', parent=self.Teams)
        TEAMS['Team 1']['Farbe'] = farbe[1]

    def farbwahl2(self):
        farbe = tkinter.colorchooser.askcolor(title='Farbwahl für Team B', parent=self.Teams)
        TEAMS['Team 2']['Farbe'] = farbe[1]

    def startRunde(self):
        for i in range(len(self.kategorienListe[0:-1])):
            self.kategorienButtons[self.kategorienListe[i]].config(state=NORMAL)
        TEAMS['Team 1']['Name'] = self.Team1.get()
        TEAMS['Team 2']['Name'] = self.Team2.get()
        self.Team1.grid_forget()
        self.Team2.grid_forget()
        self.Team1Farbe.grid_forget()
        self.Team2Farbe.grid_forget()
        self.start.grid_forget()
        self.Team1Name = Label(self.Teams, text=TEAMS['Team 1']['Name'])
        self.Team1Punkte = Label(self.Teams, text='0')
        self.Team2Name = Label(self.Teams, text=TEAMS['Team 2']['Name'])
        self.Team2Punkte = Label(self.Teams, text='0')
        self.Team1Name.config(font=('Times', 25),
                              width=10,
                              background='black',
                              foreground='white')
        self.Team2Name.config(font=('Times', 25),
                              width=10,
                              background='black',
                              foreground='white')
        self.Team1Punkte.config(font=('Times', 25),
                                background='black',
                                foreground='white')
        self.Team2Punkte.config(font=('Times', 25),
                                background='black',
                                foreground='white')
        self.Team1Name.grid(row=0, column=0, columnspan=2)
        self.Team2Name.grid(row=0, column=2, columnspan=2)
        self.Team1Punkte.grid(row=1, column=0, columnspan=2)
        self.Team2Punkte.grid(row=1, column=2, columnspan=2)

    def makeFelder(self):
        for i in range(len(self.kategorienListe[0:-1])):
            kategorie = self.kategorienListe[i]
            self.kategorienButtons[kategorie] = Button(self.Uebersicht,
                                                       text=kategorie,
                                                       command=lambda kategorie=kategorie: self.ausgewaehlt(kategorie)
                                                       )
            self.kategorienButtons[kategorie].grid(row=i%3, column=int(i/3), padx=10, pady=10)
            self.kategorienButtons[kategorie].config(font=('Times', 25),
                                                     width=9,
                                                     height=2,
                                                     background='lightblue',
                                                     borderwidth=10,
                                                     state=DISABLED)

    def ausgewaehlt(self, kategorie):
        if self.kategorieAktiv:
            self.aktiveKategorie = Label(self.Uebersicht,
                                         text=kategorie,
                                         font=('Times',100),
                                         width=11,
                                         height=3,
                                         background='yellow',
                                         padx=10,
                                         pady=10)
            self.aktiveKategorie.grid(row=0, column=0)
            self.frageAnzeigen(kategorie)
        else:
            self.kategorienButtons[kategorie].config(relief=RAISED)
            self.kategorienButtons[kategorie].config(background='yellow')
            self.kategorieAktiv = True

        #elf.frageAnzeigen(kategorie)
        #fragenZeuch=getFrage() besorgt die Frage anhand der Kategorie

    def frageAnzeigen(self, kategorie):
        self.frage = Toplevel()
        self.frage.geometry(self.geometrieFragen)
        self.frage.attributes('-topmost', True)
        self.frage.title('Frage zu der Kategorie ' + kategorie)
        fragenFile = open(NAMEFRAGENFILE, encoding='utf-8')
        fragenJson = json.load(fragenFile)
        frageText = Label(self.frage,
                          text=fragenJson[kategorie][0]['Frage'],
                          font=('Times', 25),
                          wraplength=900,
                          padx=20,
                          pady=20)
        frageText.pack()
        if self.team1aktiv:
            team = TEAMS['Team 1']
            self.Team1Name.config(background=TEAMS['Team 1']['Farbe'], foreground='black')
            self.Team2Name.config(background='black', foreground='white')

        else:
            team = TEAMS['Team 2']
            self.Team1Name.config(background='black', foreground='white')
            self.Team2Name.config(background=TEAMS['Team 2']['Farbe'], foreground='black')
        self.antwort1 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Richtig'],
                               anchor=W,
                               command=lambda feedback=(True, kategorie, team, 1): self.getFeedback(feedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        self.antwort2 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Falsch1'],
                               anchor=W,
                               command=lambda feedback=(False, kategorie, team, 2): self.getFeedback(feedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        self.antwort3 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Falsch2'],
                               anchor=W,
                               command=lambda feedback=(False, kategorie, team, 3): self.getFeedback(feedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        antworten = [self.antwort1, self.antwort2, self.antwort3]
        random.shuffle(antworten)
        buchstaben = ['C) ', 'B) ', 'A) ']
        for a in antworten:
            ant = a['text']
            a.config(text=(buchstaben.pop() + ant))
            a.pack()

    def getFeedback(self, feedback):
        positiv, kategorie, team, antwort = feedback
        if self.antwortEinloggen:
            if positiv:
                self.kategorienButtons[kategorie].config(background=team['Farbe'], state=DISABLED,
                                                         text=kategorie + '\n' + team['Name'])
                team['Punkte'] += 1
                self.Team1Punkte.config(text=TEAMS['Team 1']['Punkte'])
                self.Team2Punkte.config(text=TEAMS['Team 2']['Punkte'])
            else:
                self.kategorienButtons[kategorie].config(background='grey', state=DISABLED, text=kategorie)
            self.antwort1.config(background='darkgreen')
            self.weiterButton = Button(self.Teams,
                                 text='weiter',
                                 font=('Times', 25),
                                 command=self.weiter)
            self.weiterButton.grid(row=2, column=0, columnspan=4)
        else:
            if antwort == 1:
                self.antwort1.config(background='yellow')
            elif antwort == 2:
                self.antwort2.config(background='yellow')
            elif antwort == 3:
                self.antwort3.config(background='yellow')
            self.antwortEinloggen = True

    def weiter(self):
        self.weiterButton.grid_forget()
        self.team1aktiv = not self.team1aktiv
        self.antwortEinloggen = False
        self.kategorieAktiv = False
        self.aktiveKategorie.destroy()
        self.frage.destroy()
        self.counter += 1
        if self.counter == 12:
            self.master()

    def master(self):
        self.masterFrageButton = Button(self.Teams,
                                        text='Masterfrage',
                                        command=self.readyForMasterFrage,
                                        font=('Times', 25))
        self.masterFrageButton.grid(row=2, column=0, columnspan=4)

    def readyForMasterFrage(self):
        self.masterFrageButton.grid_forget()
        for i in range(len(self.kategorienListe[:-1])):
            kat = self.kategorienListe[i]
            self.kategorienButtons[kat].grid_forget()
        kategorie = self.kategorienListe[-1]
        self.aktiveKategorie = Label(self.Uebersicht,
                                     text='Masterfrage \nder Kategorie\n' + kategorie,
                                     font=('Times', 75),
                                     width=15,
                                     height=4,
                                     background='yellow',
                                     padx=10,
                                     pady=10)
        self.aktiveKategorie.grid(row=0, column=0)

        self.Team1Setzen = Scale(self.Teams, from_=0, to=TEAMS['Team 1']['Punkte'], orient=HORIZONTAL)
        self.Team2Setzen = Scale(self.Teams, from_=0, to=TEAMS['Team 2']['Punkte'], orient=HORIZONTAL)
        self.Team1Setzen.grid(row=2, column=0, columnspan=2)
        self.Team2Setzen.grid(row=2, column=2, columnspan=2)
        self.Setzten = Button(self.Teams, text='Setzen',
                              command=lambda kategorie=kategorie: self.finaleFrage(kategorie))
        self.Setzten.grid(row=3, column=0, columnspan=4)

    def finaleFrage(self, kategorie):
        self.Team1Punkte.grid_forget()
        self.Team2Punkte.grid_forget()
        self.Setzten.grid_forget()
        self.Team1Setzen.grid_forget()
        self.Team2Setzen.grid_forget()
        gesetzt1 = self.Team1Setzen.get()
        gesetzt2 = self.Team2Setzen.get()
        self.Team1SetzenLabel = Label(self.Teams,
                                      text=gesetzt1,
                                      font=('Times', 25),
                                      background='black',
                                      foreground=TEAMS['Team 1']['Farbe'])
        self.Team2SetzenLabel = Label(self.Teams,
                                      text=gesetzt2,
                                      font=('Times', 25),
                                      background='black',
                                      foreground=TEAMS['Team 2']['Farbe'])
        self.Team1Punkte.grid(row=1, column=0)
        self.Team1SetzenLabel.grid(row=1, column=1)
        self.Team2Punkte.grid(row=1, column=2)
        self.Team2SetzenLabel.grid(row=1, column=3)




        self.frage = Toplevel()
        self.frage.geometry('1100x400+100+500')
        self.frage.title('Frage zu der Kategorie ' + kategorie)
        fragenFile = open(NAMEFRAGENFILE, encoding='utf-8')
        fragenJson = json.load(fragenFile)
        frageText = Label(self.frage,
                          text=fragenJson[kategorie][0]['Frage'],
                          font=('Times', 25),
                          wraplength=900,
                          padx=20,
                          pady=20)
        frageText.pack()


        self.antwort1 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Richtig'],
                               anchor=W,
                               command=lambda finalFeedback=(True, 1): self.getWinner(finalFeedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        self.antwort2 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Falsch1'],
                               anchor=W,
                               command=lambda finalFeedback=(False, 2): self.getWinner(finalFeedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        self.antwort3 = Button(self.frage,
                               text=fragenJson[kategorie][0]['Falsch2'],
                               anchor=W,
                               command=lambda finalFeedback=(False, 3): self.getWinner(finalFeedback),
                               width=700,
                               font=('Times', 25),
                               wraplength=900,
                               padx=20,
                               pady=20)
        print(self.antwort3)
        antworten = [self.antwort1, self.antwort2, self.antwort3]
        random.shuffle(antworten)
        buchstaben = ['C) ', 'B) ', 'A) ']

        for a in antworten:
            ant = a['text']
            a.config(text=(buchstaben.pop() + ant))
            a.pack()

    def getWinner(self, finalFeedback):
        richtig, antwortNummer = finalFeedback
        if antwortNummer == 1:
            antwort = self.antwort1['text'][0]
        elif antwortNummer == 2:
            antwort = self.antwort2['text'][0]
        elif antwortNummer == 3:
            antwort = self.antwort3['text'][0]
        else:
            antwort = '?'

        if self.first:
            if richtig:
                TEAMS['Team 1']['Punkte'] += int(self.Team1SetzenLabel['text'])
            else:
                TEAMS['Team 1']['Punkte'] -= int(self.Team1SetzenLabel['text'])
            self.first = False

            self.finalAntwort1 = Label(self.Teams,
                                       text=antwort,
                                       font=('Times', 25),
                                       background='black',
                                       foreground=TEAMS['Team 1']['Farbe'])
            self.finalAntwort1.grid(row=3, column=0, columnspan=2)
        else:
            if richtig:
                TEAMS['Team 2']['Punkte'] += int(self.Team2SetzenLabel['text'])
            else:
                TEAMS['Team 2']['Punkte'] -= int(self.Team2SetzenLabel['text'])
            self.finalAntwort2 = Label(self.Teams,
                                       text=antwort,
                                       font=('Times', 25),
                                       background='black',
                                       foreground=TEAMS['Team 2']['Farbe'])
            self.finalAntwort2.grid(row=3, column=2, columnspan=2)
            self.ueberpruefen = Button(self.Teams,
                                      text='Überprüfen',
                                      font=('Times', 25),
                                      command=self.checkForWinner)#
            self.ueberpruefen.grid(row=4, column=0, columnspan=4)

    def checkForWinner(self):
        self.antwort1.config(background='darkgreen')
        self.Team1Punkte.config(text=TEAMS['Team 1']['Punkte'])
        self.Team2Punkte.config(text=TEAMS['Team 2']['Punkte'])
        self.Team1SetzenLabel.grid_forget()
        self.Team2SetzenLabel.grid_forget()
        self.Team1Punkte.grid(row=1, column=0, columnspan=2)
        self.Team2Punkte.grid(row=1, column=2, columnspan=2)
        self.ueberpruefen.grid_forget()
        winner = 'and the winner is\n'
        if TEAMS['Team 1']['Punkte'] > TEAMS['Team 2']['Punkte']:
            winner += TEAMS['Team 1']['Name']
        elif TEAMS['Team 2']['Punkte'] > TEAMS['Team 1']['Punkte']:
            winner += TEAMS['Team 2']['Name']
        elif TEAMS['Team 2']['Punkte'] > TEAMS['Team 1']['Punkte'] and TEAMS['Team 1']['Punkte'] == 0:
            winner += 'alle haben verloren'
        else:
            winner += 'alle haben gewonnen'
        self.aktiveKategorie.config(text=winner)


if __name__ == '__main__':
    with open(NAMEFRAGENFILE, encoding='utf-8') as fF:
        test = json.load(fF)
    kategorienListe = []
    for key in test:
        kategorienListe.append(key)
    a = Kategorien(kategorienListe)
    a.makeFelder()
    a.Uebersicht.mainloop()

