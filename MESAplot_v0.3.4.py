## MESAPlot is a graphical and dynamical interface to analyse the MESA output 
## Developed by Maurizio Giannotti, Michael Wise, Wesam Azaizeh, Daria Vasilyeva, Sanja Zivanovic



print 'You are using MESAplot version 0.3.4. If it\'s your first time, initialization may take a moment.'
print 'Attempting library imports:'

import wx , numpy as np, matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg 
from matplotlib.figure import Figure
import pylab as pl, matplotlib.pyplot as plt, datetime, re, os, loadHistAndProf, default_settings as ds
from wx.lib.wordwrap import wordwrap

print 'Managing Files (File_Manager.py)'
##Allows user to use default path and skip file open dialogue. Also checks if the requested default path exists.
if ds.use_default_path:
    path_to_data=ds.default_path
    if os.path.isdir(path_to_data.rpartition(os.path.sep)[0]):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        pass    
    else:
        print 'Warning ! use_default_path is True but the attempted path:\n   ' + path_to_data + '\ndoes not exist. \Let\'s make believe use_default_path is false :) opening fileManager'
        import File_Manager as FM
        path_to_data=FM.path_folder
else:
    import File_Manager as FM
    path_to_data=FM.path_folder

##Uses supplied path to instance data
odat = loadHistAndProf.initData(path_to_data)

class container(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size)
        self.all_Habundances=['h1', 'he4', 'c12', 'o16']
        self.all_Hreactions=['pp', 'cno', 'tri_alfa', 'burn_c', 'burn_n', 'burn_o']
        self.all_Pabundances=['h1', 'he3','he4', 'c12', 'ni14','o16','ne20','mg24','si28','s32','ar36','ca40','ti44','cr48','cr56','fe52','fe54','fe56','ni56']
        self.all_Preactions=['pp', 'cno', 'tri_alfa', 'burn_c', 'burn_n', 'burn_o']
        self.MF=MainFrame(self)  ##Instances MainFrame
        self.all_H_columns=self.MF.H_columnsNames
        self.all_P_columns=self.MF.P_columnsNames 
## Populate top menus 
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        graph_menu = wx.Menu()  ## history-plot menu
        Haxes_operations_menu = wx.Menu()
        Pgraph_menu = wx.Menu()  ## profile-plot menu
        Paxes_operations_menu = wx.Menu()
        Customize_menu = wx.Menu()
        helpMenu = wx.Menu()
        menubar.Append(file_menu, "&File")
        menubar.Append(graph_menu, "&History Plots")    
        menubar.Append(Haxes_operations_menu, "History &Axes")
        menubar.Append(Pgraph_menu, "&Profile Plots")
        menubar.Append(Paxes_operations_menu, "Profile A&xes")
        menubar.Append(Customize_menu, "Plot &Customization")
        menubar.Append(helpMenu, "Help")
## file_menu (data and star Info)
        saveHistoryPlot = file_menu.Append(-1, "Export History Plot")
        self.Bind(wx.EVT_MENU, self.MF.saveHistoryPlot, saveHistoryPlot)  
        saveProfilePlot = file_menu.Append(-1, "Export Profile Plot")
        self.Bind(wx.EVT_MENU, self.MF.saveProfilePlot, saveProfilePlot)        
        file_menu.AppendSeparator()
        path_info = file_menu.Append(-1, "Data path")
        self.Bind(wx.EVT_MENU, self.on_path_info, path_info) 
        star_info_menu = file_menu.Append(-1, "Star Info")
        self.Bind(wx.EVT_MENU, self.on_star_info_menu, star_info_menu) 
        profile_info_menu = file_menu.Append(-1, "Current Prof. Info")
        self.Bind(wx.EVT_MENU, self.on_profile_info_menu, profile_info_menu)         
## graph_menu (types of history plots)
        standard_H_plot = graph_menu.Append(-1, "standard", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_standard_H_plot, standard_H_plot) 
        HR_plot = graph_menu.Append(-1, "HR-diagram", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_HR_plot, HR_plot) 
        central_abundances_plot = graph_menu.Append(-1, "central abundances", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_central_abundances_plot, central_abundances_plot) 
        central_reactions_plot = graph_menu.Append(-1, "central reactions", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_central_reactions_plot, central_reactions_plot) 
        new_history_plot = graph_menu.Append(-1, "personalized plot", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_new_history_plot, new_history_plot) 
## Haxes_operations_menu (History operations on axes)
        Hoperation_x=Haxes_operations_menu.AppendRadioItem(-1, "x")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_x, Hoperation_x) 
        Hoperation_logx=Haxes_operations_menu.AppendRadioItem(-1, "log_10 x")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_logx, Hoperation_logx) 
        Hoperation_powerx=Haxes_operations_menu.AppendRadioItem(-1, "10^x")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_powerx, Hoperation_powerx) 
        Haxes_operations_menu.AppendSeparator()
        Hoperation_y=Haxes_operations_menu.AppendRadioItem(-1, "y")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_y, Hoperation_y) 
        Hoperation_logy=Haxes_operations_menu.AppendRadioItem(-1, "log_10 y")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_logy, Hoperation_logy) 
        Hoperation_powery=Haxes_operations_menu.AppendRadioItem(-1, "10^y")
        self.Bind(wx.EVT_MENU, self.on_Hoperation_powery, Hoperation_powery)
        Haxes_operations_menu.AppendSeparator()
        item_reverse_Hx_axis = Haxes_operations_menu.Append(-1, "Reverse x-axis")
        self.Bind(wx.EVT_MENU, self.on_reverse_Hx_axis, item_reverse_Hx_axis) 
        item_reverse_Hy_axis = Haxes_operations_menu.Append(-1, "Reverse y-axis")
        self.Bind(wx.EVT_MENU, self.on_reverse_Hy_axis, item_reverse_Hy_axis)         
## Pgraph_menu (types of profile plots)
        standard_P_plot = Pgraph_menu.Append(-1, "standard", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_standard_P_plot, standard_P_plot) 
        composition_P_plot = Pgraph_menu.Append(-1, "composition", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_composition_P_plot, composition_P_plot) 
        reactions_P_plot = Pgraph_menu.Append(-1, "reactions", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_reactions_P_plot, reactions_P_plot) 
        new_profile_plot = Pgraph_menu.Append(-1, "personalized plot", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.on_new_profile_plot, new_profile_plot)
