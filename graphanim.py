# -*- coding: utf-8 -*-
"""
Created on Mon May  4 08:51:39 2020

@author: Max
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import time
import datetime
from selenium import webdriver

import tkinter as tk

style.use('ggplot')
    
# On fait hérité la classe principale de l'app de tk.TK
class Marketapp(tk.Tk):

    # Méthode d'initialisation
    def __init__(self, *args, **kwargs):
        
        # Initialisation de l'objet Tk(widget)
        tk.Tk.__init__(self, *args, **kwargs)

        # On donne un titre au widget
        tk.Tk.wm_title(self, "Market client")
        
        # On vient créer un frame qui va contenir toutes les frame que l'on va utiliser
        container = tk.Frame(self)
        
        # On le positionne et on lui dit de s'étendre au maximum
        container.pack(side="top", fill="both", expand = True)
        
        # On donne la taille (min) au colonne et au lignes ainsi que leur ordre de priorité (ici le meme)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionnaire qui va contenir toutes les frames de l'app sur lequel on va jouer pour les affichage de pages
        self.frames = {}

        # On remplis le dictionnaire
        for F in (StartPage, AnimGraphPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10,padx=10)

        # Création du bouton pour ouvrir la page graphe
        # Utilisation de ttk d'un point de vue esthtique
        button3 = tk.ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(AnimGraphPage))
        button3.pack()
        
class AnimGraphPage(tk.Frame):
    # Création de la figure sur laquelle on va mettre notre graphe
    f = Figure(figsize=(5,4), dpi=100)
    
    #Création du sous graph
    graph = f.add_subplot(111)

    driver = webdriver.Firefox()
    driver.get("https://www.cnbc.com/quotes/?symbol=.SPX")

    market_values = []
    time_values = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Nom de la page et taille du titre
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10,padx=10)

        # Création du bouton de retour au menu
        # Utilisation de ttk d'un point de vue esthtique
        button1 = tk.ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ani = animation.FuncAnimation(self.f, self.animate, interval=1000)
        ani._start()
        
    def animate(self, interval):
        # Récupération de l'indice
        price_element = str(self.driver.find_element_by_xpath("/html/body/div[4]/div/div[3]/div[3]/div[1]/div[2]/div/div[1]/div/table/tbody/tr[5]/td[1]/span[1]").text)
        price_element = price_element.replace(',', '')
    
        # Stockage dans la liste des valeurs
        self.market_values.append(float(price_element))
        print(price_element)
    
        # Récupération de la date et de l'heure
        day = str(datetime.date.today())
        hour = str(time.localtime().tm_hour)
        minute = str(time.localtime().tm_min)
        second = str(time.localtime().tm_sec)
        current_time = str(day + " " + hour + ':' + minute + ':' + second)
    
        # Stockage dans la liste du temps
        self.time_values.append(current_time)
    
        #Création de la data frame
        df = pd.DataFrame({'market_values': self.market_values, 'time_values': self.time_values})
    
        self.graph.clear()
        self.graph.plot(df.time_values, df.market_values)
        self.graph.set_xticks(range(0,len(self.time_values),3600))
        self.graph.tick_params('x', rotation = 90)


app = Marketapp()
app.mainloop()