
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
#from matplotlib import style DOINSTALOWAC

import tkinter as tk
import tkinter.scrolledtext as ScrolledText
import datetime

import random
import database

import os

#CONFIGURE
os.system('python3 configure.py')
#STYLES
LARGE_FONT = ("Arial", 10)
#DB CONNECTION
db = database.MyDB()
db.connect()
#PLOTING
f = Figure(figsize=(4,4), dpi=100)
a = f.add_subplot(111)
def animate(i):
	speed = []
	res = db.query('select speed from airplane')
	for row in res.fetchall():
		speed.append(float(row[0]))
	timeStep = [i for i in range(1,len(speed)+1)]
	a.clear()
	a.plot(timeStep, speed)
#LOGGING
startFlag = False
def startLogging(flag):
	global startFlag;
	startFlag = flag


#MainApplication
class myApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container = tk.Frame(self, width=100, height=100)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, DrawPage, LogPage) :

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

#LOGGING PAGE
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.button4 = tk.Button(self, text="Save", command=lambda:self.saveAirplaneParameter())
		self.button4.pack(side="top", fill="both", expand = True)

		self.button3 = tk.Button(self, text="Start", command=lambda:startLogging(True))
		self.button3.pack(side="top", fill="both", expand = True)
		self.button3.configure(state="disabled")

		self.button = tk.Button(self, text="Draw", command=lambda:controller.show_frame(DrawPage))
		self.button.pack(side="top", fill="both", expand = True)

		self.button2 = tk.Button(self, text="Quit", command=quit)
		self.button2.pack(side="top", fill="both", expand = True)
		
		self.button5 = tk.Button(self, text="Check", command=lambda:controller.show_frame(LogPage))
		self.button5.pack(side="top", fill="both", expand = True)
		self.button5.configure(state="disabled")

		self.txtInfo = ScrolledText.ScrolledText(self, width=100, height = 1, state="disabled")
		self.txtInfo.pack()
		self.txtInfo.configure(state="normal")
		self.txtInfo.insert(tk.INSERT, "(Datetime, Id, Name, StartLocation, EndLocation, Fuel, High, Speed, Distance)")
		self.txtInfo.configure(state="disabled")

		self.txt = ScrolledText.ScrolledText(self, width=100, height = 8, state="disabled")
		self.txt.pack()

		l1 = tk.Label(self,text="Name")
		l1.pack()
		self.e1 = tk.Entry(self, bd=1)
		self.e1.pack()

		l2 = tk.Label(self,text="StartLocation")
		l2.pack()
		self.e2 = tk.Entry(self, bd=1)
		self.e2.pack()

		l3 = tk.Label(self,text="EndLocation")
		l3.pack()
		self.e3 = tk.Entry(self, bd=1)
		self.e3.pack()

		l4 = tk.Label(self,text="Fuel")
		l4.pack()
		self.e4 = tk.Entry(self, bd=1)
		self.e4.pack()

		l5 = tk.Label(self,text="High")
		l5.pack()
		self.e5 = tk.Entry(self, bd=1)
		self.e5.pack()

		l6 = tk.Label(self,text="Speed")
		l6.pack()
		self.e6 = tk.Entry(self, bd=1)
		self.e6.pack()

		l7 = tk.Label(self,text="Distance")
		l7.pack()
		self.e7 = tk.Entry(self, bd=1)
		self.e7.pack()

		self.checkAir()
		self.updateAir()

	def checkAir(self):
		if startFlag is True:
			res = db.query('select * from airplane where id=(select max(id) from airplane)')
			for row in res:
				self.txt.configure(state="normal")
				self.txt.insert(tk.INSERT, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(row) + "\n")
				self.txt.see(tk.END)
				self.txt.configure(state="disabled")
				self.l = row
		self.after(1000, self.checkAir)
	def updateAir(self):
		if startFlag is True:
			fuel, high, speed, distance = self.l[-4:]
			if distance <= 0.0:
				startLogging(False)
			else:
				speed = round(random.uniform(50,60), 2)
				distance -= speed
				fuel -= 0.5*speed
				fuel = round(fuel,2)
				high = round(random.uniform(1000,2000), 2)
				distance = round(distance,2)
				if distance <= 0.:
					distance = 0
					self.txt.configure(state="normal")
					self.txt.insert(tk.INSERT, "\nKoniec lotu!")
					self.txt.see(tk.END)
					self.txt.configure(state="disabled")
					startLogging(False)
					self.button5.configure(state="normal")
				query = 'INSERT INTO AIRPLANE VALUES(null,?,?,?,?,?,?,?)'
				db.query(query, (self.e1.get(), self.e2.get(), self.e3.get(), fuel, high, speed, distance))
		self.after(1000, self.updateAir)
	def saveAirplaneParameter(self):
		try:
			float(self.e4.get())
			float(self.e5.get())
			float(self.e6.get())
			float(self.e7.get())
			if self.e1.get() is '' or self.e2.get() is '' or self.e3.get() is '':
				raise Exception()
		except Exception:
			print('Blad')
			return
		query = 'INSERT INTO AIRPLANE VALUES(null,?,?,?,?,?,?,?)'
		db.query(query, (self.e1.get(), self.e2.get(), self.e3.get(), float(self.e4.get()), float(self.e5.get()), float(self.e6.get()), float(self.e7.get())))
		self.button3.configure(state="normal")
		return


class DrawPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Graph Page!!!", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
		button.pack()

		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

		toolbar = NavigationToolbar2TkAgg(canvas,self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

class LogPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Log Page!!!", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
		button.pack()

		button2 = tk.Button(self, text="Get data", command=lambda: self.getLog())
		button2.pack()

		self.txtInfo = ScrolledText.ScrolledText(self, width=100, height = 1, state="disabled")
		self.txtInfo.pack()
		self.txtInfo.configure(state="normal")
		self.txtInfo.insert(tk.INSERT, "(Datetime, Id, Name, StartLocation, EndLocation, Fuel, High, Speed, Distance)")
		self.txtInfo.configure(state="disabled")

		self.txt = ScrolledText.ScrolledText(self, width=100, height = 8, state="disabled")
		self.txt.pack()


	def getLog(self):
		res = db.query('select * from airplane')
		for row in res:
			self.txt.configure(state="normal")
			self.txt.insert(tk.INSERT, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(row) + "\n")
			self.txt.see(tk.END)
			self.txt.configure(state="disabled")


if __name__ == "__main__":
	app = myApp()
	ani = animation.FuncAnimation(f, animate, interval=1000)
	app.geometry('{}x{}'.format(800, 600))
	app.resizable(width=tk.FALSE, height=tk.FALSE)
	app.title("FLY RECORDER")
	app.mainloop()