## Paxes_operations_menu (Profile operations on axes)
        Poperation_x=Paxes_operations_menu.AppendRadioItem(-1, "x")
        self.Bind(wx.EVT_MENU, self.on_Poperation_x, Poperation_x) 
        Poperation_logx=Paxes_operations_menu.AppendRadioItem(-1, "log_10 x")
        self.Bind(wx.EVT_MENU, self.on_Poperation_logx, Poperation_logx) 
        Poperation_powerx=Paxes_operations_menu.AppendRadioItem(-1, "10^x")
        self.Bind(wx.EVT_MENU, self.on_Poperation_powerx, Poperation_powerx) 
        Paxes_operations_menu.AppendSeparator()
        Poperation_y=Paxes_operations_menu.AppendRadioItem(-1, "y")
        self.Bind(wx.EVT_MENU, self.on_Poperation_y, Poperation_y) 
        Poperation_logy=Paxes_operations_menu.AppendRadioItem(-1, "log_10 y")
        self.Bind(wx.EVT_MENU, self.on_Poperation_logy, Poperation_logy) 
        Poperation_powery=Paxes_operations_menu.AppendRadioItem(-1, "10^y")
        self.Bind(wx.EVT_MENU, self.on_Poperation_powery, Poperation_powery)
        Paxes_operations_menu.AppendSeparator()
        item_reverse_Px_axis = Paxes_operations_menu.Append(-1, "Reverse x-axis")
        self.Bind(wx.EVT_MENU, self.on_reverse_Px_axis, item_reverse_Px_axis) 
        item_reverse_Py_axis = Paxes_operations_menu.Append(-1, "Reverse y-axis")
        self.Bind(wx.EVT_MENU, self.on_reverse_Py_axis, item_reverse_Py_axis)  
## Customize_menu
        central_abundances_menu = Customize_menu.Append(-1, "Central Abundances")
        self.Bind(wx.EVT_MENU, self.on_central_abundances_menu, central_abundances_menu) 
        central_reactions_menu = Customize_menu.Append(-1, "Central Reactions")
        self.Bind(wx.EVT_MENU, self.on_central_reactions_menu, central_reactions_menu) 
        abundances_menu = Customize_menu.Append(-1, "Composition")
        self.Bind(wx.EVT_MENU, self.on_abundances_menu, abundances_menu) 
        reactions_menu = Customize_menu.Append(-1, "Reactions")
        self.Bind(wx.EVT_MENU, self.on_reactions_menu, reactions_menu) 
        new_history_menu = Customize_menu.Append(-1, "personalized History")
        self.Bind(wx.EVT_MENU, self.on_new_history_menu, new_history_menu) 
        new_profile_menu = Customize_menu.Append(-1, "personalized Profile")
        self.Bind(wx.EVT_MENU, self.on_new_profile_menu, new_profile_menu) 
## helpMenu
        aboutMenu=helpMenu.Append(-1,"&About")
        self.Bind(wx.EVT_MENU, self.on_aboutMenu, aboutMenu)
        helpHelpMenu=helpMenu.Append(-1,"&Help")
        self.Bind(wx.EVT_MENU, self.on_helpHelpMenu, helpHelpMenu)
        
        self.SetMenuBar(menubar)
    def on_path_info(self, event):
        wx.MessageBox(FM.path_folder,"path to data in use")
    def on_star_info_menu(self, event):
        wx.MessageBox(odat.star_information,"Star Info")
    def on_profile_info_menu(self, event):
        wx.MessageBox(odat.profile_information[self.MF.profile_number],"Current Profile Info")
    def on_central_abundances_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_Habundances,title='central abundances',
                                        label1='Choose central abundances to show ',label2='in the hystory plot')
        self.CPF.Show()
        self.MF.central_abundances_to_plot=self.CPF.newlist
    def on_central_reactions_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_Hreactions,title='central reactions',
                                        label1='Choose central reactions to show ',label2='in the hystory plot')
        self.CPF.Show()
        self.MF.central_reactions_to_plot=self.CPF.newlist
    def on_abundances_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_Pabundances,title='Abundances (for Profile Plot)',
                                        label1='Choose abundances to show ',label2='in the profile plot')
        self.CPF.Show()
        self.MF.abundances_to_plot=self.CPF.newlist
    def on_reactions_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_Preactions,title='Reactions (for Profile Plot)',
                                        label1='Choose reactions to show ',label2='in the profile plot')
        self.CPF.Show()
        self.MF.reactions_to_plot=self.CPF.newlist
    def on_new_history_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_H_columns,title='Personalized History Plot',
                                        label1='Choose what to show ',label2='in the history plot')
        self.CPF.Show()
        self.MF.new_history_to_plot=self.CPF.newlist
    def on_new_profile_menu(self, event):
        import plot_manager as ppM
        self.CPF=ppM.CustumizePlotFrame(list_tot=self.all_P_columns,title='Personalized Profile Plot',
                                        label1='Choose what to show ',label2='in the profile plot')
        self.CPF.Show()
        self.MF.new_profile_to_plot=self.CPF.newlist
    def on_aboutMenu(self, event):
        aboutPanel = wx.Panel(self,wx.ID_ANY)
        about = wx.AboutDialogInfo()
        about.Name = "MESAplot"
        about.Version = "0.3"
        about.Description = wordwrap("MESAplot was created at Barry University by Maurizio Giannotti, Michael Wise, \
Wesam Azaizeh, Daria Vasilyeva, and Sanja Zivanovic. It is the successor to MESAFace, which was written in Mathematica. It is a \
work in progress. If you have any errors, notice behaviour that is unintuitive, or need particular functionality, \
be sure to let us know !",350,wx.ClientDC(aboutPanel))
        about.WebSite = ("http://www.mleewise.com/MESAplot.php","http://www.mleewise.com/MESAplot.php")
        wx.AboutBox(about)
    def on_helpHelpMenu(self,event):
        helpHelpPanel = wx.Panel(self,wx.ID_ANY)
        helpHelp = wx.AboutDialogInfo()
        helpHelp.Name = "Help"
        helpHelp.Description = wordwrap("For now, please consult us for help at mgiannotti@barry.edu \
and mwise@barry.edu .",350,wx.ClientDC(helpHelpPanel))
        helpHelp.WebSite = ("http://www.mleewise.com/MESAplot.php","http://www.mleewise.com/MESAplot.php")
        wx.AboutBox(helpHelp)
    def update_graph(self):
        self.MF.figure.clear()
        self.MF.drawplot()
        self.MF.canvas.draw()
