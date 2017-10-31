#!/usr/bin/env python
#filename: pypca.py

#import Tkinter as Tk
from Tkinter import *
import Pmw

class App:

	def __init__(self, master):
		
		
		
		frame = Frame(master, width=768, height=576, bg="", colormap="new")
		frame.pack()
		
		
		 # the title
		title_label = Label(text = 'pyMODE-TASK MODE-TASK Plugin -- Bilal Nizami, RUBi, Rhodes University',background = 'navy',foreground = 'white',)
		title_label.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		
		var = StringVar()
		label = Label( frame, textvariable=var, relief=RAISED, anchor='n' )
		var.set("Select analysis")
		label.pack()

		v = StringVar()
		v.set("L")
		
		self.rb1=Radiobutton(frame, text="PCA", variable=v, value=1)
		self.rb1.pack(anchor=W)
		
		self.rb2=Radiobutton(frame, text="NMA", variable=v, value=2)
		self.rb2.pack(anchor=W)
	
		self.button = Button(frame, text="EXIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)
	
		self.hi_there = Button(frame, text="About", command=self.about)
		self.hi_there.pack(side=RIGHT)
	
	def about(self):
		print "pyMODE-TASK!\n pymol plugin of MODE-TASK\n MODE-TASK: a software tool to perform PCA and NMA of protein structure and MD trajectories"



root = Tk()
app = App(root)
root.mainloop()
root.mainloop()
root.destroy()
