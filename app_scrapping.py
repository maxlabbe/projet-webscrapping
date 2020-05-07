import tkinter as tk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from selenium import webdriver
from time import sleep


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

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
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()