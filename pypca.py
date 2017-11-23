#!/usr/bin/env python
#filename: pypca.py
import matplotlib
matplotlib.use('Agg')
from Tkinter import *
import subprocess
from ttk import Separator, Style
import ttk
import Pmw
import tkMessageBox, tkFileDialog
import os
import webbrowser


class App:
	'Main class of pyMODE-TASK.'
	def __init__(self, master):
		
		
		adplugin_font = ("Courier", 14)
		self.frame = Frame(master, width=4, height=4, bg="red3", colormap="new")
		self.frame.pack()
		
		#================================================
		#
		# Menu bar
		#===============================================
		# Create about dialog.
		self.dialog1 = Pmw.MessageDialog(master,
			title = 'pyMODE-TASK',
			message_text = 'A pymol plugin for MODE-TASK\n\n'+
				'Version 1.0\n\n\n'+
				'MODE-TASK is a open source collection of tools to perform the\n'+
				'Priciple component analysis (PCA), MDS and t-SNE on a protein MD trajectory,\n' +
				'and Normal mode analyses (NMA) on protein 3D structure.\n'+
				'pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.\n',
			buttonboxpos = 's',
			buttons = ('OK', 'Close'),
			defaultbutton = 'Close')
		self.dialog1.iconname('pyMODE-TASK')
		widget = self.dialog1.component('hull')
		Pmw.Color.changecolor(widget, background = 'brown4', foreground='white')
		self.dialog1.withdraw()
		
		# Create the Balloon.
		self.balloon = Pmw.Balloon(master)

		# Create and pack the MenuBar.
		self.menuBar = Pmw.MenuBar(master,
				hotkeys=0,
				hull_relief = 'raised',
				hull_borderwidth = 2,
				balloon = self.balloon)
		self.menuBar.pack(fill = 'x')
		
		# Add File menu bar.
		self.menuBar.addmenu('File', 'Close this window or exit')
		self.menuBar.addmenuitem('File', 'command', 'About the pyMODE-TASK',
				label = 'About',
				command=self.dialog1.activate
				)
		self.menuBar.addmenuitem('File', 'separator')
		self.menuBar.addmenuitem('File', 'command', 'Exit the application',
				label = 'Exit',
				command=self.frame.quit)
	
		# Add Help menu bar.
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/index.html")
		self.menuBar.addmenu('Help', 'Help page')
		self.menuBar.addmenuitem('Help', 'command', label='Help Page',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/theory.html")		
		self.menuBar.addmenuitem('Help', 'separator')
		self.menuBar.addmenuitem('Help', 'command', label='PCA Theory',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/theory.html")		
		self.menuBar.addmenuitem('Help', 'command', label='NMA Theory', 
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/pca_tut.html")			
		self.menuBar.addmenuitem('Help', 'separator')
		self.menuBar.addmenuitem('Help', 'command', label='PCA Tutorial',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/nma_tut.html")		
		self.menuBar.addmenuitem('Help', 'command', label='NMA Tutorial',
			command=page.openpage)
		
		
		# the title
	
		self.title_label = Label(self.frame, text = 'pyMODE-TASK: A MODE-TASK Plugin for pymol -- Bilal Nizami, RUBi, Rhodes University',
				background = 'brown4',
				foreground = 'white', 
				height=1, 
				width=880,
				font=('Arial', 11))
		self.title_label.pack(expand = 0, fill = 'both', padx = 1, pady = 1)
		
		# the notebook layout

		self.notebook = Pmw.NoteBook(master)
		Pmw.Color.changecolor(master, background='gray70', foreground='black')
		self.notebook.recolorborders()
		self.notebook.pack(fill='both',expand=1,padx=13,pady=13)



        # build pages
		self.pca_page = self.notebook.add('PCA')
		self.ipca_page = self.notebook.add('Internal PCA')
		self.mds_page = self.notebook.add('MDS/t-SNE')
		self.nma_page = self.notebook.add('NMA')
		self.about_page = self.notebook.add('About')
		self.citation_page = self.notebook.add('Citation')
		self.help_page = self.notebook.add('Help and Credit')
		
		#---------------------------------------------------------------
        # 							PCA PAGE
		#---------------------------------------------------------------
		
		# about section
		
		about_pca = """MODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University. 

Perform the Priciple component analysis (PCA) on a protein MD trajectory."""		
		self.pca_top_group = Pmw.Group(self.pca_page,tag_text='About')
		self.pca_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Helvetica',size=14)
		self.text_field = Pmw.ScrolledText(self.pca_top_group.interior(),
			borderframe=5,
			vscrollmode='dynamic',
			hscrollmode='dynamic',
			labelpos='n',
			text_width=150, text_height=4,
			text_wrap='word',
			text_background='skyblue4',
			text_foreground='white',
			text_font = myfont)
			
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_pca)
		self.text_field.configure(text_state=DISABLED)
		
		# input files
		
		self.pca_trj_file_io = Pmw.Group(self.pca_page, tag_text='MODE-TASK Input/Output')
		self.pca_trj_file_io.pack(side = TOP,expand=1, fill='both', padx = 4, pady = 4)
		
		
		# Read Trajectory 
		self.pca_trj_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.pca_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File:',
												)
		# Read Topology 						
		self.pca_top_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
                                                label_text = 'Topology File:')
		# RMSD Reference Structure
		
		self.pca_ref_file = Pmw.EntryField(self.pca_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ref_filename,mode='r',filter=[("PDB",".pdb"), ("All","*.*")]),                                                
                                                label_text = 'Ref Structure/Frame:')
		# output directory
		
		self.pca_out_dir_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.pca_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		entries=(self.pca_trj_location,
					self.pca_top_location,
					self.pca_ref_file,
					self.pca_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
			
		Pmw.alignlabels(entries)
		
		#--------------------------------------------
		# PCA options
		#--------------------------------------------
		
		# PCA Methods
		
		self.pca_page_main_group = Pmw.Group(self.pca_page, tag_text='PCA Options')
		self.pca_page_main_group.pack(fill = 'both', expand = 1, padx=4, pady=4)
		
		self.pca_methods_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'PCA Method:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_pc_method_selection)
		self.pca_methods_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.pca_methods_buttons.add('svd', command = self.ok)
		self.pca_methods_buttons.add('evd', command = self.ok)
		self.pca_methods_buttons.add('kpca', command = self.ok)
		self.pca_methods_buttons.add('ipca', command = self.ok)
		
		self.pca_methods_buttons.invoke('svd')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
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
												value='All',
												command = self.get_pc_selection)
		self.pca_comp.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Kernel Type
		self.kernel_type = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Kernel Type (kPCA):',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_kt_selection)
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
				frame_relief = 'groove',
				command = self.get_st_selection
				)
		self.svd_solver_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.svd_solver_type.add('Auto', command = self.ok)
		self.svd_solver_type.add('Full', command = self.ok)
		self.svd_solver_type.add('Arpack', command = self.ok)
		self.svd_solver_type.add('Randomized', command = self.ok)
		
		self.svd_solver_type.invoke('Auto')
		pca_options_buttons=(self.pca_methods_buttons, self.atm_grp_buttons, self.pca_comp, self.kernel_type, self.svd_solver_type)
		Pmw.alignlabels(pca_options_buttons)
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.pca_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.run_pca_button.add('Run PCA',fg='green4', command = self.run_pca)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.pca_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		##============================================================
		#
		#	internal PCA page
		#===========================================================
		
		# about section
		
		about_ipca = """Internal PCA allows user to perform the PCA on the internal cordinates of a protein MD trajectory."""
		self.ipca_top_group = Pmw.Group(self.ipca_page,tag_text='About')
		self.ipca_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Helvetica',size=14)
		self.text_field = Pmw.ScrolledText(self.ipca_top_group.interior(),
			borderframe=5,
			vscrollmode='dynamic',
			hscrollmode='dynamic',
			labelpos='n',
			text_width=150, text_height=4,
			text_wrap='word',
			text_background='skyblue4',
			text_foreground='white',
			text_font = myfont)
			
		self.text_field.pack(expand = 1, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_ipca)
		self.text_field.configure(text_state=DISABLED)
		
		# input files
		
		self.icpca_trj_file_io = Pmw.Group(self.ipca_page, tag_text='MODE-TASK Input/Output')
		self.icpca_trj_file_io.pack(side = TOP,expand=1, fill='both')
		
		
		# Read Trajectory 
		self.ipca_trj_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.ipca_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File:',
												)
		# Read Topology 						
		self.ipca_top_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.ipca_set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
                                                label_text = 'Topology File:')
		# output directory
		
		self.ipca_out_dir_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.ipca_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		entries=(self.ipca_trj_location,
					self.ipca_top_location,
					self.ipca_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
			
		Pmw.alignlabels(entries)	
		
		# internal PCA options
		#------------------------------------------
		
	
		self.ipca_page_main_group = Pmw.Group(self.ipca_page, tag_text='Internal PCA Options')
		self.ipca_page_main_group.pack(fill = 'both', expand = 1, padx=2, pady=2)
		
		## cordinate type
		self.ct_buttons = Pmw.RadioSelect(self.ipca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate type:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.ct_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.ct_buttons.add('distance', command = self.ok)
		self.ct_buttons.add('angle', command = self.ok)
		self.ct_buttons.add('phi', command = self.ok)
		self.ct_buttons.add('psi', command = self.ok)
		
		self.ct_buttons.invoke('distance')
		
		# Atom group 
		self.ipca_atm_grp_buttons = Pmw.RadioSelect(self.ipca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
				#command = self.get_ipca_ag_selection)
		self.ipca_atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.ipca_atm_grp_buttons.add('All', command = self.ok)
		self.ipca_atm_grp_buttons.add('CA', command = self.ok)
		self.ipca_atm_grp_buttons.add('Backbone', command = self.ok)
		self.ipca_atm_grp_buttons.add('Protein', command = self.ok)
		self.ipca_atm_grp_buttons.invoke('CA')
		

		# Number of PCA component
		self.pca_comp = Pmw.EntryField(self.ipca_page_main_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'PCA component:',
												value='All',
												command = self.get_pc_selection)
		self.pca_comp.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		
		pca_options_buttons=(self.ct_buttons, 
			self.ipca_atm_grp_buttons,
			self.pca_comp)
		Pmw.alignlabels(pca_options_buttons)
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.ipca_page_main_group.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_pca_button.add('Run Internal PCA',fg='blue', command = self.run_ipca)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.ipca_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		## status bar
		#pca_output='test'
		#self.pca_output_group = Pmw.Group(self.ipca_page, tag_text='Results')
		#self.pca_output_group.pack(fill = 'both', expand = 0, padx=2, pady=2)
		#self.status_feild = Pmw.ScrolledText(self.pca_output_group.interior(),
        #                     borderframe=5,
        #                     vscrollmode='dynamic',
        #                     hscrollmode='dynamic',
        #                     labelpos='n',
        #                     text_width=150, text_height=4,
        #                     text_wrap='word',
        #                     text_background='#000000',
        #                     text_foreground='white',
        #                     text_font = myfont
        #                     )
		#self.status_feild.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		#self.status_feild.insert('end',pca_output)
		#self.text_field.configure(text_state=DISABLED)
		#sys.stdout = StdoutRedirector(self.status_feild)
		
		
		##============================================================
		# MDS/ t-SNE page
		#
		#==============================================================
		
		about_mds = """Perform the Multi Dimentional Scaling (PCA) and t-SNE on a protein MD trajectory.
		
MDS and t-SNE are dimentionality reduction techniques."""		
		self.mds_top_group = Pmw.Group(self.mds_page,tag_text='About')
		self.mds_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)
        
		myfont = Pmw.logicalfont(name='Helvetica',size=14)
		self.text_field = Pmw.ScrolledText(self.mds_top_group.interior(),
			borderframe=5,
			vscrollmode='dynamic',
			hscrollmode='dynamic',
			labelpos='n',
			text_width=150, text_height=3,
			text_wrap='word',
			text_background='skyblue4',
			text_foreground='white',
			text_font = myfont)
			
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 1)
		self.text_field.insert('end',about_mds)
		self.text_field.configure(text_state=DISABLED)
		
		# input files
		
		self.mds_trj_file_io = Pmw.Group(self.mds_page, tag_text='MDS, t-SNE Input/Output')
		self.mds_trj_file_io.pack(side = TOP,expand=1, fill='both', padx = 4, pady = 4)
		
		
		# Read Trajectory 
		self.mds_trj_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.mds_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File:',
												)
		# Read Topology 						
		self.mds_top_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.mds_set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
                                                label_text = 'Topology File:')
	
		# output directory
		
		self.mds_out_dir_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.mds_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		entries=(self.mds_trj_location,
					self.mds_top_location,
					self.mds_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
			
		Pmw.alignlabels(entries)	
		
		# MDS options
		#-------------------------------------------------
		
		# MDS Type
		self.radioframe = Frame(self.mds_page)
		radiogroups = []
		
		self.mds_page_main_group = Pmw.Group(self.radioframe, tag_text='MDS Options')
		self.mds_page_main_group.pack(side=LEFT, fill = 'both', expand = 1, padx=4, pady=4)
		
		radiogroups.append(self.mds_page_main_group)
		self.mds_type_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'MDS Method:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_type_selection)
		self.mds_type_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.mds_type_buttons.add('metric', command = self.ok, text='metric')
		self.mds_type_buttons.add('nm', command = self.ok, text ='nonmetric')
	
		
		self.mds_type_buttons.invoke('metric')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.atm_grp_buttons.add('All', command = self.ok)
		self.atm_grp_buttons.add('CA', command = self.ok)
		self.atm_grp_buttons.add('Backbone', command = self.ok)
		self.atm_grp_buttons.add('Protein', command = self.ok)
		self.atm_grp_buttons.invoke('CA')
		
		# Dissimilarity Type
		self.mds_dissimilarity_type = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Dissimilarity type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_dissimilarity_type)
		self.mds_dissimilarity_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.mds_dissimilarity_type.add('euc', command = self.ok, text='Euclidean distance')
		self.mds_dissimilarity_type.add('rmsd', command = self.ok, text='RMSD')
		self.mds_dissimilarity_type.invoke('rmsd')
		
		# Cordinate Type
		self.mds_cord_type = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate Type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_cord_type
				)
		self.mds_cord_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.mds_cord_type.add('distance', command = self.ok)
		self.mds_cord_type.add('phi', command = self.ok)
		self.mds_cord_type.add('psi', command = self.ok)
		self.mds_cord_type.add('angle', command = self.ok)
		
		self.mds_cord_type.invoke('distance')
		
		# Atom Indices 
		self.mds_atm_ind_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom indices:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.mds_atm_ind_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.mds_atm_ind_buttons.add('all', command = self.ok, text='All')
		self.mds_atm_ind_buttons.add('alpha', command = self.ok, text='CA')
		self.mds_atm_ind_buttons.add('backbone', command = self.ok, text='Backbone')
		self.mds_atm_ind_buttons.add('minimal', command = self.ok, text='Minimal')
		self.mds_atm_ind_buttons.invoke('alpha')
		
		mds_options_buttons=(self.mds_type_buttons, 
			self.atm_grp_buttons,  
			self.mds_dissimilarity_type, 
			self.mds_cord_type,
			self.mds_atm_ind_buttons)
		Pmw.alignlabels(mds_options_buttons)
		
		# Run MDS button
		
		self.run_mds_button = Pmw.ButtonBox(self.mds_page_main_group.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_mds_button.add('Run MDS',
			fg='blue', 
			command = self.run_mds)
		self.run_mds_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Exit button
		
		self.exit_mds = Pmw.ButtonBox(self.mds_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_mds.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_mds.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		##=========================================
		# t-SNE options
		#-----------------------------------------
		
		# t-SNE options
		
		self.tsne_page_main_group = Pmw.Group(self.radioframe, tag_text='t-SNE Options')
		self.tsne_page_main_group.pack(side=LEFT, fill = 'both', expand = 1, padx=4, pady=4)
		
		radiogroups.append(self.tsne_page_main_group)

		Pmw.aligngrouptags(radiogroups,)
		self.radioframe.pack(padx = 6, pady = 6, expand='yes', fill='both')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.atm_grp_buttons.add('All', command = self.ok)
		self.atm_grp_buttons.add('CA', command = self.ok)
		self.atm_grp_buttons.add('Backbone', command = self.ok)
		self.atm_grp_buttons.add('Protein', command = self.ok)
		self.atm_grp_buttons.invoke('CA')
		
		# Dissimilarity Type
		self.tsne_dissimilarity_type = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Dissimilarity type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_dissimilarity_type)
		self.tsne_dissimilarity_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.tsne_dissimilarity_type.add('Euclidean distance', command = self.ok)
		self.tsne_dissimilarity_type.add('RSMD', command = self.ok)
		self.tsne_dissimilarity_type.invoke('RSMD')
		
		# Cordinate Type
		self.tsne_cord_type = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate Type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_cord_type
				)
		self.tsne_cord_type.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.tsne_cord_type.add('distance', command = self.ok)
		self.tsne_cord_type.add('phi', command = self.ok)
		self.tsne_cord_type.add('psi', command = self.ok)
		self.tsne_cord_type.add('angle', command = self.ok)
		
		self.tsne_cord_type.invoke('distance')
		#print self.svd_solver_type.getvalue()
		
		# Atom Indices 
		self.atm_ind_buttons = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom indices:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.atm_ind_buttons.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		self.atm_ind_buttons.add('All', command = self.ok)
		self.atm_ind_buttons.add('CA', command = self.ok)
		self.atm_ind_buttons.add('Backbone', command = self.ok)
		self.atm_ind_buttons.add('Protein', command = self.ok)
		self.atm_ind_buttons.invoke('CA')
		mds_options_buttons=(self.mds_type_buttons, 
			self.atm_grp_buttons,  
			self.tsne_dissimilarity_type, 
			self.tsne_cord_type,
			self.atm_ind_buttons)
		Pmw.alignlabels(mds_options_buttons)
		
		# Run t-SNE button
		
		self.run_mds_button = Pmw.ButtonBox(self.tsne_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.run_mds_button.add('Run t-SNE',fg='blue', command = self.run_tsne)
		self.run_mds_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Exit button
		
		self.exit_mds = Pmw.ButtonBox(self.tsne_page_main_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_mds.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_mds.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		
		
		#==============================================================
        # NMA PAGE
		#==============================================================
		
		about_nma = """NMA analyses the oscillations of a structure. For proteins, it is useful for studying
the large amplitude motions for a selected conformation. The main assumption is that the motions are harmonic.
Thus, each normal mode, which is a concerted motion of many atoms, acts as a simple harmonic oscillator, and 
it is independent of all the other normal modes."""

		self.nma_top_group = Pmw.Group(self.nma_page,tag_text='About')
		self.nma_top_group.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
				
		myfont = Pmw.logicalfont(name='Helvetica',size=14)
		self.text_field = Pmw.ScrolledText(self.nma_top_group.interior(),
			borderframe=5,
			vscrollmode='dynamic',
			hscrollmode='dynamic',
			labelpos='n',
			text_width=250, text_height=4,
			text_wrap='word',
			text_background='skyblue4',
			text_foreground='white',
			text_font = myfont)
			
		self.text_field.pack(expand = 1, fill = 'both', padx = 2, pady = 2)
		self.text_field.insert('end',about_nma)
		self.text_field.configure(text_state=DISABLED)
		
		# input files
		self.nma_top_group1 = Pmw.Group(self.nma_page, tag_pyclass = None)
		self.nma_top_group1.pack(fill = 'both', expand = 1, padx = 2, pady = 2)

		self.trj_file_io = Pmw.Group(self.nma_top_group1.interior(), tag_text='Coarse Graining (1)')
		self.trj_file_io.pack(expand=1, fill='both', side=LEFT)
		
		
		# Read PDB file 
		self.cg_pdb_location = Pmw.EntryField(self.trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_cg_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB File:',
												)
		# coarse grain level
		self.var = StringVar()
		self.var.set('4')
		self.cg_level = Pmw.OptionMenu(self.trj_file_io.interior(),
				labelpos = 'w',
				label_text = 'CG Level:',
				menubutton_textvariable = self.var,
				items = ['1', '2', '3', '4', '5', '6'],
				menubutton_width = 10,
		)
		
		# Starting atom
		self.cg_start_atm = Pmw.EntryField(self.trj_file_io.interior(),
			labelpos = 'w',
			label_text = 'Starting atom:',
			value='1')
		self.cg_start_atm.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# output directory
		
		self.cg_out_dir_location = Pmw.EntryField(self.trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.set_cg_out_location),                                                
												label_text = 'Output Directory:',
												value  = os.getcwd())
		
		# out pdb file name
		self.cg_out_pdb = Pmw.EntryField(self.trj_file_io.interior(),
			labelpos = 'w',
			label_text = 'Output PDB:',
			value='ComplexCG.pdb')
		self.cg_out_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		entries=(self.cg_pdb_location,
					self.cg_level,
					self.cg_start_atm,
					self.cg_out_dir_location,
					self.cg_out_pdb)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
			
		# Run coarse garining
		self.run_cg_button = Pmw.ButtonBox(self.trj_file_io.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_cg_button.add('Run Coarse Graining',fg='blue', command = self.run_cg)
		self.run_cg_button.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
			
		Pmw.alignlabels(entries)
		
		# NMA options
		
		self.nma_group = Pmw.Group(self.nma_top_group1.interior(), tag_text='NMA (2)')
		self.nma_group.pack(expand=1, fill='both', side=LEFT)
		
		# Read PDB file 
		self.nma_pdb_location = Pmw.EntryField(self.nma_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_nma_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB File:',
												)
		self.nma_pdb_location.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		

		# Cutoff in Ang
		self.nma_cut = Pmw.EntryField(self.nma_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'Cutoff (A):',
												value='15',
												command = self.get_pc_selection)
		self.nma_cut.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# output directory
		
		self.nma_out_dir_location = Pmw.EntryField(self.nma_group.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.nma_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		self.nma_out_dir_location.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
												
		pca_options_buttons=(self.nma_pdb_location, 
			self.nma_cut, 
			self.nma_out_dir_location)
		Pmw.alignlabels(pca_options_buttons)
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.nma_group.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_pca_button.add('Run NMA',fg='blue', command = self.run_ipca)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		#===============================================
		# Get eigenvectors
		self.get_eig_group = Pmw.Group(self.nma_top_group1.interior(), tag_text='Get Eigenvectors (3)')
		self.get_eig_group.pack(expand=1, fill='both', side=LEFT)
		
		# read VT file
		self.nma_vtfile_location = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'VT value file:',
												)
		self.nma_vtfile_location.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# mode index 
		
		self.nma_mode_idx = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_text = 'Mode index:',
												command = self.get_pc_selection)
		self.nma_mode_idx.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Direction
		
		self.nma_direction = Pmw.OptionMenu(self.get_eig_group.interior(),
				labelpos = 'w',
				label_text = 'Direction:',
				items = ['1', '-1'],
				menubutton_width = 10,
		)
		self.nma_direction.pack(anchor = 'w', padx = 10, pady = 10)
		
		# Get eigenvectors
		self.nma_get_eigev = Pmw.ButtonBox(self.get_eig_group.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.nma_get_eigev.add('Get eigenvectors',fg='blue', command = self.run_ipca)
		self.nma_get_eigev.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		
		## second group
		## Mean square fluctuation
		self.nma_second_group = Pmw.Group(self.nma_page,  tag_pyclass = None)
		self.nma_second_group.pack(expand=1, fill='both')
		
		self.nma_msf = Pmw.Group(self.nma_second_group.interior(), tag_text='Mean square fluctuation (4)')
		self.nma_msf.pack(expand=1, fill='both', side=LEFT)
		
		# read PDB
		self.msf_pdb = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB file:',
												)
		self.msf_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# read conformation PDB
		self.msf_conf_pdb = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'Conformation PDB file:',
												)
		self.msf_conf_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# first mode
		
		self.nma_first_mode = Pmw.EntryField(self.nma_msf.interior(),
                                                labelpos = 'w',
                                                label_text = 'First mode:',
												command = self.get_pc_selection)
		self.nma_first_mode.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# second mode
		
		self.nma_second_mode = Pmw.EntryField(self.nma_msf.interior(),
                                                labelpos = 'w',
                                                label_text = 'Second mode:',
												command = self.get_pc_selection)
		self.nma_second_mode.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		#W matrix file
		self.msf_WMatrixFile = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'W Matrix File:',
												)
		self.msf_WMatrixFile.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		#VT matrix file
		self.msf_VTMatrixFile = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'VT Matrix File:',
												)
		self.msf_VTMatrixFile.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Run MSF
		self.run_msf_button = Pmw.ButtonBox(self.nma_msf.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_msf_button.add('Run MSF',fg='blue', command = self.run_ipca)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		##====================================
		# conformation/ combination mode
		
		self.nma_conf_mode = Pmw.Group(self.nma_second_group.interior(),
			tag_text='Conformation/Combination mode (5)')
		self.nma_conf_mode.pack(expand=1, fill='both', side=LEFT)
		
		## Unaligned PDB file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'Unaligned PDB file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		## PDB file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		## VT Matrix file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'VT Matrix file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		## Output file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'Output file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Get conformation mode
		self.run_msf_button = Pmw.ButtonBox(self.nma_conf_mode.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_msf_button.add('Get conf. modes',fg='blue', command = self.run_ipca)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Get combination mode
		self.run_msf_button = Pmw.ButtonBox(self.nma_conf_mode.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_msf_button.add('Get comb. modes',fg='blue', command = self.run_ipca)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		##====================================
		# mode visualization
		
		self.nma_mode_vis = Pmw.Group(self.nma_second_group.interior(), tag_text='Mode visualization (6)')
		self.nma_mode_vis.pack(expand=1, fill='both', side=LEFT)
		
		## CG PDB file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_mode_vis.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'CG PDB file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		## mode index value
		self.mode_indx_value = Pmw.EntryField(self.nma_mode_vis.interior(),
												labelpos = 'w',
												command = self.get_pc_selection,                                                
												label_text = 'Mode index value:',
												)
		self.mode_indx_value.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		## Vector file
		self.conf_mode_Unalgn_pdb = Pmw.EntryField(self.nma_mode_vis.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'Vector file:',
												)
		self.conf_mode_Unalgn_pdb.pack(fill = 'both', expand = 1, padx = 10, pady = 2)
		
		# Get mode visualization
		self.run_msf_button = Pmw.ButtonBox(self.nma_mode_vis.interior(),
			orient='horizontal',
			padx=0,
			pady=0)
		self.run_msf_button.add('Get modes Vis',fg='blue', command = self.run_ipca)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 10, pady = 2)
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.nma_page,orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		
		
		#=====================================================
        # ABOUT PAGE
		#=======================================================
		
		# about section
		
		about_pca = """

pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.
		
MODE-TASK is a collection of tools for analysing normal modes and performing principal component analysis.		
pyMODE-TASK is the pymol plugin of MODE-TASK. Orignal command line version of MODE-TASK can be found at https://github.com/RUBi-ZA/MODE-TASK. 

Authours. (1)- MODE-TASK, CJ Ross, B Nizami, M Glenister, OS Amamuddy, AR Atilgan, C Atilgan and O Tastan Bishop.

(2)- pyMODE-TASK is written by:

Bilal Nizami

Research Unit in Bioinformatics (RUBi)
Rhodes University
Grahamstown, South Africa   
https://rubi.ru.ac.za 
2017. 

email: nizamibilal1064@gmail.com"""
		self.about_top_group = Pmw.Group(self.about_page,tag_text='About')
		self.about_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Courier',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.about_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=40,
                             text_wrap='word',
                             text_background='skyblue4',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_pca)
		self.text_field.configure(text_state=DISABLED)
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.about_top_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		#---------------------------------------------------------------
        # CITATION PAGE
		#=======================================================
		
		# citation section
		
		citation = """

pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.
		
pyMODE-TASK is a pymol plugin for MODE-TASK. If you use MODE-TASK and/or pyMODE-TASK, kindly cite the 
following papers.

(1)- MODE-TASK, CJ Ross, B Nizami, M Glenister, OS Amamuddy, AR Atilgan, C Atilgan and O Tastan Bishop.

(2)- pyMODE-TASK is written by:

Bilal Nizami

Research Unit in Bioinformatics (RUBi)
Rhodes University
Grahamstown, South Africa   
https://rubi.ru.ac.za 
2017. 

Report bug at:

email: nizamibilal1064@gmail.com"""
		self.citation_top_group = Pmw.Group(self.citation_page,tag_text='Citation')
		self.citation_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Times',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.citation_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=40,
                             text_wrap='word',
                             text_background='skyblue4',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',citation)
		self.text_field.configure(text_state=DISABLED)
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.citation_top_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
		
		#---------------------------------------------------------------
        # HELP PAGE
		#=======================================================
		
		help = """
See the help page of MODE-TASK at   http://mode-task.readthedocs.io/en/latest/index.html


Credit:

1. Bilal Nizami - plugin design and implementaion, PCA implementaion

2. Caroline Ross - NMA implementaion

3. Ozlem Tastan Bishop - Design, idea and principle investigator

Research Unit in Bioinformatics (RUBi), Rhodes University, Grahamstown, South Africa


"""
		link = '''Read the doc'''
		
		self.help_top_group = Pmw.Group(self.help_page,tag_text='Help and Credit')
		self.help_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)
		
		myfont = Pmw.logicalfont(name='Courier',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.help_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=13,
                             text_wrap='word',
                             text_background='skyblue4',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',help)
		self.text_field.configure(text_state=DISABLED)
		
		# Create dialog.
		Pmw.aboutversion('1.0')
		Pmw.aboutcopyright('Copyright Bilal Nizami 2017\nAll rights reserved\n The project is licensed under GNU GPL 3.0')
		Pmw.aboutcontact(
            'To report bug, for help and suggestion contact:\n' +
            '  email: nizamibilal1064@gmail'
		)
		self.about = Pmw.AboutDialog(self.help_top_group.interior(), applicationname = 'pyMODE-TASK')
		self.about.withdraw()

        # Create button to launch the dialog.
		w = Button(self.help_top_group.interior(), text = 'About pyMODE-TASK',
				command = self.execute)
		w.pack(padx = 8, pady = 8)
		
		
		# Exit button
		
		self.exit_pca = Pmw.ButtonBox(self.help_top_group.interior(),orient='horizontal', padx=0,pady=0)
		self.exit_pca.add('EXIT', fg='red', command = self.frame.quit)
		self.exit_pca.pack(side=RIGHT, expand = 1, padx = 10, pady = 2)
	
		
	def execute(self):
		self.about.show()

	def ok(self):
		print 'You clicked on OK'
		
	def run_pca(self):
		
		# core scripts are located at src directory under pyMODE-TASK directory
		cmd_dir = './src'
		trj_loc = self.pca_trj_location.getvalue()
		top_loc = self.pca_top_location.getvalue()
		pc_sele = self.pca_methods_buttons.getvalue()
		st_sele = self.svd_solver_type.getvalue()
		kt_sele = self.kernel_type.getvalue()
		ag_sele = self.atm_grp_buttons.getvalue()
		pc_comp = self.pca_comp.getvalue()
		out_loc = self.pca_out_dir_location.getvalue()
		ref_loc = self.pca_ref_file.getvalue()


		if trj_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
		if top_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
		
		else:
			if ref_loc != '':
				cmd = './src/pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -r ' + ref_loc
			else:				
				tkMessageBox.showinfo("pyMODE-TASK warning!", "No Ref structure given, using deafult first frame!")
				cmd = './src/pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc
			
			out = `os.system(cmd)`
			if out == '0':
				tkMessageBox.showinfo("pyMODE-TASK!", "\tPCA run successful!\nResults are written in Output Directory!")
			else:
				tkMessageBox.showinfo("pyMODE-TASK!", "PCA run failed. See terminal for details!")			
		
	def run_ipca(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		cmd_dir = './src'
		trj_loc = self.ipca_trj_location.getvalue()
		top_loc = self.ipca_top_location.getvalue()
		ct_sele = self.ct_buttons.getvalue()
		ag_sele = self.ipca_atm_grp_buttons.getvalue()
		pc_comp = self.pca_comp.getvalue()
		out_loc = self.ipca_out_dir_location.getvalue()
	
		if trj_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
		if top_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
		else:	
			cmd = './src/internal_pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele
			out = `os.system(cmd)`
			#print type(out)
			if out == '0':
				tkMessageBox.showinfo("pyMODE-TASK!", "\tInternal PCA run successful!\nResults are written in Output Directory!")
			else:
				tkMessageBox.showinfo("pyMODE-TASK!", "Internal PCA run failed. See terminal for details!")

	def run_mds(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		cmd_dir = './src'
		trj_loc = self.mds_trj_location.getvalue()
		top_loc = self.mds_top_location.getvalue()
		mds_type = self.mds_type_buttons.getvalue()
		ct_sele = self.mds_cord_type.getvalue()
		ag_sele = self.atm_grp_buttons.getvalue()
		dist_type = self.mds_dissimilarity_type.getvalue()
		out_loc = self.mds_out_dir_location.getvalue()
		atm_ind = self.mds_atm_ind_buttons.getvalue()
		if trj_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
		if top_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
		else:	
			cmd = './src/mds.py -t '+ trj_loc + ' -p ' + top_loc + ' -mt ' + mds_type +' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele + ' -ai ' + atm_ind + ' -dt ' + dist_type
			out = `os.system(cmd)`
			#print type(out)
			if out == '0':
				tkMessageBox.showinfo("pyMODE-TASK!", "\tMDS run successful!\nResults are written in Output Directory!")
			else:
				tkMessageBox.showinfo("pyMODE-TASK!", "MDS run failed. See terminal for details!")
	
	def run_tsne(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		cmd_dir = './src'
		trj_loc = self.mds_trj_location.getvalue()
		top_loc = self.mds_top_location.getvalue()
		ct_sele = self.mds_cord_type.getvalue()
		ag_sele = self.atm_grp_buttons.getvalue()
		dist_type = self.mds_dissimilarity_type.getvalue()
		out_loc = self.mds_out_dir_location.getvalue()
		atm_ind = self.mds_atm_ind_buttons.getvalue()
		if trj_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
		if top_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
		else:	
			cmd = './src/tsne.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele + ' -ai ' + atm_ind + ' -dt ' + dist_type
			out = `os.system(cmd)`
			#print type(out)
			if out == '0':
				tkMessageBox.showinfo("pyMODE-TASK!", "\tt-SNE run successful!\nResults are written in Output Directory!")
			else:
				tkMessageBox.showinfo("pyMODE-TASK!", "t-SNE run failed. See terminal for details!")
	
	def run_cg(self):
		# core scripts are located at src directory under pyMODE-TASK directory
		cmd_dir = './src'
		pdb_loc = self.cg_pdb_location.getvalue()
		cg_level = self.cg_level.getvalue()
		out_loc = self.cg_out_dir_location.getvalue()
		#out_loc = out_loc + '/ComplexCG.pdb'
		out_pdb = self.cg_out_pdb.getvalue()
		print out_loc
		start_atm = self.cg_start_atm.getvalue()
		atm_type = 'CB'
		if pdb_loc == '':
			tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB location given!")
		else:	
			cmd = './src/coarseGrain.py --pdb ' + pdb_loc + ' --cg ' + cg_level + ' --atomType ' + atm_type + ' --startingAtom ' + start_atm + ' --outdir ' + out_loc + ' --output ' + out_pdb
			out = `os.system(cmd)`
			#print type(out)
			if out == '0':
				tkMessageBox.showinfo("pyMODE-TASK!", "\tCoarse graining run successful!\nResults are written in Output Directory!")
			else:
				tkMessageBox.showinfo("pyMODE-TASK!", "Coarse graining run failed. See terminal for details!")
	
	def pca_set_trj_filename(self, filename):
		n = self.pca_trj_location.setvalue(filename)
		return n
				
	def ipca_set_trj_filename(self, filename):
		n = self.ipca_trj_location.setvalue(filename)
		return n
		
	def set_pdb_filename(self, filename):
		n = self.pdb_location.setvalue(filename)
		return n
		
	def get_pc_method_selection(self, sele_option):
		n=self.pca_methods_buttons.getvalue()
		return n
		
	def get_mds_type_selection(self, sele_option):
		n=self.mds_type_buttons.getvalue()
		return n
	
	def mds_set_trj_filename(self, filename):
		n = self.mds_trj_location.setvalue(filename)
		return n

	def mds_set_top_filename(self, filename):
		self.mds_top_location.setvalue(filename)
	
	def mds_set_out_location(self, dirname):
		self.mds_out_dir_location.setvalue(dirname)

	def get_st_selection(self, sele_option):
		n=self.svd_solver_type.getvalue()
		return n
		
	def get_kt_selection(self, sele_option):
		n=self.kernel_type.getvalue()
		return n
		
	def get_ag_selection(self, sele_option):
		n=self.atm_grp_buttons.getvalue()
		return n
		
	def get_ipca_ag_selection(self, sele_option):
		n=self.ipca_atm_grp_buttons.getvalue()
		return n
		
	def get_pc_selection(self, sele_option):
		n= self.pca_comp.getvalue()
		return n
		
	def get_cg_selection(self, sele_option):
		n= self.cg_level.getvalue()
		return n

	def set_top_filename(self, filename):
		self.pca_top_location.setvalue(filename)
	
	def ipca_set_top_filename(self, filename):
		self.ipca_top_location.setvalue(filename)
	
		
	def set_ref_filename(self, filename):
		self.pca_ref_file.setvalue(filename)
		
	def pca_set_out_location(self, dirname):
		self.pca_out_dir_location.setvalue(dirname)
	
	def ipca_set_out_location(self, dirname):
		self.ipca_out_dir_location.setvalue(dirname)
		
	def nma_set_out_location(self, dirname):
		self.nma_out_dir_location.setvalue(dirname)
	
	def get_mds_dissimilarity_type(self, sele_option):
		n= self.mds_dissimilarity_type.getvalue()
		return n
		
	def get_mds_cord_type(self, sele_option):
		n=self.mds_cord_type.getvalue()
		return n
	
	def set_cg_pdb_filename(self, filename):
		n = self.cg_pdb_location.setvalue(filename)
		return n
		
	def set_cg_out_location(self, dirname):
		self.cg_out_dir_location.setvalue(dirname)
		
	def set_nma_pdb_filename(self, filename):
		n = self.nma_pdb_location.setvalue(filename)
		return n
		
	def about(self):
		print "pyMODE-TASK!\n pymol plugin of MODE-TASK\n MODE-TASK: a software tool to perform PCA and NMA of protein structure and MD trajectories"

class FileDialogButtonClassFactory:
	def get(fn,mode = 'r',filter=[("Executable",'*')]):
		"""This returns a FileDialogButton class that will
		call the specified function with the resulting file.
		"""
		class FileDialogButton(Button):
            # This is just an ordinary button with special colors.

			def __init__(self, master=None, cnf={}, **kw):
				'''when we get a file, we call fn(filename)'''
				self.fn = fn
				self.__toggle = 0
				apply(Button.__init__, (self, master, cnf), kw)
				self.configure(command=self.set)
			def set(self):
				if mode == 'r':
					n = MyFileDialog(types = filter).getopenfile()
				elif mode == 'w':
					n = MyFileDialog(types = filter).getsavefile()
#                n = MyFileDialog().get()
#                fd = PmwFileDialog(self.master,filter=filter)
#                fd.title('Please choose a file')
#                n=fd.askfilename()
				if n is not None:
					self.fn(n)
			#print fn
		return FileDialogButton
	get = staticmethod(get)
	
class DirDialogButtonClassFactory:
	def get(fn):
		"""This returns a FileDialogButton class that will
		call the specified function with the resulting file.
		"""
		class DirDialogButton(Button):
			# This is just an ordinary button with special colors.

			def __init__(self, master=None, cnf={}, **kw):
				'''when we get a file, we call fn(filename)'''
				self.fn = fn
				self.__toggle = 0
				apply(Button.__init__, (self, master, cnf), kw)
				self.configure(command=self.set)
			def set(self):
				fd = PmwDirDialog(self.master)
				fd.title('Please choose a directory')
				n=fd.askfilename()
				if n is not None:
					self.fn(n)
		return DirDialogButton
	get = staticmethod(get)
class PmwFileDialog(Pmw.Dialog):
    """File Dialog using Pmw"""
    def __init__(self, parent = None, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('filter',    '*',              self.newfilter),
            ('directory', os.getcwd(),      self.newdir),
            ('filename',  '',               self.newfilename),
            ('historylen',10,               None),
            ('command',   None,             None),
            ('info',      None,             None),
            )
        self.defineoptions(kw, optiondefs)
        # Initialise base class (after defining options).
        Pmw.Dialog.__init__(self, parent)

        self.withdraw()

        # Create the components.
        interior = self.interior()

        if self['info'] is not None:
            rowoffset=1
            dn = self.infotxt()
            dn.grid(row=0,column=0,columnspan=2,padx=3,pady=3)
        else:
            rowoffset=0

        dn = self.mkdn()
        dn.grid(row=0+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        del dn

        # Create the directory list component.
        dnb = self.mkdnb()
        dnb.grid(row=1+rowoffset,column=0,sticky='news',padx=3,pady=3)
        del dnb

        # Create the filename list component.
        fnb = self.mkfnb()
        fnb.grid(row=1+rowoffset,column=1,sticky='news',padx=3,pady=3)
        del fnb

        # Create the filter entry
        ft = self.mkft()
        ft.grid(row=2+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        del ft

        # Create the filename entry
        fn = self.mkfn()
        fn.grid(row=3+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        fn.bind('<Return>',self.okbutton)
        del fn

        # Buttonbox already exists
        bb=self.component('buttonbox')
        bb.add('OK',command=self.okbutton)
        bb.add('Cancel',command=self.cancelbutton)
        del bb

        Pmw.alignlabels([self.component('filename'),
                         self.component('filter'),
                         self.component('dirname')])

    def infotxt(self):
        """ Make information block component at the top """
        return self.createcomponent(
                'infobox',
                (), None,
                Tkinter.Label, (self.interior(),),
                width=51,
                relief='groove',
                foreground='darkblue',
                justify='left',
                text=self['info']
            )

    def mkdn(self):
        """Make directory name component"""
        return self.createcomponent(
            'dirname',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['directory'],
            entryfield_entry_width=40,
            entryfield_validate=self.dirvalidate,
            selectioncommand=self.setdir,
            labelpos='w',
            label_text='Directory:')

    def mkdnb(self):
        """Make directory name box"""
        return self.createcomponent(
            'dirnamebox',
            (), None,
            Pmw.ScrolledListBox, (self.interior(),),
            label_text='directories',
            labelpos='n',
            hscrollmode='none',
            dblclickcommand=self.selectdir)

    def mkft(self):
        """Make filter"""
        return self.createcomponent(
            'filter',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['filter'],
            entryfield_entry_width=40,
            selectioncommand=self.setfilter,
            labelpos='w',
            label_text='Filter:')

    def mkfnb(self):
        """Make filename list box"""
        return self.createcomponent(
            'filenamebox',
            (), None,
            Pmw.ScrolledListBox, (self.interior(),),
            label_text='files',
            labelpos='n',
            hscrollmode='none',
            selectioncommand=self.singleselectfile,
            dblclickcommand=self.selectfile)

    def mkfn(self):
        """Make file name entry"""
        return self.createcomponent(
            'filename',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['filename'],
            entryfield_entry_width=40,
            entryfield_validate=self.filevalidate,
            selectioncommand=self.setfilename,
            labelpos='w',
            label_text='Filename:')
    
    def dirvalidate(self,string):
        if os.path.isdir(string):
            return Pmw.OK
        else:
            return Pmw.PARTIAL
        
    def filevalidate(self,string):
        if string=='':
            return Pmw.PARTIAL
        elif os.path.isfile(string):
            return Pmw.OK
        elif os.path.exists(string):
            return Pmw.PARTIAL
        else:
            return Pmw.OK
        
    def okbutton(self):
        """OK action: user thinks he has input valid data and wants to
           proceed. This is also called by <Return> in the filename entry"""
        fn=self.component('filename').get()
        self.setfilename(fn)
        if self.validate(fn):
            self.canceled=0
            self.deactivate()

    def cancelbutton(self):
        """Cancel the operation"""
        self.canceled=1
        self.deactivate()

    def tidy(self,w,v):
        """Insert text v into the entry and at the top of the list of 
           the combobox w, remove duplicates"""
        if not v:
            return
        entry=w.component('entry')
        entry.delete(0,'end')
        entry.insert(0,v)
        list=w.component('scrolledlist')
        list.insert(0,v)
        index=1
        while index<list.index('end'):
            k=list.get(index)
            if k==v or index>self['historylen']:
                list.delete(index)
            else:
                index=index+1
        w.checkentry()

    def setfilename(self,value):
        if not value:
            return
        value=os.path.join(self['directory'],value)
        dir,fil=os.path.split(value)
        self.configure(directory=dir,filename=value)
        
        c=self['command']
        if callable(c):
            c()

    def newfilename(self):
        """Make sure a newly set filename makes it into the combobox list"""
        self.tidy(self.component('filename'),self['filename'])
        
    def setfilter(self,value):
        self.configure(filter=value)

    def newfilter(self):
        """Make sure a newly set filter makes it into the combobox list"""
        self.tidy(self.component('filter'),self['filter'])
        self.fillit()

    def setdir(self,value):
        self.configure(directory=value)

    def newdir(self):
        """Make sure a newly set dirname makes it into the combobox list"""
        self.tidy(self.component('dirname'),self['directory'])
        self.fillit()

    def singleselectfile(self):
        """Single click in file listbox. Move file to "filename" combobox"""
        cs=self.component('filenamebox').curselection()
        if cs!=():
            value=self.component('filenamebox').get(cs)
            self.setfilename(value)

    def selectfile(self):
        """Take the selected file from the filename, normalize it, and OK"""
        self.singleselectfile()
        value=self.component('filename').get()
        self.setfilename(value)
        if value:
            self.okbutton()

    def selectdir(self):
        """Take selected directory from the dirnamebox into the dirname"""
        cs=self.component('dirnamebox').curselection()
        if cs!=():
            value=self.component('dirnamebox').get(cs)
            dir=self['directory']
            if not dir:
                dir=os.getcwd()
            if value:
                if value=='..':
                    dir=os.path.split(dir)[0]
                else:
                    dir=os.path.join(dir,value)
            self.configure(directory=dir)
            self.fillit()

    def askfilename(self,directory=None,filter=None):
        """The actual client function. Activates the dialog, and
           returns only after a valid filename has been entered 
           (return value is that filename) or when canceled (return 
           value is None)"""
        if directory!=None:
            self.configure(directory=directory)
        if filter!=None:
            self.configure(filter=filter)
        self.fillit()
        self.canceled=1 # Needed for when user kills dialog window
        self.activate()
        if self.canceled:
            return None
        else:
            return self.component('filename').get()

    lastdir=""
    lastfilter=None
    lasttime=0
    def fillit(self):
        """Get the directory list and show it in the two listboxes"""
        # Do not run unnecesarily
        if self.lastdir==self['directory'] and self.lastfilter==self['filter'] and self.lasttime>os.stat(self.lastdir)[8]:
            return
        self.lastdir=self['directory']
        self.lastfilter=self['filter']
        self.lasttime=time()
        dir=self['directory']
        if not dir:
            dir=os.getcwd()
        dirs=['..']
        files=[]
        try:
            fl=os.listdir(dir)
            fl.sort()
        except os.error,arg:
            if arg[0] in (2,20):
                return
            raise
        for f in fl:
            if os.path.isdir(os.path.join(dir,f)):
                dirs.append(f)
            else:
                filter=self['filter']
                if not filter:
                    filter='*'
                if fnmatch.fnmatch(f,filter):
                    files.append(f)
        self.component('filenamebox').setlist(files)
        self.component('dirnamebox').setlist(dirs)
    
    def validate(self,filename):
        """Validation function. Should return 1 if the filename is valid, 
           0 if invalid. May pop up dialogs to tell user why. Especially 
           suited to subclasses: i.e. only return 1 if the file does/doesn't 
           exist"""
        return 1
		
class PmwDirDialog(PmwFileDialog):
    """Directory Dialog using Pmw"""
    def __init__(self, parent = None, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('directory', os.getcwd(),      self.newdir),
            ('historylen',10,               None),
            ('command',   None,             None),
            ('info',      None,             None),
            )
        self.defineoptions(kw, optiondefs)
        # Initialise base class (after defining options).
        Pmw.Dialog.__init__(self, parent)

        self.withdraw()

        # Create the components.
        interior = self.interior()

        if self['info'] is not None:
            rowoffset=1
            dn = self.infotxt()
            dn.grid(row=0,column=0,columnspan=2,padx=3,pady=3)
        else:
            rowoffset=0

        dn = self.mkdn()
        dn.grid(row=1+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        dn.bind('<Return>',self.okbutton)
        del dn

        # Create the directory list component.
        dnb = self.mkdnb()
        dnb.grid(row=0+rowoffset,column=0,columnspan=2,sticky='news',padx=3,pady=3)
        del dnb

        # Buttonbox already exists
        bb=self.component('buttonbox')
        bb.add('OK',command=self.okbutton)
        bb.add('Cancel',command=self.cancelbutton)
        del bb



    lastdir=""
    def fillit(self):
        """Get the directory list and show it in the two listboxes"""
        # Do not run unnecesarily
        if self.lastdir==self['directory']:
            return
        self.lastdir=self['directory']
        dir=self['directory']
        if not dir:
            dir=os.getcwd()
        dirs=['..']
        try:
            fl=os.listdir(dir)
            fl.sort()
        except os.error,arg:
            if arg[0] in (2,20):
                return
            raise
        for f in fl:
            if os.path.isdir(os.path.join(dir,f)):
                dirs.append(f)
        self.component('dirnamebox').setlist(dirs)

    def okbutton(self):
        """OK action: user thinks he has input valid data and wants to
           proceed. This is also called by <Return> in the dirname entry"""
        fn=self.component('dirname').get()
        self.configure(directory=fn)
        if self.validate(fn):
            self.canceled=0
            self.deactivate()
    
    def askfilename(self,directory=None):
        """The actual client function. Activates the dialog, and
           returns only after a valid filename has been entered 
           (return value is that filename) or when canceled (return 
           value is None)"""
        if directory!=None:
            self.configure(directory=directory)
        self.fillit()
        self.activate()
        if self.canceled:
            return None
        else:
            return self.component('dirname').get()

    def dirvalidate(self,string):
        if os.path.isdir(string):
            return Pmw.OK
        elif os.path.exists(string):
            return Pmw.PARTIAL
        else:
            return Pmw.OK

    def validate(self,filename):
        """Validation function. Should return 1 if the filename is valid, 
           0 if invalid. May pop up dialogs to tell user why. Especially 
           suited to subclasses: i.e. only return 1 if the file does/doesn't 
           exist"""
        if filename=='':
            _errorpop(self.interior(),"Empty filename")
            return 0
        if os.path.isdir(filename) or not os.path.exists(filename):
            return 1
        else:
            _errorpop(self.interior(),"This is not a directory")
            return 0   
			
class MyFileDialog:

    def __init__(self,types = [("Executable","*")]):
        self.types = types

    def getopenfile(self):
        result = tkFileDialog.askopenfilename(filetypes=self.types)
        if result == "":
            return None
        else:
            return result
    def getsavefile(self):
        result = tkFileDialog.asksaveasfilename(filetypes=self.types)
        if result == "":
            return None
        else:
            return result

class IORedirector(object):
	'''A general class for redirecting I/O to this Text widget.'''
	def __init__(self,text_area):
		self.text_area = text_area


class MyHelpPage:
	'A class for opening web help pages'
	def __init__(self, url):
		self.url=url
		
	def openpage(self):
		#print self.url
		webbrowser.open_new(self.url)
		
root = Tk()
app = App(root)
root.title("pyMODE-TASK")
root.geometry("1000x700")
#root.iconbitmap('icons.ico')
root.mainloop()
