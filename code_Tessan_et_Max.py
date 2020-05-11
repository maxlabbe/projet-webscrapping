# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:01:04 2020

@author: Tesso
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib import style
from selenium import webdriver
from time import sleep
import data_treatment

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
        label = tk.Label(self, text="Home Page")
        label.pack(pady=10,padx=10)

        # Button that open the S&P 500 graph
        sp500_button = ttk.Button(self, text="S&P 500",
                            command=lambda: controller.show_frame(SP500))
        sp500_button.pack()
        
        btc_button = ttk.Button(self, text="Bitcoin",
                            command=lambda: controller.show_frame(BtcApp))
        btc_button.pack()
 
# Page with the S&P500 graph
class SP500(tk.Frame):
    # Figure wher the graph will be
    f = Figure(figsize=(7,7), dpi=100)
    gs = f.add_gridspec(2, 1)
    f.subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0, hspace = 0.5)
    
    # Subplots of the figure
    real_time_graph = f.add_subplot(gs[0, 0])
    year_graph = f.add_subplot(gs[1, 0])
    
    # List of the values of the S&P500 and the time of each value
    market_values = []
    time_values = []
    
    #List of values for 60 seconds
    market_value_60seconds = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Separate the window in 2 frames
        top_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        
        # Name of the window
        label = tk.Label(top_frame, text="S&P 500")
        label.pack(pady=10,padx=10)
        
        # Button that go to the home page
        home_button = tk.ttk.Button(top_frame, text="Home page", command=lambda: controller.show_frame(StartPage))
        home_button.pack(side=tk.LEFT)
        
        self.start_pause_flag = False
        
        # Button to start and pause the graph 
        start_pause_button = tk.ttk.Button(top_frame, text="Start/Pause", command=lambda: self.start_pause())
        start_pause_button.pack(side=tk.LEFT)
        
        # Create a save button
        save_button = tk.ttk.Button(top_frame, text='save', command=lambda: data_treatment.save_to_csv(self.market_values, self.time_values))
        save_button.pack(side=tk.LEFT)
        
        # Put the graph in the frame
        canvas = FigureCanvasTkAgg(self.f, bottom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Anime the graph
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=1)
        
        #We fill the second graph
        self.year_graph.plot(data_treatment.df_year['Date'], data_treatment.df_year['Adj Close'], color = 'black', label = 'precise values')
        self.year_graph.plot(data_treatment.df_year['moving_average20'], color = 'red', label = '20 d. moving avrg')
        self.year_graph.plot(data_treatment.df_year['moving_average50'], color = 'green', label = '50 d. moving avrg')
        self.year_graph.set_xticks(range(0, len(data_treatment.df_year['Date']), 30))
        self.year_graph.set_title("S&P 500 evolution for one year")
        self.year_graph.legend()
        top_frame.pack(fill = 'x')
        bottom_frame.pack(fill = 'x')
        
    """
    Fuction that will be use in animation.FuncAnimation to animate the graph
    param[in] self instance of SP500: we will use the graph of the instance
    param[in] interval: frame refresh interval
    """    
    def animate(self, interval):
        sleep(1)
        
        # Indice of S&P500 at time t
        market_value = str(data_treatment.driver.find_element_by_xpath("/html/body/div[4]/div/div[3]/div[3]/div[1]/div[2]/div/div[1]/div/table/tbody/tr[5]/td[1]/span[1]").text)
        
        # Data Frame with all the index of the session
        df_session = data_treatment.create_market_dataFrame(market_value, self.market_values, self.time_values)
        
        market_value = market_value.replace(',', '')
        self.market_value_60seconds.append(float(market_value))
        
        # We fill the first graph every 60 seconds
        if len(self.market_value_60seconds) == 60:
            df = data_treatment.create_high_low_df(self.market_value_60seconds)
            colors = {'increase':'red', 'decrease':'green'}
            
            self.real_time_graph.clear()
            self.real_time_graph.bar(df.time_values, df.Diff_High_Low, bottom=df.Low_values, color=df.color)
            self.real_time_graph.set_xticks(range(0,len(self.time_values),3600))
            self.real_time_graph.tick_params('x', rotation = 90)
            self.real_time_graph.set_ylim(min(df.Low_values) - 10, max(df.High_values) + 10)
            self.real_time_graph.set_title("S&P 500 real time evolution")
            for i, j in colors.items(): #Loop over color dictionary
                self.real_time_graph.bar(df.time_values, df.Diff_High_Low, width=0,color=j,label=i)
            self.real_time_graph.legend()
            self.market_value_60seconds.clear()
        
    """
    Function to stop or continue graph display
    param[in] self Instance of SP500: We need to change the start/pause flag 
    """
    def start_pause(self):
        if self.start_pause_flag == True:
            self.ani.event_source.start()
            self.start_pause_flag = False   
        
        else :
            self.ani.event_source.stop()
            self.start_pause_flag = True

class BtcApp(tk.Frame):
    
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bitcoin")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Home page", command=lambda: controller.show_frame(StartPage))
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