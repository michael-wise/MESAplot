import os, re, wx

app = wx.App(False)
class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(1,1))
        self.timer = wx.Timer(self) 
        self.Bind(wx.EVT_TIMER, self.OnTimer) 
        self.timer.Start(1, True)
    def OnTimer(self,evt):
        self.Close()
os.chdir(os.path.dirname(os.path.realpath(__file__)))
progPath= os.path.dirname(os.path.realpath(__file__))
if os.path.isfile(progPath + os.path.sep + 'config.txt'):
    f=open(progPath + os.path.sep + 'config.txt','r+')
    lines=f.read().splitlines()
    if len(lines) == 0 and not lines:
        frame=Frame("Opening Directory Selector")
        frame.Show()
        app.MainLoop()
        openFileDialog = wx.DirDialog(None, "Select data folder")
        openFileDialog.ShowModal()
        path_folder=str(openFileDialog.GetPath())
        f.seek(0,2)
        f.write(path_folder)
        f.close()
    else:
        for i in reversed(lines):
            if os.path.isdir(i.rpartition(os.path.sep)[0]):
                defaultPath=i.rpartition(os.path.sep)[0]
                break
            else:
                defaultPath=''
        frame=Frame("Opening Directory Selector")
        frame.Show()
        app.MainLoop()
        openFileDialog = wx.DirDialog(None, "Select data folder",defaultPath)
        openFileDialog.ShowModal()
        path_folder=str(openFileDialog.GetPath())
        f.seek(0,2)
        f.write('\n' + path_folder)
        f.close()
else:
    f=open(progPath + os.path.sep + 'config.txt','w+')
    frame=Frame("Opening Directory Selector")
    frame.Show()
    app.MainLoop()
    openFileDialog = wx.DirDialog(None, "Select data folder")
    openFileDialog.ShowModal()
    path_folder=str(openFileDialog.GetPath())
    f.seek(0,2)
    f.write(path_folder)
    f.close()

openFileDialog.Destroy()


#########  Changelog   #########
## 6-14-14 Added Mainloop start and close, which fixes a bug where DirDialog would not open properly on OSX.