## Operations on Axes
    def on_Hoperation_x(self, event):
        self.MF.Hoperation_x='x'
        self.update_graph()
    def on_Hoperation_logx(self, event):
        self.MF.Hoperation_x='log_10 x'
        self.update_graph()
    def on_Hoperation_powerx(self, event):
        self.MF.Hoperation_x='10^x'
        self.update_graph()
    def on_Hoperation_y(self, event):
        self.MF.Hoperation_y='x'
        self.update_graph()
    def on_Hoperation_logy(self, event):
        self.MF.Hoperation_y='log_10 x'
        self.update_graph()
    def on_Hoperation_powery(self, event):
        self.MF.Hoperation_y='10^x'
        self.update_graph()
    def on_Poperation_x(self, event):
        self.MF.Poperation_x='x'
        self.update_graph()
    def on_Poperation_logx(self, event):
        self.MF.Poperation_x='log_10 x'
        self.update_graph()
    def on_Poperation_powerx(self, event):
        self.MF.Poperation_x='10^x'
        self.update_graph()
    def on_Poperation_y(self, event):
        self.MF.Poperation_y='x'
        self.update_graph()
    def on_Poperation_logy(self, event):
        self.MF.Poperation_y='log_10 x'
        self.update_graph()
    def on_Poperation_powery(self, event):
        self.MF.Poperation_y='10^x'
        self.update_graph()
## END OPERATION ON AXIS ######################
## Functions on Plots       
    def on_standard_H_plot(self, event):
        self.MF.Hgraph_type="standard"
        self.MF.reverse_Hx_Axis=self.MF.reverse_Hy_Axis=False
        self.MF.type_of_Hgraph_lbl.SetValue('standard')
        self.MF.HSection_reverse_x_lbl.SetValue('')
        self.MF.HSection_reverse_y_lbl.SetValue('')
        self.update_graph()
    def on_standard_P_plot(self, event):
        self.MF.Pgraph_type="standard"
        self.MF.reverse_Px_Axis=self.MF.reverse_Py_Axis=False
        self.MF.type_of_Pgraph_lbl.SetValue('standard')
        self.MF.PSection_reverse_x_lbl.SetValue('')
        self.MF.PSection_reverse_y_lbl.SetValue('')
        self.update_graph()
    def on_HR_plot(self, event):
        self.MF.Hgraph_type="standard"
        self.MF.Hx_var='log_Teff'
        self.MF.Hy_var='log_L'
        self.MF.reverse_Hx_Axis=True
        self.MF.reverse_Hy_Axis=False
        self.MF.type_of_Hgraph_lbl.SetValue('HR-diagram')
        self.MF.HSection_reverse_x_lbl.SetValue('reversed')
        self.MF.HSection_reverse_y_lbl.SetValue('')
        self.update_graph()
        self.MF.Hx_dropDown.SetValue('log_Teff')
        self.MF.Hy_dropDown.SetValue('log_L')
    def on_central_abundances_plot(self, event):
        self.MF.Hgraph_type="central_composition"
        self.MF.Hx_var='star_age'
        self.MF.reverse_Hx_Axis=self.MF.reverse_Hy_Axis=False
        self.MF.type_of_Hgraph_lbl.SetValue('central abundances')
        self.MF.HSection_reverse_x_lbl.SetValue('')
        self.MF.HSection_reverse_y_lbl.SetValue('')
        self.update_graph()
        self.MF.Hx_dropDown.SetValue('star_age')
    def on_central_reactions_plot(self, event):
        self.MF.Hgraph_type="central_reactions"
        self.MF.Hx_var='star_age'
        self.MF.reverse_Hx_Axis=self.MF.reverse_Hy_Axis=False
        self.MF.type_of_Hgraph_lbl.SetValue('central reactions')
        self.MF.HSection_reverse_x_lbl.SetValue('')
        self.MF.HSection_reverse_y_lbl.SetValue('')
        self.update_graph()
        self.MF.Hx_dropDown.SetValue('star_age')
    def on_new_history_plot(self, event):
        self.MF.Hgraph_type="new_H"
        self.MF.reverse_Hx_Axis=self.MF.reverse_Hy_Axis=False
        self.MF.type_of_Hgraph_lbl.SetValue('personal')
        self.MF.HSection_reverse_x_lbl.SetValue('')
        self.MF.HSection_reverse_y_lbl.SetValue('')
        self.update_graph()
    def on_new_profile_plot(self, event):
        self.MF.Pgraph_type="new_P"
        self.MF.reverse_Px_Axis=self.MF.reverse_Py_Axis=False
        self.MF.type_of_Pgraph_lbl.SetValue('personal')
        self.MF.PSection_reverse_x_lbl.SetValue('')
        self.MF.PSection_reverse_y_lbl.SetValue('')
        self.update_graph()
    def on_composition_P_plot(self, event):
        self.MF.Pgraph_type="composition"
        self.MF.Px_var='mass'
        self.MF.reverse_Px_Axis=self.MF.reverse_Py_Axis=False
        self.MF.type_of_Pgraph_lbl.SetValue('composition')
        self.MF.PSection_reverse_x_lbl.SetValue('')
        self.MF.PSection_reverse_y_lbl.SetValue('')
        self.update_graph()
        self.MF.Px_dropDown.SetValue('mass')
    def on_reactions_P_plot(self, event):
        self.MF.Pgraph_type="reactions"
        self.MF.Px_var='mass'
        self.MF.reverse_Px_Axis=self.MF.reverse_Py_Axis=False
        self.MF.type_of_Pgraph_lbl.SetValue('reactions')
        self.MF.PSection_reverse_x_lbl.SetValue('')
        self.MF.PSection_reverse_y_lbl.SetValue('')
        self.update_graph()
        self.MF.Px_dropDown.SetValue('mass')
    def on_reverse_Hx_axis(self, event):
        self.MF.reverse_Hx_Axis=not(self.MF.reverse_Hx_Axis)
        if self.MF.reverse_Hx_Axis:
            lbl='reversed'
        else:
            lbl=''    
        self.MF.HSection_reverse_x_lbl.SetValue(lbl)
        self.update_graph()
    def on_reverse_Hy_axis(self, event):
        self.MF.reverse_Hy_Axis=not(self.MF.reverse_Hy_Axis)
        if self.MF.reverse_Hy_Axis:
            lbl='reversed'
        else:
            lbl=''    
        self.MF.HSection_reverse_y_lbl.SetValue(lbl)
        self.update_graph()
    def on_reverse_Px_axis(self, event):
        self.MF.reverse_Px_Axis=not(self.MF.reverse_Px_Axis)
        if self.MF.reverse_Px_Axis:
            lbl='reversed'
        else:
            lbl=''    
        self.MF.PSection_reverse_x_lbl.SetValue(lbl)
        self.update_graph()
    def on_reverse_Py_axis(self, event):
        self.MF.reverse_Py_Axis=not(self.MF.reverse_Py_Axis)
        if self.MF.reverse_Py_Axis:
            lbl='reversed'
        else:
            lbl=''    
        self.MF.PSection_reverse_y_lbl.SetValue(lbl)
        self.update_graph()
