import sys
import os
import wx

# Adiciona o diretório 'src' ao sys.path para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from views.main_window import MainWindow

if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow(None, "GesCol - Gestão de Equipamentos Logísticos")
    main_window.Show()
    app.MainLoop()