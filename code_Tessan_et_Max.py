# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:01:04 2020

@author: Tesso
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib import style
from selenium import webdriver
from time import sleep
import scrapping_celenium

matplotlib.use("TkAgg")
style.use('ggplot')
    
# Principale class of the app that will manage all the frames
class Marketapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        # Creation of widget
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Market client")
        
        # frame that will contain all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Creation of a dictionnay that will contain all the frames
        self.frames = {}

        # We fill out the dictionary
        for F in (StartPage, SP500, BtcApp):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

# Function that will put a frame in front of the others
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# Home page 
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10,padx=10)

        # Button that open the S&P 500 graph
        sp500_button = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(SP500))
        sp500_button.pack()
        
        btc_button = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(BtcApp))
        btc_button.pack()
 
# Page with the S&P500 graph
class SP500(tk.Frame):
    # Figure wher the graph will be
    f = Figure(figsize=(5,4), dpi=100)
    
    # Subplot of the figure
    graph = f.add_subplot(111)
    
    # List of the values of the S&P500 and the time of each value
    market_values = []
    time_values = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Name of the frame
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10,padx=10)
        
        # Button that go to the home page
        home_button = tk.ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        home_button.pack()

        
        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=1000)
        
        self.start_pause_flag = False
        
        start_pause_button = tk.ttk.Button(self, text="Start", command=lambda: self.start_pause())
        start_pause_button.pack()
        
        save_button = tk.ttk.Button(self, text='save', command=lambda: scrapping_celenium.save_to_csv(self.market_values, self.time_values))
        save_button.pack()
    """
    Fuction that will be use in animation.FuncAnimation to animate the graph
    param[in] self instance of SP500: we will use the graph of the instance
    param[in] interval: frame refresh interval
    """    
    def animate(self, interval):
        
        # Index of S&P500 at time t
        market_value = str(scrapping_celenium.driver.find_element_by_xpath("/html/body/div[4]/div/div[3]/div[3]/div[1]/div[2]/div/div[1]/div/table/tbody/tr[5]/td[1]/span[1]").text)
        
        # Data Frame with all the index of the session
        df = scrapping_celenium.create_market_dataFrame(market_value, self.market_values, self.time_values)
        
        # We fill the graph
        self.graph.clear()
        self.graph.plot(df.time_values, df.market_values)
        self.graph.set_xticks(range(0,len(self.time_values),3600))
        self.graph.tick_params('x', rotation = 90)
        
    """
    Function to stop or continue graph display
    param[in] self Instance of SP500: We need to change the start/pause flag 
    """
    def start_pause(self):
        print(self.start_pause_flag)
        if self.start_pause_flag == True:
            self.ani.event_source.start()
            self.start_pause_flag = False   
        
        else :
            self.ani.event_source.stop()
            self.start_pause_flag = True
        print(self.start_pause_flag)

class BtcApp(tk.Frame):
    
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        self.running = False
        self.ani = None

        btns = tk.Frame(self)
        btns.pack()
        
        lbl = tk.Label(btns, text="Number of times to run")
        lbl.pack(side=tk.LEFT)

        self.points_ent = tk.Entry(btns, width=5)
        self.points_ent.insert(0, '50')
        self.points_ent.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="update interval (ms)")
        lbl.pack(side=tk.LEFT)

        self.interval = tk.Entry(btns, width=5)
        self.interval.insert(0, '2000')
        self.interval.pack(side=tk.LEFT)
        
        self.driver = webdriver.Firefox()
        self.driver.get("https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-USD")
        sleep(4)
        self.last_values =[]
        
        self.btn = tk.Button(btns, text='Start', command=self.on_click)
        self.btn.pack(side=tk.LEFT)

        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.line, = self.ax1.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.ax1.set_ylim(8700,9000)
        self.ax1.set_xlim(0,100)

     def on_click(self):
        '''the button is a start, pause and unpause button all in one
        this method sorts out which of those actions to take'''
        if self.ani is None:
            # animation is not running; start it
            return self.start()

        if self.running:
            # animation is running; pause it
            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            # animation is paused; unpause it
            self.ani.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

     def start(self):
        self.points = int(self.points_ent.get()) + 1
        self.ani = animation.FuncAnimation(
                                            self.fig,
                                            self.update_graph,
                                            frames=self.points,
                                            interval=int(self.interval.get()),
                                            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.ani._start()
        print('started animation')

     def update_graph(self, i):
        price_element = self.driver.find_element_by_css_selector('a[title="Kraken BTC/USD"]').find_element_by_class_name("price")
        
        if len(self.last_values) >=100 :
            del self.last_values[0]
            self.last_values.append(float(price_element.text))
    
        else:
            self.last_values.append(float(price_element.text))
            
        self.ax1.set_ylim(min(self.last_values)-10, max(self.last_values)+10)
        self.ax1.set_xlim(0, len(self.last_values) + 5 )
        
        self.line.set_data([range(len(self.last_values))],self.last_values) # update graph
        sleep(5)

        if i >= self.points - 1:
            # code to limit the number of run times; could be left out
            self.btn.config(text='Start')
            self.running = False
            self.ani = None
        return self.line,
       
def main():
    app = Marketapp()
    app.mainloop()