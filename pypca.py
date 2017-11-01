#!/usr/bin/env python
#filename: pypca.py

#import Tkinter as Tk
from Tkinter import *
import Pmw

class App:

	def __init__(self, master):
		
		
		adplugin_font = ("Courier", 12)
		self.frame = Frame(master, width=768, height=576, bg="red", colormap="new")
		self.frame.pack()
		
		
		# the title
		self.title_label = Label(self.frame, text = 'pyMODE-TASK: A MODE-TASK Plugin -- Bilal Nizami, RUBi, Rhodes University',background = 'navy',foreground = 'white',)
		self.title_label.pack(expand = 0, fill = 'both', padx = 1, pady = 1)
		
		# the basic notebook

		self.notebook = Pmw.NoteBook(master)
		self.notebook.pack(fill='both',expand=1,padx=13,pady=13)



        # build pages
		self.pca_page = self.notebook.add('PCA')
		self.nma_page = self.notebook.add('NMA')
		self.about_page = self.notebook.add('About')
		self.citation_page = self.notebook.add('Citation')
		self.help_page = self.notebook.add('Help')
		
		#---------------------------------------------------------------
        # PCA PAGE
		
		# about section
		
		about_pca = """MODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University. 
To perform the Priciple component analysis (PCA) on a protein MD trajectory."""
		self.configuration_top_group = Pmw.Group(self.pca_page,tag_text='About')
		self.configuration_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name=adplugin_font[0],size=int(adplugin_font[1]))
		self.text_field = Pmw.ScrolledText(self.configuration_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=4,
                             text_wrap='word',
                             text_background='#000000',
                             text_foreground='green',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_pca)
		
		# input files
		
		self.trj_file_io = Pmw.Group(self.pca_page, tag_text='MODE-TASK input')
		self.trj_file_io.pack(side = TOP,expand=1, fill='x')	
		
		# Read Trajectory 
		self.trj_location = Pmw.EntryField(self.trj_file_io.interior(),
                                                labelpos = 'w',
                                                label_text = 'Trajectory File:')
		# Read Topology 
		self.top_location = Pmw.EntryField(self.trj_file_io.interior(),
                                                labelpos = 'w',
                                                label_text = 'Topology File:')
		# RMSD Reference Structure
		
		self.ref_file = Pmw.EntryField(self.trj_file_io.interior(),
                                                labelpos = 'w',
                                                label_text = 'Ref Structure/Frame:',
												value='First')
		for x in  [self.trj_location,
					self.top_location,
					self.ref_file,
					]:
			x.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
			
		# PCA options
		# PCA Methods
		self.pca_page_main_group = Pmw.Group(self.pca_page, tag_text='PCA Options')
		self.pca_page_main_group.pack(fill = 'both', expand = 0, padx=2, pady=2)
		
		self.pca_methods_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'PCA Method:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.pca_methods_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.pca_methods_buttons.add('SVD', command = self.ok)
		self.pca_methods_buttons.add('EVD', command = self.ok)
		self.pca_methods_buttons.add('kPCA', command = self.ok)
		self.pca_methods_buttons.add('iPCA', command = self.ok)
		
		self.pca_methods_buttons.invoke('SVD')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.atm_grp_buttons.add('All', command = self.ok)
		self.atm_grp_buttons.add('CA', command = self.ok)
		self.atm_grp_buttons.add('Backbone', command = self.ok)
		self.atm_grp_buttons.add('Protein', command = self.ok)
		self.atm_grp_buttons.invoke('CA')
		

		# Number of PCA component
		self.pca_comp = Pmw.EntryField(self.pca_page_main_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'PCA component:',
												value='All')
		self.pca_comp.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Kernel Type
		self.kernel_type = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Kernel Type (kPCA):',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.kernel_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.kernel_type.add('Linear', command = self.ok)
		self.kernel_type.add('Poly', command = self.ok)
		self.kernel_type.add('RBF', command = self.ok)
		self.kernel_type.add('Sigmoid', command = self.ok)
		self.kernel_type.add('Precomputed', command = self.ok)
		self.kernel_type.add('Cosine', command = self.ok)
		self.kernel_type.invoke('Linear')
		
		# SVD Solver
		self.svd_solver_type = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'SVD solver:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.svd_solver_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.svd_solver_type.add('Auto', command = self.ok)
		self.svd_solver_type.add('Full', command = self.ok)
		self.svd_solver_type.add('Arpack', command = self.ok)
		self.svd_solver_type.add('Randomized', command = self.ok)
		
		self.svd_solver_type.invoke('Auto')
		
		# Run button
		
		self.run_pca = Pmw.ButtonBox(self.pca_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.run_pca.add('Run PCA',command = self.load_gpf_file)
		self.run_pca.pack(side=BOTTOM,expand = 1, padx = 10, pady = 2)
		
	def button_pressed(self, result):
		if hasattr(result,'keycode'):
			if result.keycode == 36:
				if self.notebook.getcurselection()=='Grid Settings':
					self.show_box()
				elif self.notebook.getcurselection()=='View Poses':
					self.load_ligand_file()
		elif result == 'Exit' or result == None:
			self.dialog.withdraw()
	def ok(self):
		print 'You clicked on OK'
		
	def load_gpf_file(self):
		global global_status
		filename = self.gpf_file_location.get()
		fp = self.fileopen(filename,'r')
		if not fp:
			return
		lst = fp.readlines()
		new = []
		for line in lst:
			if line.strip():
				new.append(line.strip())
		lst = new
		for line in lst:
			entr = line.split()
			if entr[0] == 'npts':
				n_points_X = int(entr[1])
				n_points_Y = int(entr[2])
				n_points_Z = int(entr[3])
				self.n_points_X.set(n_points_X)
				self.n_points_Y.set(n_points_Y)
				self.n_points_Z.set(n_points_Z)
			elif entr[0] == 'spacing':
				spacing = float(entr[1])
				self.grid_spacing.set(spacing)
			elif entr[0] == 'gridcenter':
				if entr[1]!='auto':
					grid_X = float(entr[1])
					grid_Y = float(entr[2])
					grid_Z = float(entr[3])
					self.grid_center[0].set(grid_X)
					self.grid_center[1].set(grid_Y)
					self.grid_center[2].set(grid_Z)
		global_status.set( 'Reading box info from %s' % filename)
		self.grid_center_selection_mode.set(GRID_CENTER_FROM_COORDINATES)
		self.calculate_box()
		
	def save_gpf_file(self):
		global global_status
		filename = self.gpf_file_location.get()
		fp = self.fileopen(filename,'w')
		if not fp:
				return
		n_points_X = self.n_points_X.get()
		n_points_Y = self.n_points_Y.get()
		n_points_Z = self.n_points_Z.get()
		spacing = self.grid_spacing.get()
		center_X = self.grid_center[0].get()
		center_Y = self.grid_center[1].get()
		center_Z = self.grid_center[2].get()
		print >>fp, 'npts %d %d %d' % (n_points_X, n_points_Y, n_points_Z)
		print >>fp, 'spacing %5.3f' % spacing
		print >>fp, 'gridcenter  %8.3f %8.3f %8.3f' % (center_X, center_Y, center_Z)
		fp.close()
		global_status.set( 'Wrote box info to %s' % filename)
		
	def about(self):
		print "pyMODE-TASK!\n pymol plugin of MODE-TASK\n MODE-TASK: a software tool to perform PCA and NMA of protein structure and MD trajectories"



root = Tk()
app = App(root)
root.title("pyMODE-TASK")
root.geometry("1000x700")
root.mainloop()
root.mainloop()
root.destroy()
