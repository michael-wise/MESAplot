import numpy as np

import wx

class CustumizePlotFrame(wx.Frame):
    def __init__(self,list_tot,title,label1,label2):
        wx.Frame.__init__(self, None, -1, title ,size=(350, 300))
        panel = wx.Panel(self, -1)


        self.label1 = wx.StaticText(panel, label=label1)
        self.label1.SetForegroundColour('Blue')
        self.label2 = wx.StaticText(panel, label=label2)
        self.label2.SetForegroundColour('Blue')

        full_list = list_tot

        self.newlist=[]

        self.full_list_box = wx.ListBox(panel, 26, wx.DefaultPosition, (170, 150),
                                     full_list, wx.LB_MULTIPLE)
        
        self.btn_ok = wx.Button(panel, label='OK')
        self.Bind(wx.EVT_BUTTON, self.On_OK, self.btn_ok) 



        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.full_list_box, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
        sizer1.Add(self.btn_ok, 0, wx.ALIGN_LEFT | wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label1, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
        sizer.Add(self.label2, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
        sizer.Add(sizer1, 0, wx.ALIGN_LEFT | wx.ALL, border=5)

        panel.SetSizer(sizer)
        panel.Fit()
        

    def On_OK(self, event):
        Testlist=self.newlist
        selected_list= self.full_list_box.GetSelections()
        for i in selected_list:
            Testlist.append(str(self.full_list_box.GetString(i)))
        self.newlist=Testlist
##        print 'new reactions selected for the history plot'
##        print self.newlist

        self.Close()


        
##class CustumizePlotFrameXY(wx.Frame):
##    def __init__(self,list_tot,title,label1,label2,default):
##        wx.Frame.__init__(self, None, -1, title ,size=(450, 350))
##        panel = wx.Panel(self, -1)
##
##
##        self.label1 = wx.StaticText(panel, label=label1)
##        self.label1.SetForegroundColour('Blue')
##        self.label2 = wx.StaticText(panel, label=label2)
##        self.label2.SetForegroundColour('Blue')
##
##        full_list = list_tot
##
##        self.newlist=[]
##        self.XSelection=''
##
##        self.full_list_box_X = wx.ListBox(panel, 26, wx.DefaultPosition, (170, 150),
##                                     full_list,wx.LB_SINGLE)
##        self.full_list_box_Y = wx.ListBox(panel, 26, wx.DefaultPosition, (170, 150),
##                                     full_list, wx.LB_MULTIPLE)
##        
##        self.btn_ok = wx.Button(panel, label='OK')
##        self.Bind(wx.EVT_BUTTON, self.On_OK, self.btn_ok) 
##
##
##
##        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
##        sizer1.Add(self.full_list_box_X, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##        sizer1.Add(self.full_list_box_Y, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##
##        sizer = wx.BoxSizer(wx.VERTICAL)
##        sizer.Add(self.label1, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##        sizer.Add(self.label2, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##        sizer.Add(sizer1, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##        sizer.Add(self.btn_ok, 0, wx.ALIGN_LEFT | wx.ALL, border=5)
##
##        panel.SetSizer(sizer)
##        panel.Fit()
##        
##
##    def On_OK(self, event):
##        Testlist=self.newlist
##        selected_list_Y= self.full_list_box_Y.GetSelections()
##        X_Selection= self.full_list_box_X.GetSelection()
##        for i in selected_list_Y:
##            Testlist.append(str(self.full_list_box_Y.GetString(i)))
##        self.newlist=Testlist
##        self.XSelection=str(self.full_list_box_X.GetString(X_Selection))
####        print 'new reactions selected for the history plot'
##        print self.XSelection
##
##        self.Close()