#################################################################################
class MainFrame(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollbars(1,1,1,1)
        self.SetBackgroundColour(wx.WHITE)
        self.reverse_Hx_Axis=False
        self.reverse_Hy_Axis=False
        self.reverse_Px_Axis=False
        self.reverse_Py_Axis=False
        self.Hgraph_type="standard"
        self.Pgraph_type="standard"
        self.show_HLegend_flag=self.show_PLegend_flag=True
        self.HLegend_position=self.PLegend_position='upper right'
        self.Legend_position_options=['upper right','upper left','lower left','lower right',
                                      'right','center left','center right','lower center',
                                      'upper center','center']
        self.Hoperation_x=self.Hoperation_y=self.Poperation_x=self.Poperation_y= 'x'
        self.H_columnsNames = odat.history_labels
        self.P_columnsNames = odat.profile_labels
        self.central_abundances_to_plot=ds.default_central_abundances    #for the history
        self.abundances_to_plot=ds.default_profile_abundances               #for the profile
        self.central_reactions_to_plot=ds.default_central_reactions      #for the history
        self.reactions_to_plot= ds.default_profile_reactions   #for the profile
        self.new_history_to_plot=['star_age']     #for the history
        self.new_profile_to_plot=['mass']     #for the profile
        Hx_var_deafult = 'star_age'
        self.Hx_var = Hx_var_deafult
        Hy_var_deafult = 'log_Teff'
        self.Hy_var = Hy_var_deafult
        Px_var_deafult = 'mass'
        self.Px_var = Px_var_deafult
        Py_var_deafult = 'radius'
        self.Py_var = Py_var_deafult
        profile_number_deafult = 1
        self.profile_number = profile_number_deafult
        self.start_H = 0
        self.end_H = -1
        self.start_P = 0
        self.end_P = -1
        self.show_age_flag = False
## Style
        self.lbl_ftsize =ds.font_size_for_plot_labels
        self.line_color = ds.plot_line_color
        self.lbl_color = ds.lbl_color
        self.age_line_color = ds.age_line_color ##Color of the age dot
##HISTORY
##        HSection_space_lbl = wx.StaticText(self, label="     ")
        HSection_type_of_plot_lbl = wx.StaticText(self, label="type of plot: ")
        HSection_type_of_plot_lbl.SetForegroundColour('red')
        HSection_title_lbl = wx.StaticText(self, label="HISTORY", style=wx.ALIGN_CENTRE)
        HSection_title_lbl.SetForegroundColour('red')
        self.type_of_Hgraph_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value=self.Hgraph_type)
        self.HSection_reverse_x_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value="")
        self.HSection_reverse_y_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value="")
        HSection_lbl= wx.BoxSizer(wx.HORIZONTAL)
        HSection_lbl.Add(HSection_type_of_plot_lbl, 0, wx.ALL, 1)
        HSection_lbl.Add(self.type_of_Hgraph_lbl, 0, wx.ALL, 1)
##  History x-axis
        self.Hx_button_sizer = wx.RadioBox(self, -1, "x-axis", (10, 10), wx.DefaultSize,
                                      ['star_age', 'log_Teff', 'log_L','log_center_T','log_center_Rho','log_center_P'],
                                      3, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.OnHxButton, self.Hx_button_sizer) 
        Hx_var_lbl = wx.StaticText(self, label="   x-var  ")
        Hx_var_lbl.SetForegroundColour('Blue')
        self.Hx_dropDown = wx.ComboBox(self, choices=self.H_columnsNames, size=(120, -1), style=wx.CB_DROPDOWN)
        self.Hx_dropDown.SetValue(Hx_var_deafult)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSelectVar_Hx, self.Hx_dropDown)
        Hx_menu_sizer = wx.BoxSizer(wx.VERTICAL)
        Hx_menu_sizer.Add(Hx_var_lbl, 0, wx.ALL, 1)
        Hx_menu_sizer.Add(self.Hx_dropDown, 0, wx.ALL, 1)
        Hx_menu_sizer.Add(self.HSection_reverse_x_lbl, 0, wx.ALL, 1)
        Hx_Var_Selector_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Hx_Var_Selector_sizer.Add(self.Hx_button_sizer, 0, wx.ALL, 1)
        Hx_Var_Selector_sizer.Add(Hx_menu_sizer, 0, wx.ALL, 1)
##  History y-axis
        self.Hy_button_sizer = wx.RadioBox(self, -1, "y-axis", (10, 10), wx.DefaultSize,
                                      ['star_age', 'log_Teff', 'log_L','log_center_T','log_center_Rho','log_center_P'],
                                      3, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.OnHyButton, self.Hy_button_sizer) 
        Hy_var_lbl = wx.StaticText(self, label="   y-var  ")
        Hy_var_lbl.SetForegroundColour('Blue')
        self.Hy_dropDown = wx.ComboBox(self, choices=self.H_columnsNames, size=(120, -1), style=wx.CB_DROPDOWN)
        self.Hy_dropDown.SetValue(Hy_var_deafult)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSelectVar_Hy, self.Hy_dropDown)
        Hy_menu_sizer = wx.BoxSizer(wx.VERTICAL)
        Hy_menu_sizer.Add(Hy_var_lbl, 0, wx.ALL, 1)
        Hy_menu_sizer.Add(self.Hy_dropDown,  0, wx.ALL, 1)
        Hy_menu_sizer.Add(self.HSection_reverse_y_lbl, 0, wx.ALL, 1)
        Hy_Var_Selector_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Hy_Var_Selector_sizer.Add(self.Hy_button_sizer, 0, wx.ALL, 1)
        Hy_Var_Selector_sizer.Add(Hy_menu_sizer, 0, wx.ALL, 1)
##  Combine everything for the History variable selector
        H_Var_Selector_sizer = wx.BoxSizer(wx.VERTICAL)
        H_Var_Selector_sizer.Add(Hx_Var_Selector_sizer, 0, wx.ALL, 1)
        H_Var_Selector_sizer.Add(Hy_Var_Selector_sizer, 0, wx.ALL, 1)
