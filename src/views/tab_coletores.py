import wx

class TabColetores(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        wx.StaticText(self, label="Conteúdo da aba de Coletores")