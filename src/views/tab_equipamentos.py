import wx

class TabEmpilhadeiras(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        wx.StaticText(self, label="Conteúdo da aba de Empilhadeiras")