##  Slider Control for starting and ending point.
        H_start_lbl = wx.StaticText(self, label="start  ")
        H_start_lbl.SetForegroundColour('Blue')
        self.H_start_bar = wx.Slider(self, value=1, minValue = 1, maxValue=odat.history_size, size=(120, -1), style=wx.SL_HORIZONTAL)
        self.Bind(wx.EVT_SCROLL, self.EvtSelect_H_start, self.H_start_bar)
        H_end_lbl = wx.StaticText(self, label="end  ")
        H_end_lbl.SetForegroundColour('Blue')
        self.H_end_bar = wx.Slider(self, value=1, minValue = 1, maxValue=odat.history_size, size=(120, -1), style=wx.SL_INVERSE)
        self.Bind(wx.EVT_SCROLL, self.EvtSelect_H_end, self.H_end_bar)
        H_StartEnd_sizer = wx.BoxSizer(wx.HORIZONTAL)
        H_StartEnd_sizer.Add(H_start_lbl, 0, wx.ALL, 1)
        H_StartEnd_sizer.Add(self.H_start_bar, 0, wx.ALL, 1)
        H_StartEnd_sizer.Add(H_end_lbl, 0, wx.ALL, 1)
        H_StartEnd_sizer.Add(self.H_end_bar, 0, wx.ALL, 1) 
##  PROFILES
        PSection_title_lbl = wx.StaticText(self, label="PROFILE", style=wx.ALIGN_CENTRE)
        PSection_title_lbl.SetForegroundColour('red')

        PSection_type_of_plot_lbl = wx.StaticText(self, label="type of plot: ")
        PSection_type_of_plot_lbl.SetForegroundColour('red')
        self.type_of_Pgraph_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value=self.Pgraph_type)
        self.PSection_reverse_x_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value="")
        self.PSection_reverse_y_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
            value="")
        PSection_lbl= wx.BoxSizer(wx.HORIZONTAL)
        PSection_lbl.Add(PSection_type_of_plot_lbl, 0, wx.ALL, 1)
        PSection_lbl.Add(self.type_of_Pgraph_lbl, 0, wx.ALL, 1)
##  Profiles x-axis
        self.Px_button_sizer = wx.RadioBox(self, -1, "x-axis", (10, 10), wx.DefaultSize,
                                      ['mass', 'radius', 'logR', 'logT','logRho','logP'],
                                      3, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.OnPxButton, self.Px_button_sizer) 
        Px_var_lbl = wx.StaticText(self, label="   x-var  ")
        Px_var_lbl.SetForegroundColour('Blue')
        self.Px_dropDown = wx.ComboBox(self, choices=self.P_columnsNames, size=(120, -1), style=wx.CB_DROPDOWN)
        self.Px_dropDown.SetValue(Px_var_deafult)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSelectVar_Px, self.Px_dropDown)
        Px_menu_sizer = wx.BoxSizer(wx.VERTICAL)
        Px_menu_sizer.Add(Px_var_lbl, 0, wx.ALL, 1)
        Px_menu_sizer.Add(self.Px_dropDown, 0, wx.ALL, 1)
        Px_menu_sizer.Add(self.PSection_reverse_x_lbl, 0, wx.ALL, 1)
        Px_Var_Selector_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Px_Var_Selector_sizer.Add(self.Px_button_sizer, 0, wx.ALL, 1)
        Px_Var_Selector_sizer.Add(Px_menu_sizer, 0, wx.ALL, 1)
##  Profiles y-axis
        self.Py_button_sizer = wx.RadioBox(self, -1, "y-axis", (10, 10), wx.DefaultSize,
                                      ['mass', 'radius', 'logR', 'logT','logRho','logP'],
                                      3, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.OnPyButton, self.Py_button_sizer) 
        Py_var_lbl = wx.StaticText(self, label="   y-var  ")
        Py_var_lbl.SetForegroundColour('Blue')
        self.Py_dropDown = wx.ComboBox(self, choices=self.P_columnsNames, size=(120, -1), style=wx.CB_DROPDOWN)
        self.Py_dropDown.SetValue(Py_var_deafult)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSelectVar_Py, self.Py_dropDown)
        Py_menu_sizer = wx.BoxSizer(wx.VERTICAL)
        Py_menu_sizer.Add(Py_var_lbl, 0, wx.ALL, 1)
        Py_menu_sizer.Add(self.Py_dropDown, 0, wx.ALL, 1)
        Py_menu_sizer.Add(self.PSection_reverse_y_lbl, 0, wx.ALL, 1)
        Py_Var_Selector_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Py_Var_Selector_sizer.Add(self.Py_button_sizer, 0, wx.ALL, 1)
        Py_Var_Selector_sizer.Add(Py_menu_sizer, 0, wx.ALL, 1)
##  Combine everything for the Profile variable selector
        P_Var_Selector_sizer = wx.BoxSizer(wx.VERTICAL)
        P_Var_Selector_sizer.Add(Px_Var_Selector_sizer, 0, wx.ALL, 1)
        P_Var_Selector_sizer.Add(Py_Var_Selector_sizer, 0, wx.ALL, 1)
##  Slider Control for starting and ending point.
        P_start_lbl = wx.StaticText(self, label="start  ")
        P_start_lbl.SetForegroundColour('Blue')
        self.P_start_bar = wx.Slider(self, value=1, minValue = 1,
            maxValue=odat.max_profile_size, size=(120, -1), style=wx.SL_HORIZONTAL)
        self.Bind(wx.EVT_SCROLL, self.EvtSelect_P_start, self.P_start_bar)
        P_end_lbl = wx.StaticText(self, label="end  ")
        P_end_lbl.SetForegroundColour('Blue')
        self.P_end_bar = wx.Slider(self, value=1, minValue = 1,
            maxValue=odat.max_profile_size,size=(120, -1), style=wx.SL_INVERSE)
        self.Bind(wx.EVT_SCROLL, self.EvtSelect_P_end, self.P_end_bar) 
        P_StartEnd_sizer = wx.BoxSizer(wx.HORIZONTAL)
        P_StartEnd_sizer.Add(P_start_lbl, 0, wx.ALL, 1)
        P_StartEnd_sizer.Add(self.P_start_bar, 0, wx.ALL, 1)
        P_StartEnd_sizer.Add(P_end_lbl, 0, wx.ALL, 1)
        P_StartEnd_sizer.Add(self.P_end_bar, 0, wx.ALL, 1)
## show age in history plots
        self.show_age = wx.CheckBox(self, -1, ' Show Age')
        self.show_age.SetValue(self.show_age_flag)
        wx.EVT_CHECKBOX(self, self.show_age.GetId(), self.EvtShowAgeInHistory)
## show legend in history plots
        self.show_HLegend = wx.CheckBox(self, -1, ' Legend')
        self.show_HLegend.SetValue(self.show_HLegend_flag)
        wx.EVT_CHECKBOX(self, self.show_HLegend.GetId(), self.EvtShowAgeLegendInHistory)
        HLegend_position_lbl = wx.StaticText(self, label="      legend position  ")
        HLegend_position_lbl.SetForegroundColour('Blue')
        self.HLegend_position_dropDown = wx.ComboBox(self, choices=self.Legend_position_options, size=(120, -1), style=wx.CB_DROPDOWN)
        self.HLegend_position_dropDown.SetValue(self.HLegend_position)
        self.Bind(wx.EVT_COMBOBOX, self.EvtHLegendPosition, self.HLegend_position_dropDown)
        HLegend_position_sizer = wx.BoxSizer(wx.HORIZONTAL)
        HLegend_position_sizer.Add(self.show_HLegend, 0, wx.ALL, 1)
        HLegend_position_sizer.Add(HLegend_position_lbl, 0, wx.ALL, 1)
        HLegend_position_sizer.Add(self.HLegend_position_dropDown, 0, wx.ALL, 1)
## show legend in profile plots
        self.show_PLegend = wx.CheckBox(self, -1, ' Legend')
        self.show_PLegend.SetValue(self.show_PLegend_flag)
        wx.EVT_CHECKBOX(self, self.show_PLegend.GetId(), self.EvtShowAgeLegendInProfile)
        PLegend_position_lbl = wx.StaticText(self, label="      legend position  ")
        PLegend_position_lbl.SetForegroundColour('Blue')
        self.PLegend_position_dropDown = wx.ComboBox(self, choices=self.Legend_position_options, size=(120, -1), style=wx.CB_DROPDOWN)
        self.PLegend_position_dropDown.SetValue(self.PLegend_position)
        self.Bind(wx.EVT_COMBOBOX, self.EvtPLegendPosition, self.PLegend_position_dropDown)
        PLegend_position_sizer = wx.BoxSizer(wx.HORIZONTAL)
        PLegend_position_sizer.Add(self.show_PLegend, 0, wx.ALL, 1)
        PLegend_position_sizer.Add(PLegend_position_lbl, 0, wx.ALL, 1)
        PLegend_position_sizer.Add(self.PLegend_position_dropDown, 0, wx.ALL, 1)
##  Slider Control for the model number (age). The profile numbers are re-ordered in terms of increasing age.
##  So, the first profile to show is the one for the youngest model.
        star_age_lbl = wx.StaticText(self, label="star age")
        star_age_lbl.SetForegroundColour('Blue')
        self.profile_number_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
                    value=str(odat.sorted_profile_number(self.profile_number)))
        self.profile_Age_lbl = wx.TextCtrl(self, style=wx.TE_READONLY,
                    value=odat.redefine_age(odat.profileAge[odat.sorted_profile_number(self.profile_number)]))
        self.star_age_bar = wx.Slider(self, value=1, minValue = 1, maxValue=odat.num_profiles, size=(120, -1), style=wx.SL_HORIZONTAL)
        self.Bind(wx.EVT_SCROLL, self.EvtSelectVar_Pnumber, self.star_age_bar)
##Control panel Layout
        star_age_panel = wx.BoxSizer(wx.HORIZONTAL)
        star_age_panel.Add(star_age_lbl, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
        star_age_panel.Add(self.star_age_bar, 0, \
            wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)
        star_age_panel.Add(wx.StaticText(self, label="prof.#  "), 0, \
            wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)
        star_age_panel.Add(self.profile_number_lbl, 0, \
            wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)
        star_age_panel.Add(self.show_age, 0, \
            wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)
## Control Panel
        control_panel = wx.BoxSizer(wx.VERTICAL)
## History Controls
        control_panel.Add(wx.StaticLine(self,-1,style=wx.LI_HORIZONTAL), 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(HSection_title_lbl, 0, \
            wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, border=5)
        control_panel.Add(wx.StaticLine(self,-1,style=wx.LI_HORIZONTAL), 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(HSection_lbl, 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(H_Var_Selector_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(H_StartEnd_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(HLegend_position_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
## Profile Controls
        control_panel.Add(wx.StaticLine(self,-1,style=wx.LI_HORIZONTAL), 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(PSection_title_lbl, 0, \
            wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, border=5)
        control_panel.Add(wx.StaticLine(self,-1,style=wx.LI_HORIZONTAL), 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(PSection_lbl, 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(star_age_panel, 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(self.profile_Age_lbl, 0, \
            wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(P_Var_Selector_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(P_StartEnd_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
        control_panel.Add(PLegend_position_sizer, 0, \
            wx.ALIGN_LEFT | wx.ALL, border=5)
## Creating the figure and make it an interacting canvas
        self.figure = plt.Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.drawplot()
## Combining Controls and Plots into a sizer and fit to Frame
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(control_panel, 1, wx.ALIGN_TOP|wx.ALL)
        sizer.Add(self.canvas, 2, wx.EXPAND | wx.ALIGN_TOP | wx.ALL)
        self.SetSizer(sizer)
        self.Fit()
### Handles click events for plot -- Causes issues for Mac. 
##        self.canvas.mpl_connect('button_press_event',self.plotLeftClick)
##        self.canvas.mpl_connect('button_press_event',self.plotRightClick)
## Takes care of some erroneous warnings due to mouse events on plots
##        self.canvas.Bind(wx.EVT_MOUSE_CAPTURE_LOST,self.OnCaptureLost) 
##  Functions on Plots        
    def update_graph(self):
        self.figure.clear()
        self.drawplot()
        self.canvas.draw()
    def OnHxButton(self, Event):
        self.Hx_var=self.Hx_button_sizer.GetStringSelection()
        self.update_graph()
        self.Hx_dropDown.SetValue(self.Hx_var)
    def OnHyButton(self, Event):
        self.Hy_var=self.Hy_button_sizer.GetStringSelection()
        self.update_graph()
        self.Hy_dropDown.SetValue(self.Hy_var)
    def OnPxButton(self, Event):
        self.Px_var=self.Px_button_sizer.GetStringSelection()
        self.update_graph()
        self.Px_dropDown.SetValue(self.Px_var)
    def OnPyButton(self, Event):
        self.Py_var=self.Py_button_sizer.GetStringSelection()
        self.update_graph()
        self.Py_dropDown.SetValue(self.Py_var)
    def Hx_button_action(self, event):
        self.Hx_var=event.GetLabel()
        self.update_graph()
    def EvtSelectVar_Hx(self, event):
        self.Hx_var=event.GetString()
        self.Hx_var=event.GetString()
        self.Hx_button_sizer.SetStringSelection(self.Hx_var)
        self.update_graph()
    def EvtSelectVar_Hy(self, event):
        self.Hy_var=event.GetString()
        self.update_graph()
    def EvtSelect_H_start(self, event):
        self.start_H=event.GetInt()-1
        self.update_graph()
    def EvtSelect_H_end(self, event):
        self.end_H=-event.GetInt()
        self.update_graph()
    def EvtSelectVar_Px(self, event):
        self.Px_var=event.GetString()
        self.update_graph()
    def EvtSelectVar_Py(self, event):
        self.Py_var=event.GetString()
        self.update_graph()
    def EvtSelectVar_Pnumber(self, event):
        self.profile_number=event.GetInt()
        self.profile_number_lbl.SetValue(str(self.profile_number))
        self.profile_Age_lbl.SetValue(odat.redefine_age(odat.profileAge[self.profile_number]))
        self.update_graph()
    def EvtSelect_P_end(self, event):
        self.start_P=event.GetInt()-1
        self.update_graph()
    def EvtSelect_P_start(self, event):
        self.end_P=-event.GetInt()
        self.update_graph()
    def EvtShowAgeInHistory(self, event):
        self.show_age_flag = self.show_age.GetValue()
        self.update_graph()
    def EvtShowAgeLegendInHistory(self, event):
        self.show_HLegend_flag = self.show_HLegend.GetValue()
        self.update_graph()
    def EvtHLegendPosition(self, event):
        self.HLegend_position=event.GetString()
        self.update_graph()
    def EvtShowAgeLegendInProfile(self, event):
        self.show_PLegend_flag = self.show_PLegend.GetValue()
        self.update_graph()
    def EvtPLegendPosition(self, event):
        self.PLegend_position=event.GetString()
        self.update_graph()
    def operation(self,selected_operation,x):
        if selected_operation=='x':
            return x
        elif selected_operation=='log_10 x':
            return np.log10(x).tolist()
        elif selected_operation=='10^x':
            return np.power(10, x).tolist()
    def operation_label(self,selected_operation,x):
        if selected_operation=='x':
            return x
        elif selected_operation=='log_10 x':
            return 'log('+x+')'
        elif selected_operation=='10^x':
            return '10^('+x+')'
    def OnCaptureLost(self,event): # fixes warnings that appear in terminal for certain mouse events
        pass
    def plotLeftClick(self,event): # forces an update to the plots
        self.update_graph()
    def plotRightClick(self, event): 
        if event.button !=3:
            pass
        else:
#            print event.ydata
            print event.inaxes.get_position()
            rightMenu = wx.Menu()
            someItem = wx.NewId()
            rightMenu.Append(someItem,'Save plots in MESAplot directory')
            wx.EVT_MENU(rightMenu,someItem,self.savePlots)
            self.PopupMenu(rightMenu)
            rightMenu.Destroy()
    def saveHistoryPlot(self,event):
        extentH=self.H_plot.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        timeStamp = re.sub('[:]','',str(datetime.datetime.now()).split('.')[0])+'.'+ ds.plotExportFileType
        self.canvas.print_figure(self.Hy_var+'-vs-'+self.Hx_var+'-'+timeStamp,format=ds.plotExportFileType,bbox_inches=extentH.expanded(1.2,1.3).shrunk(1,.94))
        print 'History plot saved to MESAplot directory as ' + ds.plotExportFileType
        print 'You can change the file type in the default_settings.py file'
    def saveProfilePlot(self,event):
        extentP=self.P_plot.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        timeStamp = re.sub('[:]','',str(datetime.datetime.now()).split('.')[0])+'.'+ ds.plotExportFileType
        self.canvas.print_figure(self.Py_var+'-vs-'+self.Px_var+'-'+timeStamp,ext=ds.plotExportFileType,bbox_inches=extentP.expanded(1.2,1.3).shrunk(1,.94))
        print 'Profile plot saved to MESAplot directory as ' + ds.plotExportFileType
        print 'You can change the file type in the default_settings.py file'
    def savePlots(self,event):
        extentH=self.H_plot.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        extentP=self.P_plot.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        timeStamp = re.sub('[:]','',str(datetime.datetime.now()).split('.')[0])+'.'+ ds.plotExportFileType
        self.canvas.print_figure(self.Hy_var+'-vs-'+self.Hx_var+'-'+timeStamp,format=ds.plotExportFileType,bbox_inches=extentH.expanded(1.2,1.3).shrunk(1,.94))
        self.canvas.print_figure(self.Py_var+'-vs-'+self.Px_var+'-'+timeStamp,ext=ds.plotExportFileType,bbox_inches=extentP.expanded(1.2,1.3).shrunk(1,.94))
        print 'History and Profile plots saved to MESAplot directory as ' + ds.plotExportFileType
        print 'You can change the file type in the default_settings.py file'
    def drawplot(self):
        Hx_var = self.Hx_var
        Hy_var = self.Hy_var
        Px_var = self.Px_var
        Py_var = self.Py_var
        profile_number=self.profile_number
## current_age_index: line of history file that corresponds to age of current profile shown 
        current_age_index=odat.profile_age_index_in_History[odat.sorted_profile_number(self.profile_number)]
        
        self.H_plot = self.figure.add_subplot(2,1,1)
        self.P_plot = self.figure.add_subplot(2,1,2)

        Hx_data=odat.profile[0][self.start_H:self.end_H:1,odat.history_labels.index(Hx_var)]
        Hy_data=odat.profile[0][self.start_H:self.end_H:1,odat.history_labels.index(Hy_var)]
        Px_data=odat.profile[odat.sorted_profile_number(profile_number)][self.start_P:self.end_P:1,odat.profile_labels.index(Px_var)]
        Py_data=odat.profile[odat.sorted_profile_number(profile_number)][self.start_P:self.end_P:1,odat.profile_labels.index(Py_var)]
        if self.Hgraph_type=="standard":
            self.H_plot.plot(self.operation(self.Hoperation_x,Hx_data), self.operation(self.Hoperation_y,Hy_data), linewidth=1, color=self.line_color,label=Hy_var)
            if self.show_age_flag:
                self.H_plot.plot(self.operation(self.Hoperation_x,odat.profile[0][:,odat.history_labels.index(Hx_var)][current_age_index]),
                            self.operation(self.Hoperation_y,odat.profile[0][:,odat.history_labels.index(Hy_var)][current_age_index]),'ro')    
            if self.show_HLegend_flag:
                self.H_plot.legend(loc=self.HLegend_position)
            Hx_label=Hx_var
            Hy_label=Hy_var
        if self.Hgraph_type=="central_composition":
            for indx in self.central_abundances_to_plot:
                self.H_plot.plot(self.operation(self.Hoperation_x,Hx_data),
                            self.operation(self.Hoperation_y,odat.profile[0][self.start_H:self.end_H:1,odat.history_labels.index('center_'+indx)]),label=indx)
            if self.show_HLegend_flag:
                self.H_plot.legend(loc=self.HLegend_position)
            Hx_label=Hx_var
            Hy_label='central composition'
        if self.Hgraph_type=="central_reactions":
            for indx in self.central_reactions_to_plot:
                self.H_plot.plot(self.operation(self.Hoperation_x,Hx_data),
                            self.operation(self.Hoperation_y,odat.profile[0][self.start_H:self.end_H:1,odat.history_labels.index(indx)]),label=indx)
            if self.show_HLegend_flag:
                self.H_plot.legend(loc=self.HLegend_position)
            Hx_label=Hx_var
            Hy_label='central reactions'
        if self.Hgraph_type=="new_H":
            for indx in self.new_history_to_plot:
                self.H_plot.plot(self.operation(self.Hoperation_x,Hx_data),
                            self.operation(self.Hoperation_y,odat.profile[0][self.start_H:self.end_H:1,odat.history_labels.index(indx)]),label=indx)
            if self.show_HLegend_flag:
                self.H_plot.legend(loc=self.HLegend_position)
            Hx_label=self.Hx_var
            print 'new '+self.Hx_var
            Hy_label=''
        if self.reverse_Hx_Axis:
            self.H_plot.invert_xaxis()
        if self.reverse_Hy_Axis:
            self.H_plot.invert_yaxis()
        if self.show_age_flag:
            if Hx_var=='star_age':
                self.H_plot.axvline(x=self.operation(self.Hoperation_x,float(odat.profileAge[odat.sorted_profile_number(self.profile_number)])),
                               linewidth=1, color=self.age_line_color)
        self.H_plot.set_xlabel(self.operation_label(self.Hoperation_x,Hx_label), fontsize = self.lbl_ftsize, color=self.lbl_color)
        self.H_plot.set_ylabel(self.operation_label(self.Hoperation_y,Hy_label), fontsize = self.lbl_ftsize, color=self.lbl_color)
        if self.Pgraph_type=="standard":
            self.P_plot.plot(self.operation(self.Poperation_x,Px_data), self.operation(self.Poperation_y,Py_data), label=Py_var, linewidth=1, color=self.line_color)
            if self.show_PLegend_flag:
                self.P_plot.legend(loc=self.PLegend_position)
            Px_label=Px_var
            Py_label=Py_var
        if self.Pgraph_type=="composition":
            for indx in self.abundances_to_plot:
                self.P_plot.plot(self.operation(self.Poperation_x,Px_data),
                            self.operation(self.Poperation_y,odat.profile[odat.sorted_profile_number(profile_number)][self.start_P:self.end_P:1,odat.profile_labels.index(indx)]),label=indx)
            if self.show_PLegend_flag:
                self.P_plot.legend(loc=self.PLegend_position)
            Px_label=Px_var
            Py_label='composition'
        if self.Pgraph_type=="reactions":
            for indx in self.reactions_to_plot:
                self.P_plot.plot(self.operation(self.Poperation_x,Px_data),
                            self.operation(self.Poperation_y,odat.profile[odat.sorted_profile_number(profile_number)][self.start_P:self.end_P:1,odat.profile_labels.index(indx)]),label=indx)
            if self.show_PLegend_flag:
                self.P_plot.legend(loc=self.PLegend_position)
            Px_label=Px_var
            Py_label='reactions'
        if self.Pgraph_type=="new_P":
            for indx in self.new_profile_to_plot:
                self.P_plot.plot(self.operation(self.Poperation_x,Px_data),
                            self.operation(self.Poperation_y,odat.profile[odat.sorted_profile_number(profile_number)][self.start_P:self.end_P:1,odat.profile_labels.index(indx)]),label=indx)
            if self.show_PLegend_flag:
                self.P_plot.legend(loc=self.PLegend_position)
            Px_label=Px_var
            Py_label=''
        if self.reverse_Px_Axis:
            self.P_plot.invert_xaxis()
        if self.reverse_Py_Axis:
            self.P_plot.invert_yaxis()
        self.P_plot.set_xlabel(self.operation_label(self.Poperation_x,Px_label), fontsize = self.lbl_ftsize, color=self.lbl_color)
        self.P_plot.set_ylabel(self.operation_label(self.Poperation_y,Py_label), fontsize = self.lbl_ftsize, color=self.lbl_color)
app = wx.App(False)
frame = container("MESAplot",(ds.window_position_x,ds.window_position_y),(ds.window_size_x,ds.window_size_y))
frame.Show()
app.MainLoop()

#########  Changelog   #########
## 6-5-14 Under savePlots, files now save with the plot-type and timestamp in the name. Added several comments in other places. 
## 6-5-14 Under 'file menu (data and star Info)', added 'Save Both Plots' to File Menu (it calls MF.savePlots) 
## 6-13-14 Added a check when 'use_default_path' is True. Will now use file open dialogue from fileManager if the requested default path does not exist. 
## 6-13-14 Added Help and About dialogues to Help Menu, implemented update_graph everywhere. 
## 6-13-14 Arbitrarily designated as version 0.3
## 6-14-14 Fixed plot save function. The images are now properly cropped to not include segments of each other, using Shrink(xm,ym). v.0.3.1
## 6-14-14 Fixed a bug where using 'use_default_path=True' would not set the working directory to the MESAplot directory, not allowing saving of plots. v0.3.1
## 6-14-14 Fixed File_Manager bug that caused OSX systems to close it immediately. v0.3.2
## 6-21-14 Changed MESAoutput1.py to allow handling of data named using old format (star.log, log1.data)
## 6-21-14 Changed a spot in File_Manager for the config.txt file, where a slash was still being used instead of os.path.sep. This was causing crashes in linux.
## 8-5-14 Rewrote prune function, which handles duplicate or non-chronological models. 

#########   Todo   #########
## Process profile image before saving, removing the top portion that catches text from the above history plot (or find out how to pull image position out correctly to begin with) MW
## Arrange on___ functions into logical order
## Move 'use_default_path' check into File_Manager
## Allow opening of Hplot or Pplot into new pyplot windows.
## Change "save both figures" to two separate options, one for each plot.
## Allow support for non-standard data file names in preferences (ie besides history and star.log)

#########   Wishlist   #########
## Allow user to choose naming format for saved plots (including option to prompt upon save), and option to select where to save them. 
## Allow opening a new star without re-opening mesaplot.
## Allow opening multiple stars and multiple plots with tabs.
